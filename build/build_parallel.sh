#!/usr/bin/env bash
# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear
#
# build_parallel.sh
# Modes:
#   1) Default mode (no options, no env): run built-in default full commands (includes tee)
#   2) Env mode (no options, but KERNEL_CMD and ANDROID_CMD env vars set): use those env vars
#   3) Cmd mode (both --kernel-cmd and --android-cmd provided): execute provided commands as-is
#   4) Clean mode: ./build_parallel.sh clean → remove build output directories
# Usage:
#   ./build_parallel.sh
#   KERNEL_CMD='...' ANDROID_CMD='...' ./build_parallel.sh
#   ./build_parallel.sh --kernel-cmd '...' --android-cmd '...'
#   ./build_parallel.sh clean

set -Eeo pipefail

print_usage() {
  cat <<'USAGE' >&2
Usage:
  ./build_parallel.sh
    Run default commands:
      RECOMPILE_KERNEL=1 ./kernel_platform/build/android/prepare_vendor.sh < /dev/null |& tee prepare.txt
      (time bash build.sh -j$(nproc) dist --target_only) |& tee makelog.txt

  KERNEL_CMD='<kernel full command>' ANDROID_CMD='<android full command>' ./build_parallel.sh
    Use the two environment variables as commands.

  ./build_parallel.sh --kernel-cmd '<kernel full command>' --android-cmd '<android full command>'
    Execute the two provided full command strings. Both options are required in cmd mode.

  ./build_parallel.sh clean
    Remove build output directories:
      out/
      kernel_platform/out
      kernel_platform/bazel-cache

Examples:
  1: ./build_parallel.sh
  2: KERNEL_CMD="RECOMPILE_KERNEL=1 ./kernel_platform/build/android/prepare_vendor.sh < /dev/null |& tee prepare.txt" \
  ANDROID_CMD="(time bash build.sh -j$(nproc) dist --target_only) |& tee makelog.txt" ./build_parallel.sh
  3: ./build_parallel.sh \
    --kernel-cmd "RECOMPILE_KERNEL=1 ./kernel_platform/build/android/prepare_vendor.sh < /dev/null |& tee prepare.txt" \
    --android-cmd "(time bash build.sh -j$(nproc) dist --target_only) |& tee makelog.txt"
  4: ./build_parallel.sh clean
USAGE
}

# BASELINE_VERSION: build_parallel_v1

MAKE_JOBS="$(nproc)"

# Default full commands
DEFAULT_KERNEL_CMD='RECOMPILE_KERNEL=1 ./kernel_platform/build/android/prepare_vendor.sh < /dev/null |& tee prepare.txt'
DEFAULT_ANDROID_CMD="(time bash build.sh -j${MAKE_JOBS} dist --target_only) |& tee makelog.txt"

# Parse options into separate variables so we don't clobber environment variables
PARSED_KERNEL_CMD=""
PARSED_ANDROID_CMD=""

clean_env() {
  unset KERNEL_VENDOR_PARALLEL_BUILDING
}

# Special case: clean
if [ "${1:-}" = "clean" ]; then
  clean_env
  echo "Cleaning build output directories..."
  rm -rf out/ kernel_platform/out kernel_platform/bazel-cache
  echo "Clean finished."
  exit 0
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --kernel-cmd)
      if [ $# -lt 2 ]; then
        echo "Error: --kernel-cmd requires an argument" >&2
        print_usage
        exit 2
      fi
      PARSED_KERNEL_CMD="$2"
      shift 2
      ;;
    --android-cmd)
      if [ $# -lt 2 ]; then
        echo "Error: --android-cmd requires an argument" >&2
        print_usage
        exit 2
      fi
      PARSED_ANDROID_CMD="$2"
      shift 2
      ;;
    --help|-h)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_usage
      exit 2
      ;;
  esac
done

