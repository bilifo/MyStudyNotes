adb root
adb remount
adb shell rm /product/priv-app/SearchLauncherQRef/SearchLauncherQRef.apk
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\product\priv-app\Launcher3\Launcher3.apk /product/priv-app/SearchLauncherQRef/SearchLauncherQRef.apk
pause
adb reboot

