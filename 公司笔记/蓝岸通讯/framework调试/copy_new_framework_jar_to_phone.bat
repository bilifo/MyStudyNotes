adb root
adb remount
adb shell rm /system/framework/services.jar
adb push Z:\QC26B\MSM8909W_LAW_3001\LINUX\android\out\target\product\msm8909w\system\framework\services.jar /system/framework/services.jar
pause
adb reboot
