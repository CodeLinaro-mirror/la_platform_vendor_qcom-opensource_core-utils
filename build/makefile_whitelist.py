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
    "vendor/qcom/opensource/vienna/audio-hal/primary-hal/configs/qssi/qssi.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/common/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/China/ChinaMobile/products.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/China/ChinaTelecom/products.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/China/ChinaUnicom/products.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/China/CTA/products.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/Extension/products.mk",
    "vendor/qcom/proprietary/vienna/commonsys/qrdplus/sva/products.mk",
    "vendor/qcom/proprietary/vienna/commonsys/voiceui/products.mk",
    "vendor/qcom/proprietary/vienna/resource-overlay/overlay.mk",
    "vendor/qcom/proprietary/vienna/chi-cdk/product.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_ASAN/target/product/qssi/prebuilt.mk",
    "vendor/qcom/proprietary/vienna/android-perf/profiles.mk",
    "vendor/qcom/proprietary/vienna/mm-audio-internal/dolby/dax/device/dax2_common_hw.mk",
    "vendor/qcom/proprietary/vienna/qrdplus/InternalUseOnly/DuerosSDK/products.mk",
}

SHELL_WHITELIST = {
    "device/qcom/common/vienna/init/Android.mk",
    "device/qcom/sepolicy/vienna/SEPolicy.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/kalama/Android.mk",
    "vendor/qcom/opensource/vienna/touch-drivers/Android.mk",
    "vendor/qcom/proprietary/vienna/data-noship/qcril-data-utf/test/utf/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/ftm_flows/libwigig_ftm_flows/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/debug-tools/lib/FlashAcss/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/samples/apps/camera_test/Android.mk",
    "vendor/qcom/opensource/vienna/eva-kernel/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/tools/sensors_calibration/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/service/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/samples/plugins/eyetracking/Android.mk",
    "vendor/qcom/opensource/vienna/wlan/utils/sigma-dut/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/sm8150/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/sensing/sensingdaemon/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/samples/apps/imu_test/Android.mk",
    "vendor/qcom/proprietary/vienna/Innopath/FOTA/MobileUpdateClient/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/sm6125/Android.mk",
    "vendor/qcom/proprietary/vienna/ml/nnhal/qnn-gpu/QNN/GPU/OpPackage/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/debug-tools/lib/WlctPciAcss/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/tools/qvrdatalogger/Android.mk",
    "device/qcom/common/vienna/init/Android.mk",
    "vendor/qcom/proprietary/vienna/ml/nnhal/qnn-gpu/QNN/GPU/Backend/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/bengal/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/ftm_flows/ftm_flows_test/Android.mk",
    "vendor/qcom/proprietary/vienna/wlan/utils/halproxydaemon/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/common/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/debug-tools/lib/utils/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/services/2dframework/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig-noship/location/libaoa/Android.mk",
    "vendor/qcom/proprietary/vienna/ac_policy-noship/Android.mk",
    "vendor/qcom/opensource/vienna/wlan/qcacld-3.0/Android.mk",
    "vendor/qcom/proprietary/vienna/securemsm-internal/isdbtmm/test/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/lahaina/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/debug-tools/host_manager_11ad/Android.mk",
    "vendor/qcom/proprietary/vienna/platform-boost/platform_boost_hal/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/services/sxr/Android.mk",
    "vendor/qcom/proprietary/vienna/commonsys/openclwrapper/Android.mk",
    "vendor/qcom/proprietary/vienna/wlan/utils/qsh_wifi_test/Android.mk",
    "vendor/qcom/proprietary/vienna/wigig/debug-tools/shell_11ad/Android.mk",
    "vendor/qcom/proprietary/vienna/ts_firmware-noship/holi/Android.mk",
    "vendor/qcom/proprietary/vienna/vfw-vpu-20/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib/test/nativetest/nativechitest/common/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/chi-cdk/core/chiframework/common/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx/camx-qsee/qsee-utils/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx/camx-qsee/qsee-aon/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/video/noship/hfi-test/driver/Android.mk",
    "vendor/qcom/proprietary/vienna/chi-cdk/api/generated/build/android/Android.mk",
    "vendor/qcom/opensource/vienna/camera-kernel/Android.mk",
    "vendor/qcom/opensource/vienna/video-driver/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib-stats/system/statsalgo/aecxcontrol/build/android/Android.mk",
    "vendor/qcom/opensource/vienna/camera-kernel/include/uapi/Android.mk",
    "vendor/qcom/proprietary/vienna/camx/src/mapperutils/formatmapper/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib-stats/system/statsalgo/af/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/chi-cdk/oem/qcom/chiusecase/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib/system/statsalgo/awb/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx/src/core/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx/src/mapperutils/extformatutil/build/android/Android.mk",
    "vendor/qcom/opensource/vienna/mmrm-driver/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/Android.mk",
    "vendor/qcom/proprietary/vienna/common/create_files.mk",
    "vendor/qcom/proprietary/vienna/common/vienna/copy_files.mk",
}

