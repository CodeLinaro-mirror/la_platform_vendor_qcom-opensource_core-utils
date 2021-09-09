
.PHONY:vendor_prop_context_restriction_enforcement

vendor_prop_context_restriction_enforcement:
ifneq ($(BOARD_OPENSOURCE_DIR), )
	python $(BOARD_OPENSOURCE_DIR)/core-utils/build/vendor_prop_context_restriction.py --m error
else
	python vendor/qcom/opensource/core-utils/build/vendor_prop_context_restriction.py --m error
endif  #BOARD_OPENSOURCE_DIR

ifneq ($(TARGET_PRODUCT), qssi)
droidcore:vendor_prop_context_restriction_enforcement
endif
