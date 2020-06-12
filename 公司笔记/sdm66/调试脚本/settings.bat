adb root
adb remount
adb shell rm system/product/priv-app/Settings/Settings.apk
adb uninstall com.android.settings
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\product\priv-app\Settings\Settings.apk /system/product/priv-app/Settings/
pause
adb reboot