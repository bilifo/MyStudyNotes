#!/bin/bash
source build/envsetup.sh
lunch QC26B-userdebug
mmm -j16 frameworks/base/services/

ls -ls out/target/product/msm8909w/system/framework/services.jar