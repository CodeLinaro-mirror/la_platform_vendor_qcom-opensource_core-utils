# Copyright (c) 2021 The Linux Foundation. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of The Linux Foundation nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

FAILED_FILEPATHS_WHITELIST = {
    "vendor/qcom/opensource/audio-hal/primary-hal/configs/qssi/qssi.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/qrdplus/China/ChinaMobile/products.mk",
    "vendor/qcom/proprietary/qrdplus/China/ChinaTelecom/products.mk",
    "vendor/qcom/proprietary/qrdplus/China/ChinaUnicom/products.mk",
    "vendor/qcom/proprietary/qrdplus/China/CTA/products.mk",
    "vendor/qcom/proprietary/qrdplus/Extension/products.mk",
    "vendor/qcom/proprietary/commonsys/qrdplus/sva/products.mk",
    "vendor/qcom/proprietary/commonsys/voiceui/products.mk",
    "vendor/qcom/proprietary/resource-overlay/overlay.mk",
    "vendor/qcom/proprietary/chi-cdk/product.mk",
    "vendor/qcom/proprietary/prebuilt_ASAN/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/android-perf/profiles.mk",
    "vendor/qcom/proprietary/mm-audio-internal/dolby/dax/device/dax2_common_hw.mk",
    "vendor/qcom/proprietary/qrdplus/InternalUseOnly/DuerosSDK/products.mk",
}

SHELL_WHITELIST = {
    "device/qcom/common/init/Android.mk",
    "device/qcom/common/utils.mk",
    "device/qcom/sepolicy/SEPolicy.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/kalama/Android.mk",
    "vendor/qcom/opensource/touch-drivers/Android.mk",
    "vendor/qcom/proprietary/data-noship/qcril-data-utf/test/utf/Android.mk",
    "vendor/qcom/proprietary/wigig/ftm_flows/libwigig_ftm_flows/Android.mk",
    "vendor/qcom/proprietary/wigig/debug-tools/lib/FlashAcss/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/samples/apps/camera_test/Android.mk",
    "vendor/qcom/opensource/eva-kernel/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/tools/sensors_calibration/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/service/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/samples/plugins/eyetracking/Android.mk",
    "vendor/qcom/opensource/wlan/utils/sigma-dut/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/sm8150/Android.mk",
    "vendor/qcom/proprietary/wigig/sensing/sensingdaemon/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/samples/apps/imu_test/Android.mk",
    "vendor/qcom/proprietary/Innopath/FOTA/MobileUpdateClient/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/sm6125/Android.mk",
    "vendor/qcom/proprietary/ml/nnhal/qnn-gpu/QNN/GPU/OpPackage/Android.mk",
    "vendor/qcom/proprietary/wigig/debug-tools/lib/WlctPciAcss/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/tools/qvrdatalogger/Android.mk",
    "device/qcom/common/init/Android.mk",
    "vendor/qcom/proprietary/ml/nnhal/qnn-gpu/QNN/GPU/Backend/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/bengal/Android.mk",
    "vendor/qcom/proprietary/wigig/ftm_flows/ftm_flows_test/Android.mk",
    "vendor/qcom/proprietary/wlan/utils/halproxydaemon/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/common/Android.mk",
    "vendor/qcom/proprietary/wigig/debug-tools/lib/utils/Android.mk",
    "vendor/qcom/proprietary/ts_firmware/taro/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/services/2dframework/Android.mk",
    "vendor/qcom/proprietary/wigig-noship/location/libaoa/Android.mk",
    "vendor/qcom/proprietary/ac_policy-noship/Android.mk",
    "vendor/qcom/opensource/wlan/qcacld-3.0/Android.mk",
    "vendor/qcom/proprietary/securemsm-internal/isdbtmm/test/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/taro/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/lahaina/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/Android.mk",
    "vendor/qcom/proprietary/wigig/debug-tools/host_manager_11ad/Android.mk",
    "vendor/qcom/proprietary/platform-boost/platform_boost_hal/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/services/sxr/Android.mk",
    "vendor/qcom/proprietary/commonsys/openclwrapper/Android.mk",
    "vendor/qcom/proprietary/wlan/utils/qsh_wifi_test/Android.mk",
    "vendor/qcom/proprietary/wigig/debug-tools/shell_11ad/Android.mk",
    "vendor/qcom/proprietary/ts_firmware-noship/holi/Android.mk",
    "vendor/qcom/proprietary/vfw-vpu-20/Android.mk",
    "vendor/qcom/proprietary/camx-lib/test/nativetest/nativechitest/common/build/android/Android.mk",
    "vendor/qcom/proprietary/chi-cdk/core/chiframework/common/build/android/Android.mk",
    "vendor/qcom/proprietary/camx/camx-qsee/qsee-utils/build/android/Android.mk",
    "vendor/qcom/proprietary/camx/camx-qsee/qsee-aon/build/android/Android.mk",
    "vendor/qcom/proprietary/video/noship/hfi-test/driver/Android.mk",
    "vendor/qcom/proprietary/chi-cdk/api/generated/build/android/Android.mk",
    "vendor/qcom/opensource/camera-kernel/Android.mk",
    "vendor/qcom/opensource/video-driver/Android.mk",
    "vendor/qcom/proprietary/camx-lib-stats/system/statsalgo/aecxcontrol/build/android/Android.mk",
    "vendor/qcom/opensource/camera-kernel/include/uapi/Android.mk",
    "vendor/qcom/proprietary/camx/src/mapperutils/formatmapper/build/android/Android.mk",
    "vendor/qcom/proprietary/camx-lib-stats/system/statsalgo/af/build/android/Android.mk",
    "vendor/qcom/proprietary/chi-cdk/oem/qcom/chiusecase/build/android/Android.mk",
    "vendor/qcom/proprietary/camx-lib/system/statsalgo/awb/build/android/Android.mk",
    "vendor/qcom/proprietary/camx/src/core/build/android/Android.mk",
    "vendor/qcom/proprietary/camx/src/mapperutils/extformatutil/build/android/Android.mk",
    "vendor/qcom/opensource/mmrm-driver/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/Android.mk",
    "vendor/qcom/proprietary/common/create_files.mk",
    "device/qcom/common/base.mk",
    "device/qcom/msmnile_gvmq/BoardConfig.mk",
    "vendor/qcom/proprietary/display-tests/config/display-product-tests-system.mk",
    "device/qcom/gen4_gvm/BoardConfig.mk",
}

