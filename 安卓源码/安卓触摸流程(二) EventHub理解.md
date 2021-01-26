Android 输入子系统名义上是由遍历系统多个层的事件管道组成。

在最低层(硬件物理层)，物理输入设备会生成描述状态更改（例如按键按压和触摸接触点）的信号。设备固件以某种方式编码和传输这些信号，例如向系统发送 USB HID 报告或在 I2C 总线上产生中断。

接着(驱动层),信号由 Linux 内核中的设备驱动程序解码,Linux 内核为许多标准的外围设备提供驱动程序，特别是那些符合 HID 协议的外围设备。

(标准通讯协议)设备驱动程序通过 Linux 输入协议将设备特定信号转换为标准输入事件格式。Linux 输入协议在 linux/input.h 内核头文件中定义了一组标准事件类型和代码。这样一来，内核之外的组件就不需要关注物理扫描代码、HID 用途、I2C 消息、GPIO 引脚等方面的详细信息。

(安卓事件类接入,c++)接下来，Android EventHub 组件通过打开与每个输入设备关联的 evdev 驱动程序从内核读取输入事件。然后，Android InputReader 组件根据设备类别解码输入事件，并生成 Android 输入事件流。在此过程中，Linux 输入协议事件代码将根据输入设备配置、键盘布局文件和各种映射表，转化为 Android 事件代码。

(安卓事件上层,java)最后，InputReader 将输入事件发送到 InputDispatcher，后者将这些事件转发到相应的窗口。

如何确定getevent中显示的设备event事件,使用的是哪个驱动,在设备中eg: ls -l /sys/class/input/event0/device/device

查看 frameworks\native\services\inputflinger\EventHub.cpp 代码
主要看 EventHub::EventHub(void) : 中inotify_init()和inotify_add_watch部分代码,这些是监听外设改变的函数方法.

在java层的inputManagerService中,也有 notifyInputDevicesChanged 监听所有输入设备改变的方法,可以在 filterInputEvent 中对事件进行过滤.

事件的分发还是在frameworks\native\services\inputflinger\InputDispatcher.cpp的 dispatchOnceInnerLocked 中处理,传到窗口,包含输入设备改变,键盘,触摸移动事件等.dispatchMotionLocked方法中DropReason代表丢弃事件,一般默认为不丢弃DROP_REASON_NOT_DROPPED.

    DROP_REASON_NOT_DROPPED
    当InputDispatcher在将输入事件放入派发队列前想DispatcherPolicy询问此事件派发策略时，DispatcherPolicy会将DROP_REASON_NOT_DROPPED策略去掉，没有这个派发策略的对象会被丢弃。

    DROP_REASON_POLICY
    某些输入事件具有系统级功能，例如HOME键、电源键、电话接听/挂断等被系统处理，因此DispatcherPolicy不希望这些事件被窗口捕获。

    DROP_REASON_APP_SWITCH
    dispatchOnceInnerLocked()函数说明了InputDispatcher的事件派发是串行的。因此在前一个事件派发成功并得到目标窗口的反馈之前，后续事件都会被其阻塞。当某个窗口因程序缺陷而无法响应输入事件时，用户可能会尝试使用HOME键退出这个程序。而由于派发的串行性，用户所操作的HOME键在其之前的输入事件成功派发给无响应的应用窗口之前无法获得派发机会，因此在ANR对话框弹出之前的5秒里，用户不得不面对无响应程序。为了解决这个问题，InputDispatcher为HOME键设置了限时派发的要求。当InputDispatcher的enqueueInboundEventLocked()函数发现HOME键被加入派发队列后，便要求HOME键之前的所有输入事件在0.5秒（APP_SWITCH_TIMEOUT常量定义）之前派发完毕，否则这些事件将被丢弃，是的HOME键至少能在0.5秒内得到响应。

    DROP_REASON_DISABLED
    因为InputDispatcher被禁用而使得事件被丢弃。InputDispatcher::setInputDispatchMode()函数可以是的InputDispatcher在禁用、冻结、正常三种状态之间进行切换。禁用状态会使得所有事件被丢弃，冻结将会使的dispatchOnceInnerLocked()函数直接返回从而停止派发工作。InputDispatcher的这三种状态的切换InputDispatcher的setInputDispatchMode,有Java层的IMS提供接口，由AMS和WMS根据需要进行设置。例如：当手机进入休眠状态时，InputDispatcher会被禁用，而屏幕旋转过程中，InputDispatcher会被暂时冻结。

    DROP_REASON_BLOCKED
    和APP_SWITCH原因类似，如果是因为一个窗口无法响应输入事件，可用户可能希望在其他窗口上进行点击，以尝试是否能得到响应。因为派发的串行性，这次尝试会以失败而高中。为此，当enqueueInboundEventLocked()发现有窗口正在阻塞派发的进行，并且新入队的触摸事件的目标是另外一个窗口，则将这个新事件保存到mNextUnblockedEvent中。随后的dispatchOnceInnerLocked()会将此事件之前的输入事件全部丢弃，使得用户在其他窗口上进行点击的尝试可以立即得到响应。

    DROP_REASON_STALE
    在dispatchOnceInnerLocked()函数准备对事件进行派发时，会先检查一下事件所携带的时间戳和当前时间的差距。如果事件过于陈旧（10秒以上，由常量STALE_EVENT_TIMEOUT所指定），则此事件需要被抛弃

