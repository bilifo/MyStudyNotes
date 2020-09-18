adb root
adb remount
adb shell rm /product/priv-app/SystemUI/SystemUI.apk
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\product\priv-app\SystemUI\SystemUI.apk /product/priv-app/SystemUI/
pause
adb reboot