RM_WHITELIST = {
    "vendor/qcom/proprietary/graphics/t-bins/Android.mk",
    "vendor/qcom/proprietary/biometrics/fingerprint/QFingerprintService/Android.mk",
    "vendor/qcom/proprietary/common/scripts/Android.mk",
    "vendor/qcom/proprietary/graphics/s-bins/Android.mk",
    "vendor/qcom/proprietary/biometrics/fingerprint/QFPCalibration/Android.mk",
}

LOCAL_COPY_HEADERS_WHITELIST = {
    "vendor/qcom/proprietary/common/config/Android.mk",
    "vendor/qcom/proprietary/peripheral-manager/libpmclient/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_grease/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/msmnile_gvmq/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/gen4_gvm_cdccomm/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY22/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY33/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11-HWASAN/target/product/gen4_gvm/Android.mk",
    "vendor/qcom/proprietary/mm-hab/uhab/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/gen4_gvm/Android.mk",
    "vendor/qcom/proprietary/prebuilt_HY11/target/product/gen4_gvm_sdvcomm/Android.mk",
    "vendor/qcom/proprietary/sysprofiler/Android.mk",
    "vendor/qcom/proprietary/mm-bufferq/fence_queue/Android.mk",
    "vendor/qcom/proprietary/mm-bufferq/src/Android.mk",
}