**整体EventHub.cpp分析**:
EventHub的主要工作都是在getEvents函数中，InputReaderThread通过循环调用EventHub的getEvents()函数获取输入事件。在getEvents函数的循环中,又分为了多个操作:
1. 重新打开设备（mNeedToReopenDevices）

    //获取系统当前时间（native层的方法）。
    nsecs_t now = systemTime(SYSTEM_TIME_MONOTONIC);
    
    // Reopen input devices if needed.
    if (mNeedToReopenDevices) {//判断是否需要重新打开设备
        mNeedToReopenDevices = false;
    
        ALOGI("Reopening all input devices due to a configuration change.");
    
        closeAllDevicesLocked();//关闭、卸载所有设备
        mNeedToScanDevices = true; //下次扫描设备
        break; // return to the caller before we actually rescan
    }

由EventHub构造函数可知mNeedToReopenDevices为初始值false，第一次调用getEvents()时不会运行上面的代码块。其中调用了closeAllDevicesLocked()函数,通过closeDeviceLocked()函数卸载所有这些设备。

补充:
RawEvent结构体:

    struct RawEvent {
        nsecs_t when; //事件发生的时间店
        int32_t deviceId; //产生事件的设备Id
        int32_t type; // 事件类型:DEVICE_ADDED（输入设备插入）,DEVICE_REMOVED（输入设备被拔出）,FINISHED_DEVICE_SCAN（与Device相关的事件）,EV_KEY,EV_ABS,EV_REL
        int32_t code;
        int32_t value;
    };

2. DEVICE_REMOVED事件（mClosingDevices）

    //遍历mClosingDevices，生成DEVICE_REMOVED事件
    while (mClosingDevices) {
        Device* device = mClosingDevices;
        ALOGV("Reporting device closed: id=%d, name=%s\n",
                    device->id, device->path.string());
        mClosingDevices = device->next;
        event->when = now;//设置事件的时间戳
        event->deviceId = device->id == mBuiltInKeyboardId ? BUILT_IN_KEYBOARD_ID : device->id;	//设置事件对应的设备id
        event->type = DEVICE_REMOVED;   //设在事件类型DEVICE_REMOVED
        event += 1;	  		    //event指向下一个RawEvent对象
        delete device;		    //释放不需要的device
        mNeedToSendFinishedDeviceScan = true;
        //capacity为0时，表示buffer已满，则停止循环将事件返回给调用者（也就是InputReader），剩余的事件等下次getEvents调用
        if (--capacity == 0) {
            break;
        }
    }

同样的,第一次mClosingDevices初始值为0，所以刚开始调用getEvents()函数不会运行上述代码块。该块中主要是遍历mClosingDevices，生成DEVICE_REMOVED事件。

3. 扫描加载设备（mNeedToScanDevices）

    if (mNeedToScanDevices) {
        mNeedToScanDevices = false;
        scanDevicesLocked();//打开/dev/input下所有输入设备
        mNeedToSendFinishedDeviceScan = true;
    }

