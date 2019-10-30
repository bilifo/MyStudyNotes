adb root
adb remount
adb shell rm system/priv-app/Settings/Settings.apk
adb uninstall com.android.settings
adb push Z:\QC26B\MSM8909W_LAW_3001\LINUX\android\out\target\product\msm8909w\system\priv-app\Settings\Settings.apk /system/priv-app/Settings/
pause
adb reboot