DATETIME_WHITELIST = {
    "vendor/qcom/proprietary/qvr-vndr/tools/AnchorTest/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/tools/qvrdatalogger/Android.mk",
    "vendor/qcom/proprietary/qvr-vndr/tools/qvrdatacapture/Android.mk",
    "vendor/qcom/proprietary/camx-lib/system/mfnr/build/android/Android.mk",
    "vendor/qcom/proprietary/camx-lib/system/statsalgo/ubifocus/build/android/Android.mk",
    "vendor/qcom/proprietary/camx-lib/system/cac3/build/android/Android.mk",
}

TARGET_PRODUCT_WHITELIST = {
    "vendor/qcom/opensource/core-utils/build/AndroidBoardCommon.mk",
    "vendor/qcom/opensource/core-utils/build/QSSI_violators",
    "vendor/qcom/opensource/core-utils/build/build.sh",
    "vendor/qcom/opensource/core-utils/build/build_image_standalone.py",
}

RECURSIVE_WHITELIST = {
}

KERNEL_WHITELIST = {
}

OVERRIDE_WHITELIST = {
    "device/qcom/qssi/qssi.mk",
    "device/qcom/qssi/qssi_whitelist.mk",
    "device/qcom/qssi_au/qssi_au.mk",
    "device/qcom/qssi_au/qssi_au_whitelist.mk",
    "device/qcom/gen4_gvm/gen4_gvm.mk",
    "device/qcom/msmnile_gvmq/msmnile_gvmq.mk",
}

SOONG_WHITELIST = {
    "device/qcom/qssi/base.mk",
    "vendor/qcom/opensource/commonsys/display/config/display-product-commonsys.mk",
    "vendor/qcom/proprietary/commonsys-intf/bluetooth/bt-system-proprietary-product.mk",
    "vendor/qcom/proprietary/perf-core/configs/perf-core-product-vendor.mk",
    "vendor/qcom/proprietary/video/ship/video-vendor-modules.mk",
    "device/qcom/common/base.mk",
    "device/qcom/msmnile_gvmq/BoardConfig.mk",
    "hardware/qcom/display/config/display-product.mk",
    "vendor/qcom/opensource/audio-hal/primary-hal/configs/msmnile_au/msmnile_au.mk",
    "vendor/qcom/opensource/audio-hal/primary-hal/configs/msmsteppe_au/msmsteppe_au.mk",
    "device/qcom/gen4_gvm/BoardConfig.mk",
}

FOREACH_WHITELIST = {
    "device/qcom/common/utils.mk",
    "vendor/qcom/opensource/core-utils/build/utils.mk",
    "vendor/qcom/proprietary/common-noship/build/generate_extra_images_prop.mk",
    "vendor/qcom/proprietary/common/config/device-vendor-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/common/config/device-vendor-qssi.mk",
    "vendor/qcom/proprietary/perf-core/profiles.mk",
    "vendor/qcom/proprietary/video/ship/video-vendor-modules.mk",
    "vendor/qcom/proprietary/media-external/media-external-product.mk",
}