RM_WHITELIST = {
    "vendor/qcom/proprietary/vienna/graphics/t-bins/Android.mk",
    "vendor/qcom/proprietary/vienna/biometrics/fingerprint/QFingerprintService/Android.mk",
    "vendor/qcom/proprietary/vienna/common/scripts/Android.mk",
    "vendor/qcom/proprietary/vienna/graphics/s-bins/Android.mk",
    "vendor/qcom/proprietary/vienna/biometrics/fingerprint/QFPCalibration/Android.mk",
}

LOCAL_COPY_HEADERS_WHITELIST = {
    "vendor/qcom/proprietary/vienna/common/config/Android.mk",
    "vendor/qcom/proprietary/vienna/peripheral-manager/libpmclient/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_grease/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY11/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY22/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/target/product/qssi/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/target/product/taro/Android.mk",
    "vendor/qcom/proprietary/vienna/prebuilt_HY33/Android.mk",
}

DATETIME_WHITELIST = {
    "vendor/qcom/proprietary/vienna/qvr-vndr/tools/AnchorTest/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/tools/qvrdatalogger/Android.mk",
    "vendor/qcom/proprietary/vienna/qvr-vndr/tools/qvrdatacapture/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib/system/mfnr/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib/system/statsalgo/ubifocus/build/android/Android.mk",
    "vendor/qcom/proprietary/vienna/camx-lib/system/cac3/build/android/Android.mk",
}

TARGET_PRODUCT_WHITELIST = {
    "vendor/qcom/opensource/vienna/core-utils/build/AndroidBoardCommon.mk",
    "vendor/qcom/opensource/vienna/core-utils/build/QSSI_violators",
    "vendor/qcom/opensource/vienna/core-utils/build/build.sh",
    "vendor/qcom/opensource/vienna/core-utils/build/build_image_standalone.py",
}

RECURSIVE_WHITELIST = {
}

KERNEL_WHITELIST = {
}

OVERRIDE_WHITELIST = {
    "device/qcom/qssi/qssi.mk",
    "device/qcom/qssi/qssi_whitelist.mk",
}

SOONG_WHITELIST = {
    "device/qcom/qssi/base.mk",
    "vendor/qcom/opensource/vienna/commonsys/display/config/display-product-commonsys.mk",
    "vendor/qcom/proprietary/vienna/commonsys-intf/bluetooth/bt-system-proprietary-product.mk",
}

FOREACH_WHITELIST = {
    "vendor/qcom/opensource/vienna/core-utils/build/utils.mk",
    "vendor/qcom/proprietary/vienna/common-noship/build/generate_extra_images_prop.mk",
    "vendor/qcom/proprietary/vienna/common/config/device-vendor-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/vienna/common/config/device-vendor-qssi.mk",
}

MACRO_WHITELIST = {
    "device/qcom/sepolicy/vienna/SEPolicy.mk",
    "vendor/qcom/opensource/vienna/commonsys/display/config/display-product-commonsys.mk",
    "vendor/qcom/proprietary/vienna/common-noship/etc/device-vendor-noship-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/vienna/common-noship/etc/device-vendor-noship.mk",
    "vendor/qcom/proprietary/vienna/common-noship/etc/device-vendor-qssi-noship.mk",
    "vendor/qcom/proprietary/vienna/common/config/device-vendor-SDM845-pureAOSP.mk",
    "vendor/qcom/proprietary/vienna/common/config/device-vendor-qssi.mk",
    "vendor/qcom/proprietary/vienna/commonsys-intf/data/dpm_system_product_noship.mk",
    "vendor/qcom/proprietary/vienna/commonsys/android-perf-noship/config/perf-product-system-proprietary.mk",
    "vendor/qcom/proprietary/vienna/commonsys/telephony-build/build/telephony_system_product.mk",
}