mNeedToScanDevices初始值为true，所以第一次getEvents会运行该代码块。该代码块主要工作：
1. mNeedToScanDevices赋值为false，避免重复扫描打开设备。
2. 调用scanDevicesLocked()，//打开/dev/input下所有输入设备。
3. mNeedToSendFinishedDeviceScan赋值为true，用于生成FINISHED_DEVICE_SCAN事件。
scanDevicesLocked()函数中调用了scanDirLocked()函数，scanDirLocked()函数遍历/dev/input文件夹下的所有设备节点，并分别执行openDeviceLocked(devname)，加载设备。

    status_t EventHub::openDeviceLocked(const char *devicePath) {
        //打开设备节点
        int fd = open(devicePath, O_RDWR | O_CLOEXEC);
        if(fd < 0) {
            ALOGE("could not open %s, %s\n", devicePath, strerror(errno));
            return -1;
        }
        
        //获取device的name、driver version、id等。
        。。。。。。
        //创建Device
        int32_t deviceId = mNextDeviceId++;
        Device* device = new Device(fd, deviceId, String8(devicePath), identifier);
        。。。。。。
        // Load the configuration file for the device. 加载配置信息
        loadConfigurationLocked(device);
        // Figure out the kinds of events the device reports.
        //设置device->classes，为设备分配类别（鼠标、键盘、触摸板等）
        
        // Register with epoll.将设备节点描述符的可读事件添加到Epoll中。
        struct epoll_event eventItem;
        memset(&eventItem, 0, sizeof(eventItem));
        eventItem.events = EPOLLIN;
        eventItem.data.u32 = deviceId;   //设备id
        if (epoll_ctl(mEpollFd, EPOLL_CTL_ADD, fd, &eventItem)) {
            ALOGE("Could not add device fd to epoll instance.  errno=%d", errno);
            delete device;
            return -1;
        }
        。。。。。
        //将device添加到mDevice中。
        addDeviceLocked(device);
        return 0;
    }

a ddDeviceLocked将Device添加到mDevice中，同时也会添加到mOpeningDevices中，用来生成DEVICE_ADDED事件，发送给InputReader。这之后就可以通过adb shell getEvents读取到设备产生的输入事件了。

4. DEVICE_ADDED事件（mOpeningDevices）

    while (mOpeningDevices != NULL) {
        Device* device = mOpeningDevices;
        ALOGD("Reporting device opened: id=%d, name=%s\n",
                    device->id, device->path.string());
        mOpeningDevices = device->next;
        event->when = now;		//设置事件端时间戳
        event->deviceId = device->id == mBuiltInKeyboardId ? 0 : device->id;
        event->type = DEVICE_ADDED;	    //设置事件类型DEVICE_ADDED
        event += 1;			    //event指向下一个RawEvent对象,用于填写下一次事件
        mNeedToSendFinishedDeviceScan = true;
        if (--capacity == 0) {	  //查看buffer是否已满
        break;
        }
    }

由于上面scanDevicesLocked时将/dev/input下的设备节点打开，并添加到mOpeningDevices中，所以会运行此代码块。这里主要是遍历mOpeningDevices，设置DEVICE_ADDED事件。

5. FINISHED_DEVICE_SCAN事件（mNeedToSendFinishedDeviceScan）

    if (mNeedToSendFinishedDeviceScan) {
        mNeedToSendFinishedDeviceScan = false;
        event->when = now;		  //设置事件端时间戳
        event->type = FINISHED_DEVICE_SCAN;	//设置事件类型FINISHED_DEVICE_SCAN
        event += 1;
        if (--capacity == 0) {
            break;
        }
    }

上述三个代码块(3,4,5)都会将mNeedToSendFinishedDeviceScan设为true，所以接着生成FINISHED_DEVICE_SCAN类型的事件。也就是当设备增删事件后，需要向getEvents()函数调用者发送FINISHED_DEVICE_SCAN事件。
由代码顺序可以知道DEVICE_REMOVED事件优先级最高、然后DEVICE_ADDED事件、FINISHED_DEVICE_SCAN事件最低。只有高优先级的事件处理完之后才会处理低优先级的事件。

