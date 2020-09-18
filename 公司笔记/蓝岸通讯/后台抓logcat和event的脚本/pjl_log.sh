#抓logcat 和getevent 日志.
#sh pjl_log.sh 不加任何参数,两个都抓.
#sh pjl_log.sh kill,全部结束
#sh pjl_log.sh run logcat/event,指定单个抓取
#sh pjl_log.sh kill logcat/event,指定单个结束抓取
if [ "$#" -eq 0 ] ; then
	echo "save all"
	rm -rf /sdcard/event.txt
	getevent -tl > /sdcard/event.txt &
	logcat -c /sdcard/log.txt
	logcat -v time > /sdcard/log.txt &
else
	if [ "$1" == "run" ] ;then
		if [ "$2" == "logcat" ] ;then
			echo "save logcat"
			rm -rf /sdcard/event.txt
			getevent -tl > /sdcard/event.txt &
		elif [ "$2" == "event" ] ;then
			echo "save event"
			logcat -c /sdcard/log.txt
			logcat -v time > /sdcard/log.txt &
		fi
	elif [ "$1" == "kill" ] ;then
		if [ -z "$2" ] ;then
			echo "kill all"
			echo $(ls -l /sdcard/)
			pkill  logcat
			pkill getevent
		elif [ "$2" == "logcat" ] ;then
			echo "kill logcat"
			echo $(ls -l /sdcard/)
			pkill  logcat
		elif [ "$2" == "event" ] ;then
			echo "kill event"
			echo $(ls -l /sdcard/)
			pkill getevent
		fi
	else 
		echo "缺少参数"
	fi;
fi;
