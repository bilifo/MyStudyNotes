#!/bin/bash
source build/envsetup.sh
lunch QC26B-userdebug
mmm -j16 packages/apps/Settings/
ls -ls out/target/product/msm8909w/system/priv-app/Settings