6. iNotify事件、管道事件

    while (mPendingEventIndex < mPendingEventCount) {
        const struct epoll_event& eventItem = mPendingEventItems[mPendingEventIndex++];
        //EPOLL_ID_INOTIFY是EventHub初始化时，用来检测/dev/input下添加、删除设备事件。
        if (eventItem.data.u32 == EPOLL_ID_INOTIFY) {
            if (eventItem.events & EPOLLIN) {
            mPendingINotify = true;	//符合条件标记inotify事件待处理。
            } else {
            ALOGW("Received unexpected epoll event 0x%08x for INotify.", eventItem.events);
            }
            continue;//继续处理mPendingEventItems中的事件
        }
        。。。。。。
    }
    
        // readNotify() will modify the list of devices so this must be done after
        // processing all other events to ensure that we read all remaining events
        // before closing the devices.
    //判断是否有待处理的inotify事件。
        if (mPendingINotify && mPendingEventIndex >= mPendingEventCount) {
            mPendingINotify = false;
            readNotifyLocked();
            deviceChanged = true;
        }
    ALOGD("getEvents -----9 deviceChanged:%d",deviceChanged);
        // Report added or removed devices immediately.
        if (deviceChanged) {
            continue;//如果处理有inotify事件，处理后，进行下一次循环，生成设备增删事件。
        }
    。。。。。。

接着检查是否有未处理的设备事件。
mPendingINotify赋值为false，表示之后没有待处理的inotify事件。
readNotifyLocked() 处理inotify事件。
deviceChanged设置为true，进行下一次循环，生成设备增删事件。  

readNotifyLocked()函数:
1. 通过read()函数读取iNotify事件
2. 遍历所有的iNotify事件
3. 判断iNotify事件类型，IN_CREATE类型则加载设备，IN_DELETE类型则卸载设备。

    status_t EventHub::readNotifyLocked() {
        int res;
        char devname[PATH_MAX];
        char *filename;
        char event_buf[512];
        int event_size;
        int event_pos = 0;
        struct inotify_event *event;
    
        ALOGD("EventHub::readNotify nfd: %d\n", mINotifyFd);
        //从mINotifyFd读取inotify事件，存到event_buf中，
        res = read(mINotifyFd, event_buf, sizeof(event_buf));
        if(res < (int)sizeof(*event)) {
            if(errno == EINTR)
                return 0;
            ALOGW("could not get event, %s\n", strerror(errno));
            return -1;
        }
        //printf("got %d bytes of event information\n", res);
    
        strcpy(devname, DEVICE_PATH);
        filename = devname + strlen(devname);
        *filename++ = '/';
    
        while(res >= (int)sizeof(*event)) {
            event = (struct inotify_event *)(event_buf + event_pos);
            //printf("%d: %08x \"%s\"\n", event->wd, event->mask, event->len ? event->name : "");
            if(event->len) {
                strcpy(filename, event->name);
                if(event->mask & IN_CREATE) {//判断事件类型是否是IN_CREATE
                    openDeviceLocked(devname);	//加载对应设备
                } else {				//事件类型不是IN_CREATE，则是IN_DELETE
                    ALOGI("Removing device '%s' due to inotify event\n", devname);
                    closeDeviceByPathLocked(devname);  //卸载对应设备
                }
            }
        //移动到下一个事件。
            event_size = sizeof(*event) + event->len;
            res -= event_size;
            event_pos += event_size;  
        }
        return 0;
    }

