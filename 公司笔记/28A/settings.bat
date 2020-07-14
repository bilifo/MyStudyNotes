adb root
adb remount
adb shell rm system/b2g/webapps/settings.gaiamobile.org/application.zip
adb push \\192.168.1.245\panjunlong\28A\MSM8905.LF.1.4_BB\LINUX\android\gaia\profile\webapps\settings.gaiamobile.org\application.zip system/b2g/webapps/settings.gaiamobile.org/ 
pause
adb reboot

