# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

import os
import sys
from pathlib import Path
root_dir = str(Path.cwd())
pyyaml_path = os.path.join(root_dir, "external", "python", "pyyaml", "lib")
sys.path.insert(0, pyyaml_path)
import yaml
import hashlib
from typing import List
from common_utils import QtiFeatureLogger
from stitch_parser import get_combined_content, get_metadata
from build_types import BuildConfig, BuildPaths, BuildStatus
import central_feature_tool_constants as constants

logger = QtiFeatureLogger()


def get_dict_key(filepath: Path) -> str:
    """Converts a filepath to a dict key."""
    root = str(Path(filepath).resolve())
    pwd = str(Path.cwd()) + '/'
    root = root.replace(pwd, "", 1)
    key = root.replace("/", "__")
    return key


def compute_file_hash(filepath: Path) -> str:
    """Compute MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_artifact_hash(artifact_dir: str) -> dict | None:
    """Compute hashes of all files in the artifact output directory."""
    out_path = Path(artifact_dir)
    current_hashes = {}
    try:
        for filepath in out_path.rglob("*"):
            if filepath.is_file():
                key = get_dict_key(filepath)
                current_hashes[key] = {'hash': compute_file_hash(filepath)}
        return current_hashes
    except Exception as e:
        logger.error(f"[incremental_build]: error computing artifact hashes: {e}")
        return None


def save_artifact_snapshot(paths: BuildPaths) -> int:
    """Save artifact snapshot to file."""
    current_hashes = get_artifact_hash(paths.gen_out_dir)
    if current_hashes is None:
        return -1
    try:
        with open(paths.snapshot_artifact, 'w') as f:
            yaml.dump(current_hashes, f, sort_keys=False, default_flow_style=False)
        return 0
    except FileNotFoundError as e:
        logger.error(f"[incremental_build]: File not found {e}")
        return -1
    except Exception as e:
        logger.error(f"[incremental_build]: {e}")
        return -1


def dump_hash(combined_content: str, snapshot_yaml: str) -> int:
    """ save hash of central yaml file. """
    try:
        with open(snapshot_yaml, 'w') as snap_file:
            hash_data = {
                "file": snapshot_yaml,
                "hash": hashlib.md5(combined_content.encode()).hexdigest()
            }
            yaml.dump(hash_data, snap_file, sort_keys=False, default_flow_style=False)
        return 0
    except Exception as e:
        logger.error(f"[incremental_build]: dump_hash failed: {e}")
        return -1


def incremental_build(yaml_file_list: List[str], config: BuildConfig, paths: BuildPaths) -> tuple[int, BuildStatus | None]:
    try:
        if not os.path.exists(paths.snapshot_yaml) or not os.path.exists(paths.snapshot_artifact):
            logger.info("[incremental_build]: snapshot file not found, running full build...")
            return 0, BuildStatus.FULL_RUN
        if os.path.exists(config.schema_config_path):
            with open(config.schema_config_path, 'r') as schema_file:
                schema_dict = yaml.safe_load(schema_file)
            version = schema_dict.get('version', '""')
            metadata = get_metadata(config.profile, config.target, version)
        else:
            metadata = get_metadata(config.profile, config.target)

        combined_content = get_combined_content(yaml_file_list)
        if combined_content is None:
            logger.error("[incremental_build]: Error reading features yaml")
            return -1, None
        current_combined = metadata + combined_content
        current_hash = hashlib.md5(current_combined.encode()).hexdigest() # calculate the hash of current central yaml
        
        if not os.path.exists(paths.central_yaml):
            return 0, BuildStatus.FULL_RUN
        with open(paths.snapshot_yaml, 'r') as snap_file:
            stored_data = yaml.safe_load(snap_file)
        stored_hash = stored_data.get('hash', '')
        
        if stored_hash != current_hash:
            return 0, BuildStatus.FULL_RUN
        expected_central_hash = hashlib.md5((constants.CENTRAL_YAML_HEADER + current_combined).encode()).hexdigest()
        
        with open(paths.central_yaml, 'r') as yaml_file:  # 
            actual_central_hash = hashlib.md5(yaml_file.read().encode()).hexdigest()
        if actual_central_hash != expected_central_hash:
            return 0, BuildStatus.FULL_RUN
        
        with open(paths.snapshot_artifact, 'r') as yaml_artifact_hash: # check artifact yaml
            stored_artifact_hashes = yaml.safe_load(yaml_artifact_hash)
        current_artifact_hash = get_artifact_hash(paths.gen_out_dir)
        if current_artifact_hash is None or current_artifact_hash != stored_artifact_hashes:
            return 0, BuildStatus.FULL_RUN
        return 0, BuildStatus.NO_CHANGE
    
    except Exception as e:
        logger.error(f"[incremental_build]: Exception in incremental build {e}")
        return -1, None