MACRO_WHITELIST = {
    "device/qcom/sepolicy/SEPolicy.mk",
    "vendor/qcom/opensource/commonsys/display/config/display-product-commonsys.mk",
    "vendor/qcom/proprietary/common-noship/etc/device-vendor-noship-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/common-noship/etc/device-vendor-noship.mk",
    "vendor/qcom/proprietary/common-noship/etc/device-vendor-qssi-noship.mk",
    "vendor/qcom/proprietary/common/config/device-vendor-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/common/config/device-vendor-qssi.mk",
    "vendor/qcom/proprietary/commonsys-intf/data/dpm_system_product_noship.mk",
    "vendor/qcom/proprietary/commonsys/android-perf-noship/config/perf-product-system-proprietary.mk",
    "vendor/qcom/proprietary/commonsys/telephony-build/build/telephony_system_product.mk",
    "vendor/qcom/proprietary/perf-core/configs/perf-core-product-vendor.mk",
    "vendor/qcom/opensource/bt-kernel/bt_kernel_vendor_board.mk",
    "vendor/qcom/opensource/dataipa/dataipa_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/datarmnet-ext/datarmnet_ext_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/datarmnet/datarmnet_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/dsp-kernel/dsp_kernel_board.mk",
    "vendor/qcom/opensource/graphics-kernel/gfx_kernel_board.mk",
    "vendor/qcom/opensource/platform-kernel/platform_kernel_board.mk",
    "vendor/qcom/opensource/platform-kernel/platform_kernel_product.mk",
    "vendor/qcom/opensource/video-driver/video_kernel_board.mk",
    "vendor/qcom/proprietary/dspservices_ship/dspservices_vendor_product.mk",
    "vendor/qcom/proprietary/dspservices_ship/remote_debug_agent_vendor_board.mk",
    "vendor/qcom/proprietary/gles/adreno_buildcfg/build/android/adreno-product.mk",
    "vendor/qcom/proprietary/kernel-scripts/kernel-platform/kernel-platform-board.mk",
    "vendor/qcom/proprietary/msmirqbalance/msm_irqbalance.mk",
    "vendor/qcom/proprietary/securemsm-internal/securemsm_internal_vendor_product.mk",
    "vendor/qcom/proprietary/video/binship/media-product.mk",
    "vendor/qcom/proprietary/video/ship/video-vendor-modules.mk",
    "device/qcom/common/base.mk",
    "device/qcom/sepolicy_vndr/SEPolicy.mk",
    "hardware/qcom/media/product.mk",
    "vendor/qcom/opensource/audio-hal-ar/primary-hal/configs/audio_ar_vendor_product.mk",
    "vendor/qcom/opensource/audio-hal/primary-hal/configs/audio_vendor_product.mk",
    "vendor/qcom/opensource/audio-kernel/audio_kernel_modules.mk",
    "vendor/qcom/opensource/audio-kernel/audio_kernel_product_board.mk",
    "vendor/qcom/opensource/bt-kernel/bt_kernel_vendor_board.mk",
    "vendor/qcom/opensource/data-ipa-cfg-mgr/ipacm_vendor_product.mk",
    "vendor/qcom/opensource/dataipa/dataipa_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/datarmnet-ext/datarmnet_ext_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/datarmnet/datarmnet_dlkm_vendor_board.mk",
    "vendor/qcom/opensource/display-drivers/display_driver_board.mk",
    "vendor/qcom/opensource/dsp-kernel/dsp_kernel_board.mk",
    "vendor/qcom/opensource/graphics-kernel/gfx_kernel_board.mk",
    "vendor/qcom/opensource/limits-noship/thermal-stats_board.mk",
    "vendor/qcom/opensource/limits-noship/thermal-stats_product.mk",
    "vendor/qcom/opensource/platform-kernel/platform_kernel_board.mk",
    "vendor/qcom/opensource/platform-kernel/platform_kernel_product.mk",
    "vendor/qcom/proprietary/cne/dpm-ship/dpm_vendor_product_noship.mk",
    "vendor/qcom/proprietary/data/data_prop_vendor_product.mk",
    "vendor/qcom/proprietary/dspservices_ship/dspservices_vendor_product.mk",
    "vendor/qcom/proprietary/dspservices_ship/remote_debug_agent_vendor_board.mk",
    "vendor/qcom/proprietary/gles/adreno_buildcfg/build/android/adreno-product.mk",
    "vendor/qcom/proprietary/ims-ship/ims_vendor_product_noship.mk",
    "vendor/qcom/proprietary/kernel-scripts/kernel-platform/kernel-platform-board.mk",
    "vendor/qcom/proprietary/media-external/media-external-product.mk",
    "vendor/qcom/proprietary/media-noship/media-noship-product.mk",
    "vendor/qcom/proprietary/media/media-product.mk",
    "vendor/qcom/proprietary/msmirqbalance/msm_irqbalance.mk",
    "vendor/qcom/proprietary/qcril-data-hal/datamodule/module/qcril-data-product.mk",
    "vendor/qcom/proprietary/qmi/qmi_data_vendor_product.mk",
    "vendor/qcom/proprietary/securemsm-internal/securemsm_internal_vendor_product.mk",
    "vendor/qcom/proprietary/vpp/config/vpp-vendor-board.mk",
}


