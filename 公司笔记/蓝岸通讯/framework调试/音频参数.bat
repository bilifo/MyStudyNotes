adb root
adb remount
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\vendor\lib64\hw\audio.primary.sdm660.so /vendor/lib64/hw/audio.primary.sdm660.so
adb push \\192.168.1.245\panjunlong\sdm660_2\SDM660\LINUX\android\out\target\product\sdm660_64\vendor\lib\hw\audio.primary.sdm660.so /vendor/lib/hw/audio.primary.sdm660.so
pause
adb reboot
