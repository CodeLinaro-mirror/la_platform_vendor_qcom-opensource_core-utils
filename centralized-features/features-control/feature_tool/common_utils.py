# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

import logging, sys
# Common Utils Header file for centralized feature tools
class QtiFeatureConstants:
    # Feature Key Definitions
    FEATURE_SCOPE_KEY = "feature_scope"
    FEATURE_VALUE_KEY = "feature_value"
    FEATURE_TYPE_KEY = "feature_datatype"
    # Feature Scope Values
    FEATURE_SCOPE_MAKE = "make"
    FEATURE_SCOPE_NATIVE = "native"
    FEATURE_SCOPE_JAVA = "java"
    FEATURE_SCOPE_RUNTIME = "runtime"
    FEATURE_SCOPE_ALL = "all"
    # Feature Type Values
    FEATURE_TYPE_STRING = "string"
    FEATURE_TYPE_BOOLEAN = "boolean"
    FEATURE_TYPE_INTEGER = "integer"

class QtiFeatureUtils:
    @staticmethod
    def iter_feature_nodes(features_dict: dict):
        """
        Deep-interate YAML Dict to find out all Feature Nodes
        """
        for key in features_dict.keys():
            node = features_dict[key]
            if isinstance(node, dict):
                if "feature_value" in node:
                    yield key, node
                else:
                    yield from QtiFeatureUtils.iter_feature_nodes(node)
            elif isinstance(node, list):
                for idx, item in enumerate(node):
                    if isinstance(item, dict):
                        yield from QtiFeatureUtils.iter_feature_nodes(item)

    @staticmethod
    def get_all_feature_nodes(features_dict: dict) -> dict:
        return dict(QtiFeatureUtils.iter_feature_nodes(features_dict))

    @staticmethod
    def add_sys_path(path_list: list) -> None:
        for path in path_list:
            if path not in sys.path:
                sys.path.insert(0, path)

''' Logger utility class'''
class QtiFeatureLogger:

    def __init__(self):
        pass

    #incase we want to add file based logging later
    def do_logger_setup(log_type, log_file, level):
        log_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(log_type)
        logger.setLevel(level)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
        return logger

    #we can add multiple here to decide the log destination
    logStdOut = do_logger_setup("Centralized Feature Control", None, logging.DEBUG)

    @staticmethod
    def info(message):
        QtiFeatureLogger.logStdOut.info(message)

    @staticmethod
    def warning(message):
        QtiFeatureLogger.logStdOut.warning(message)

    @staticmethod
    def error(message):
        QtiFeatureLogger.logStdOut.error(message)