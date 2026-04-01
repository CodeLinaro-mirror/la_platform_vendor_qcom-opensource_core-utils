# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear


#!/usr/bin/python
import sys
import os
from pathlib import Path
root_dir = str(Path.cwd())
pyyaml_path = os.path.join(root_dir, "external", "python", "pyyaml", "lib")
sys.path.insert(0, pyyaml_path)
import yaml
from typing import List
import central_feature_tool_constants as constants
from common_utils import QtiFeatureLogger
from build_types import BuildConfig, StitchResult

logger = QtiFeatureLogger()


def get_provenance_data(file_path: str) -> str:
    root = str(Path(file_path).resolve())
    pwd = str(Path.cwd()) + '/'
    root = root.replace(pwd, "", 1)
    provenance_data = (
        f"provenance_data:\n"
        f"  source_file: {root}\n"
        f"  module_git_path: ''\n"
        f"  manifest_linkfile_path: {file_path}\n")
    return provenance_data


def get_metadata(profile: str, target: str, version: str = '""') -> str:
    metadata = (
        f"metadata:\n"
        f"  version: {version}\n"
        f"  generated_by: {constants.CREATED_BY}\n"
        f"  profile: {profile}\n"
        f"  target: {target}\n"
    )
    return metadata


def load_schema(schema_config_path: str) -> dict:
    try:
        with open(schema_config_path, 'r', encoding='utf-8') as schema_yaml:
            schema_dict = yaml.safe_load(schema_yaml)
            if schema_dict is None:
                logger.error("[parse_and_stitch]: error parsing schema yaml")
                return {}
        logger.info(f"[parse_and_stitch]: parsed schema yaml: {schema_config_path}")
        return schema_dict
    except FileNotFoundError as e:
        logger.error(f"[parse_and_stitch]: File not found {e}")
        return {}
    except Exception as e:
        logger.error(f"[parse_and_stitch]: {e}")
        return {}


def dump_centralized_file(combined_features: str, centralized_file_path: str) -> int:
    try:
        with open(centralized_file_path, 'w', encoding='utf-8') as centralized_features_file:
            centralized_features_file.write(constants.CENTRAL_YAML_HEADER)
            centralized_features_file.write(combined_features)
        return 0
    except FileNotFoundError as e:
        logger.error(f"[parse_and_stitch]: File not found {e}")
        return -1
    except Exception as e:
        logger.error(f"[parse_and_stitch]: {e}")
        return -1


def indent_content(content: str, indent_level: int = 2) -> str:
    indent = " " * indent_level
    return "\n".join(f"{indent}{line}" for line in content.splitlines())


def get_combined_content(yaml_file_list: List[str]) -> str:
    """ read all fragment yaml files and return the combined text. """
    combined_content = ""
    try:
        for path in yaml_file_list:
            root = str(Path(path).resolve())
            pwd = str(Path.cwd()) + '/'
            root = root.replace(pwd, "", 1)
            key = root.replace("/", "__")
            with open(path, 'r') as fragment_yaml:
                logger.info(f"[parse_and_stitch]: parsing fragment yaml: {path}")
                raw_data = fragment_yaml.read().strip()
                combined_content += key + ':\n'
                combined_content += indent_content(get_provenance_data(path), 2) + "\n"
                combined_content += indent_content(raw_data, 2) + "\n"
        return combined_content
    except Exception as e:
        logger.error(f"[parse_and_stitch]: Error parsing and stitching fragments: {e}")
        return None


def parse_and_stitch(yaml_file_list: List[str], config: BuildConfig, yaml_out_dir: str) -> tuple[int, StitchResult | None]:
    """
    INPUT:
        yaml_file_list: resolved list of Fragment YAML files
        config: BuildConfig with profile, target, schema_config_path
    OUTPUT:
        (0, StitchResult)  on success
        (-1, None)         on failure
    """
    try:
        if not os.path.exists(yaml_out_dir):
            os.makedirs(yaml_out_dir, exist_ok=True)
            logger.info(f"[parse_and_stitch]: created directory: '{yaml_out_dir}'")

        schema_dict = {}
        if not os.path.exists(config.schema_config_path):
            logger.warning("[parse_and_stitch]: schema file does not exist")
        else:
            schema_dict = load_schema(config.schema_config_path)
            if not schema_dict:
                logger.warning("[parse_and_stitch]: schema.yaml is empty")
                
    
        metadata = get_metadata(config.profile, config.target, schema_dict.get('version', '""'))
        
        feature_yaml_data = get_combined_content(yaml_file_list)
        if feature_yaml_data is None:
            return -1, None
        combined_content = metadata + feature_yaml_data
        feature_dict = yaml.safe_load(combined_content)
        return 0, StitchResult(feature_dict=feature_dict, schema_dict=schema_dict, combined_content=combined_content)
    except FileNotFoundError as e:
        logger.error(f"[parse_and_stitch]: File not found {e}")
        return -1, None
    except OSError as e:
        logger.error(f"[parse_and_stitch]: Failed to create output directory: {e}")
        return -1, None
    except Exception as e:
        logger.error(f"[parse_and_stitch]: {e}")
        return -1, None
