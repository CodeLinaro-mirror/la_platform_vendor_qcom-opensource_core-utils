# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

from dataclasses import dataclass, field
from enum import Enum
import os
import central_feature_tool_constants as constants


class BuildStatus(str, Enum):
    FULL_RUN  = 'full_run'
    NO_CHANGE = 'no_change'


class BuildVariant(str, Enum):
    VENDOR = 'vendor'
    QSSI   = 'qssi'


@dataclass
class BuildConfig:
    """Build identity and input configuration, derived from CLI arguments."""
    input_path:         str
    out_dir:            str
    schema_config_path: str
    profile:            str
    target:             str
    build_variant:      str = 'vendor'
    extra_params:       dict = field(default_factory=dict)


@dataclass
class BuildPaths:
    """All output/intermediate file paths, auto-computed from out_dir."""
    out_dir:           str
    build_variant:     str = 'vendor'
    snapshot_yaml:     str = field(init=False)
    snapshot_artifact: str = field(init=False)
    gen_out_dir:       str = field(init=False)
    central_yaml:      str = field(init=False)
    yaml_out_dir:      str = field(init=False)

    def __post_init__(self):
        vp = constants.VARIANT_PATHS[self.build_variant]
        self.snapshot_yaml     = os.path.join(self.out_dir, vp["snapshot_yaml_file"])
        self.snapshot_artifact = os.path.join(self.out_dir, vp["snapshot_artifact_file"])
        self.gen_out_dir       = os.path.join(self.out_dir, vp["impl_gen_dir"])
        self.central_yaml      = os.path.join(self.out_dir, vp["central_features_file"])
        self.yaml_out_dir      = os.path.join(self.out_dir, vp["yaml_out_dir"])


@dataclass
class StitchResult:
    """In-memory outputs from the parse_and_stitch pipeline stage."""
    feature_dict:     dict
    schema_dict:      dict
    combined_content: str