# Centralized Feature Control
FEATURE_CONFIG_MK := vendor/qcom/opensource/core-utils-vendor/centralized-features-vendor/features-vendor-impl-gen/make_feature_config/config.mk
ifneq ($(wildcard $(FEATURE_CONFIG_MK)),)
  include $(FEATURE_CONFIG_MK)
else
  $(warning Centralized feature config not found: $(FEATURE_CONFIG_MK))
endif