7.输入事件
接着到输入事件了。根据输入事件，进行设置时间戳、id、类型、值等。返回给调用者InputReader。

    while (mPendingEventIndex < mPendingEventCount) {
        。。。。。
        //通过eventItem.data.u32 获取设备id
        ssize_t deviceIndex = mDevices.indexOfKey(eventItem.data.u32);
        if (deviceIndex < 0) {
            ALOGW("Received unexpected epoll event 0x%08x for unknown device id %d.",
                            eventItem.events, eventItem.data.u32);
        continue;
        }
        //从mDevices获取设备
        Device* device = mDevices.valueAt(deviceIndex);
                if (eventItem.events & EPOLLIN) {//epoll事件是EPOLLIN，可读，读取结果保存在readBuffer中，capacity是限制一次读取事件的个数
                int32_t readSize = read(device->fd, readBuffer,
                            sizeof(struct input_event) * capacity);
                    if (readSize == 0 || (readSize < 0 && errno == ENODEV)) {
                //读取有问题
                        // Device was removed before INotify noticed.
                        ALOGW("could not get event, removed? (fd: %d size: %d bufferSize: %d "
                                "capacity: %d errno: %d)\n",
                                device->fd, readSize, bufferSize, capacity, errno);
                        deviceChanged = true;
                        closeDeviceLocked(device);//关闭该设备
                    } else if (readSize < 0) {
                        if (errno != EAGAIN && errno != EINTR) {
                            ALOGW("could not get event (errno=%d)", errno);
                        }
                    } else if ((readSize % sizeof(struct input_event)) != 0) {
                        ALOGE("could not get event (wrong size: %d)", readSize);
                    } else {
                        int32_t deviceId = device->id == mBuiltInKeyboardId ? 0 : device->id;
    
                        size_t count = size_t(readSize) / sizeof(struct input_event);
                //遍历所有读取的输入事件
                        for (size_t i = 0; i < count; i++) {
                            struct input_event& iev = readBuffer[i];
    
                            if (iev.type == EV_MSC) {
                                if (iev.code == MSC_ANDROID_TIME_SEC) {
                                    device->timestampOverrideSec = iev.value;
                                    continue;
                                } else if (iev.code == MSC_ANDROID_TIME_USEC) {
                                    device->timestampOverrideUsec = iev.value;
                                    continue;
                                }
                            }
                            if (device->timestampOverrideSec || device->timestampOverrideUsec) {
                                iev.time.tv_sec = device->timestampOverrideSec;
                                iev.time.tv_usec = device->timestampOverrideUsec;
                                if (iev.type == EV_SYN && iev.code == SYN_REPORT) {
                                    device->timestampOverrideSec = 0;
                                    device->timestampOverrideUsec = 0;
                                }
                                ALOGV("applied override time %d.%06d",
                                        int(iev.time.tv_sec), int(iev.time.tv_usec));
                            }
    
    #ifdef HAVE_POSIX_CLOCKS
                //设置更准确的时间           
                            event->when = nsecs_t(iev.time.tv_sec) * 1000000000LL
                                    + nsecs_t(iev.time.tv_usec) * 1000LL;
                            ALOGV("event time %lld, now %lld", event->when, now);
    
                            if (event->when >= now + 10 * 1000000000LL) {
                                // Double-check.  Time may have moved on.
                                nsecs_t time = systemTime(SYSTEM_TIME_MONOTONIC);
                                if (event->when > time) {
                                    ALOGW("An input event from %s has a timestamp that appears to "
                                            "have been generated using the wrong clock source "
                                            "(expected CLOCK_MONOTONIC): "
                                            "event time %lld, current time %lld, call time %lld.  "
                                            "Using current time instead.",
                                            device->path.string(), event->when, time, now);
                                    event->when = time;
                                } else {
                                    ALOGV("Event time is ok but failed the fast path and required "
                                            "an extra call to systemTime: "
                                            "event time %lld, current time %lld, call time %lld.",
                                            event->when, time, now);
                                }
                            }
    #else
                            event->when = now;
    #endif
                //设置一些信息
                            event->deviceId = deviceId;
                            event->type = iev.type;
                            event->code = iev.code;
                            event->value = iev.value;
                            event += 1;  //移动到下一该可用元素
                            capacity -= 1;	//可用数量减少1
                        }
                        if (capacity == 0) {//buffer存满了，mPendingEventIndex至为-1，下一次循环处理未完的事件。
                            // The result buffer is full.  Reset the pending event index
                            // so we will try to read the device again on the next iteration.
                            mPendingEventIndex -= 1;
                            break;
                        }
                    }
                } else if (eventItem.events & EPOLLHUP) {//事件类型为挂起
                    ALOGI("Removing device %s due to epoll hang-up event.",
                            device->identifier.name.string());
                    deviceChanged = true;
                    closeDeviceLocked(device);	//卸载设备
                } else {
                    ALOGW("Received unexpected epoll event 0x%08x for device %s.",
                            eventItem.events, device->identifier.name.string());
                }
            }      
    。。。。。。
        rerutn event-buffer;//返回事件数量
    }

while循环后面是判断是否有inotify事件，wake事件。接着是获取epoll事件 。先获取到epoll事件，下次循环才会处理while循环。
通过mEpollFd描述符，获取epoll事件。保存在mPendingEventItems中，EPOLL_MAX_EVENTS（16）为限制一次最大读取事件次数，timeoutMillis为超时时间。