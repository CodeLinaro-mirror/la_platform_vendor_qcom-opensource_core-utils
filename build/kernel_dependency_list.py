# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

# Base directories: current layout and the 16k variant (same file hierarchy,
# future migration target).
KERNEL_PREBUILT_DIR_BASES = [
    "device/qcom/$(TARGET_BOARD_PLATFORM)-kernel",
    "device/qcom/$(TARGET_BOARD_PLATFORM)-kernel/16k",
    "$(KERNEL_PREBUILT_DIR)",
    "$(KERNEL_PREBUILT_DIR)/16k",
]

# Relative paths that are valid under either base directory above.
KERNEL_PREBUILT_DIR_FILES = [
    "debug",
    "kernel-gbl/gbl_aarch64.efi",
    "kernel-gbl/gbl.bin",
    "kernel-abl/abl.bin",
    "vendor_dlkm/system_dlkm.modules.blocklist",
    "extra_cmdline",
    "extra_bootconfig",
    "build_opts.txt",
    "Image",
    "System.map",
    "debug/kernel-tests",
    "kernel-headers",
    "kernel-abl/abl-$(TARGET_BUILD_VARIANT)",
    "dtbs",
    "dtbs/dtbo.img",
    "dtbs/dtb.img",
    "dtbo.img",
    "$(1)/modules.load",
    "modules.load",
    "system_dlkm/flatten/lib/modules",
    "system_dlkm/flatten/lib/modules/*.ko",
    "$(notdir $@)",
    "vendor_dlkm/$(notdir $@)",
    "vendor_dlkm/modules.blocklist",
    "vendor_dlkm/cfg80211.ko",
    "vendor_dlkm/mac80211.ko",
    "vendor_dlkm",
    "techpack.built",
    ".config",
    "Module.symvers",
    "system_dlkm/flatten/lib/modules/$(notdir $@)",
]

KERNEL_DEPENDENCY_ALLOWED_LIST = {
    "{}/{}".format(base, file)
    for base in KERNEL_PREBUILT_DIR_BASES
    for file in KERNEL_PREBUILT_DIR_FILES
}