# Decide mode and set KERNEL_CMD_STR / ANDROID_CMD_STR
# Priority:
# 1) If both parsed options provided -> use parsed (cmd mode)
# 2) Else if no parsed options but both env vars KERNEL_CMD and ANDROID_CMD are set -> use env (env mode)
# 3) Else -> use defaults (default mode)
if [ -n "$PARSED_KERNEL_CMD" ] || [ -n "$PARSED_ANDROID_CMD" ]; then
  # cmd mode requires both parsed options
  if [ -z "$PARSED_KERNEL_CMD" ] || [ -z "$PARSED_ANDROID_CMD" ]; then
    echo "Error: both --kernel-cmd and --android-cmd must be provided in cmd mode" >&2
    print_usage
    exit 2
  fi
  KERNEL_CMD_STR="$PARSED_KERNEL_CMD"
  ANDROID_CMD_STR="$PARSED_ANDROID_CMD"
else
  # no parsed options; check environment variables KERNEL_CMD and ANDROID_CMD
  if [ -n "${KERNEL_CMD:-}" ] && [ -n "${ANDROID_CMD:-}" ]; then
    KERNEL_CMD_STR="$KERNEL_CMD"
    ANDROID_CMD_STR="$ANDROID_CMD"
  else
    # fallback to defaults
    KERNEL_CMD_STR="$DEFAULT_KERNEL_CMD"
    ANDROID_CMD_STR="$DEFAULT_ANDROID_CMD"
  fi
fi

# Environment check
if [ -z "${TARGET_PRODUCT:-}" ]; then
  echo "error: No target product; please set TARGET_PRODUCT using 'lunch <target>-<release>-<build_type>'" >&2
  exit 1
fi

# Whitelist check for target
ALLOWED_TARGETS=("canoe" "art")

platform_ok=false
for p in "${ALLOWED_TARGETS[@]}"; do
  if [ "$TARGET_BOARD_PLATFORM" = "$p" ]; then
    platform_ok=true
    break
  fi
done

if [ "$platform_ok" = false ]; then
  echo "error: Unsupported TARGET_BOARD_PLATFORM='$TARGET_BOARD_PLATFORM'." >&2
  echo "Allowed values are: ${ALLOWED_TARGETS[*]}" >&2
  exit 1
fi

# Function to extract arguments passed to prepare_vendor.sh from KERNEL_CMD_STR
extract_prepare_args() {
  local cmd="$1"
  local script='./kernel_platform/build/android/prepare_vendor.sh'

  # Check if the command contains prepare_vendor.sh
  case "$cmd" in
    *"$script"* )
      # Remove everything up to and including the script path
      local tail="${cmd#*${script}}"
      ;;
    *)
      # Script not found in command, return empty string
      echo ""
      return 0
      ;;
  esac

  # Remove redirections and pipes (|, |&, <, > and everything after them)
  tail="${tail%%|&*}"
  tail="${tail%%| *}"
  tail="${tail%%<*}"
  tail="${tail%%>*}"

  # Trim leading and trailing whitespace
  local args
  args="$(echo "$tail" | xargs)"

  echo "$args"
}

pid_prepare=""
pid_build=""
pid_prepare_for_parallel=""
# Cleanup function to forward signals and kill child process groups
cleanup() {
  echo "Interrupt received, terminating child processes..." >&2
  clean_env
  if [ -n "$pid_prepare_for_parallel" ]; then
    kill -TERM -- -"$pid_prepare_for_parallel" 2>/dev/null || true
    sleep 1
    kill -KILL -- -"$pid_prepare_for_parallel" 2>/dev/null || true
  fi
  if [ -n "$pid_prepare" ]; then
    kill -TERM -- -"$pid_prepare" 2>/dev/null || true
    sleep 1
    kill -KILL -- -"$pid_prepare" 2>/dev/null || true
  fi
  if [ -n "$pid_build" ]; then
    kill -TERM -- -"$pid_build" 2>/dev/null || true
    sleep 1
    kill -KILL -- -"$pid_build" 2>/dev/null || true
  fi
  exit 130
}

trap cleanup SIGINT SIGTERM

