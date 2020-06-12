adb root
adb remount
adb shell rm /system/framework/services.jar
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\system\framework\services.jar /system/framework/services.jar
pause
adb reboot