echo "Kernel prepare stage..."
# Extract arguments from KERNEL_CMD_STR and pass them to prepare_for_parallel.sh
PREPARE_ARGS="$(extract_prepare_args "$KERNEL_CMD_STR")"
echo "Prepare args extracted from kernel cmd: '${PREPARE_ARGS}'"

setsid bash -c "./kernel_platform/build/kernel/android/prepare_for_parallel.sh ${PREPARE_ARGS:+$PREPARE_ARGS}" &
pid_prepare_for_parallel=$!
wait "$pid_prepare_for_parallel"
prepare_for_parallel_status=$?

if [ $prepare_for_parallel_status -ne 0 ]; then
  echo "prepare_for_parallel.sh failed (exit=$prepare_for_parallel_status), exit"
  exit 1
fi

# this env variable inidcates we are in parallel build
export KERNEL_VENDOR_PARALLEL_BUILDING=true

PRECHECK_DIR="out/target/product/$TARGET_PRODUCT/obj/pre_check_kernel"
if [ -d "$PRECHECK_DIR" ]; then
  rm -rf "$PRECHECK_DIR"
fi
mkdir -p "$PRECHECK_DIR"

# Print commands for visibility
echo "Kernel command: $KERNEL_CMD_STR"
echo "Android command: $ANDROID_CMD_STR"

KERNEL_RESULT="$PRECHECK_DIR/prepare_vendor_result"
ANDROID_RESULT="$PRECHECK_DIR/android_result"
rm -f "$KERNEL_RESULT" "$ANDROID_RESULT"

# Unified handler for both SIGUSR1 (Android) and SIGUSR2 (Kernel)
handle_build_done() {
  sig="$1"
  case "$sig" in
    SIGUSR1)
      echo "Parent received SIGUSR1: Android build finished"
      result_file="$ANDROID_RESULT"
      other_pid="$pid_prepare"
      other_name="Kernel"
      ;;
    SIGUSR2)
      echo "Parent received SIGUSR2: Kernel build finished"
      result_file="$KERNEL_RESULT"
      other_pid="$pid_build"
      other_name="Android"
      ;;
  esac

  if [ -f "$result_file" ]; then
    ret=$(cat "$result_file")
    [[ "$ret" =~ ^[0-9]+$ ]] || ret=1
  else
    echo "Result file not found, treating as failure" >&2
    ret=1
  fi

  if [ "$ret" -ne 0 ]; then
    echo "$sig build failed (exit code $ret), terminating $other_name..."
    kill -0 "$other_pid" 2>/dev/null && kill -TERM -- -"$other_pid" 2>/dev/null || true
  else
    echo "$sig build succeeded (exit code $ret)"
  fi
}

trap 'handle_build_done SIGUSR1' SIGUSR1
trap 'handle_build_done SIGUSR2' SIGUSR2

# Start kernel build
setsid bash -c "
  set -o pipefail
  ${KERNEL_CMD_STR}
  rc=\$?
  echo -n \$rc > \"$KERNEL_RESULT\"
  kill -USR2 $$
  exit \$rc
" &
pid_prepare=$!

# Start Android build
setsid bash -c "
  set -o pipefail
  ${ANDROID_CMD_STR}
  rc=\$?
  echo -n \$rc > \"$ANDROID_RESULT\"
  kill -USR1 $$
  exit \$rc
" &
pid_build=$!

# Wait for both tasks
wait "$pid_prepare" || true
wait "$pid_build" || true

# Read results
ret_prepare=1; ret_build=1
[ -f "$KERNEL_RESULT" ] && ret_prepare=$(cat "$KERNEL_RESULT")
[ -f "$ANDROID_RESULT" ] && ret_build=$(cat "$ANDROID_RESULT")

echo "Kernel exit code: $ret_prepare"
echo "Android exit code: $ret_build"
echo "Build process finished."

trap - SIGINT SIGTERM
clean_env

if [ "$ret_prepare" -ne 0 ] || [ "$ret_build" -ne 0 ]; then
  exit 1
fi
exit 0
