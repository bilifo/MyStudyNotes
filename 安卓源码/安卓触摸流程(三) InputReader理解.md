Android 输入子系统名义上是由遍历系统多个层的事件管道组成。

在最低层(硬件物理层)，物理输入设备会生成描述状态更改（例如按键按压和触摸接触点）的信号。设备固件以某种方式编码和传输这些信号，例如向系统发送 USB HID 报告或在 I2C 总线上产生中断。

接着(驱动层),信号由 Linux 内核中的设备驱动程序解码,Linux 内核为许多标准的外围设备提供驱动程序，特别是那些符合 HID 协议的外围设备。

(标准通讯协议)设备驱动程序通过 Linux 输入协议将设备特定信号转换为标准输入事件格式。Linux 输入协议在 linux/input.h 内核头文件中定义了一组标准事件类型和代码。这样一来，内核之外的组件就不需要关注物理扫描代码、HID 用途、I2C 消息、GPIO 引脚等方面的详细信息。

(安卓事件类接入,c++)接下来，Android EventHub 组件通过打开与每个输入设备关联的 evdev 驱动程序从内核读取输入事件。然后，Android InputReader 组件根据设备类别解码输入事件，并生成 Android 输入事件流。在此过程中，Linux 输入协议事件代码将根据输入设备配置、键盘布局文件和各种映射表，转化为 Android 事件代码。

(安卓事件上层,java)最后，InputReader 将输入事件发送到 InputDispatcher ，后者将这些事件转发到相应的窗口。

InputReader主要工作是从EventHub读取事件、进行加工、将加工好的事件发送到InputDispatcher。
查看 frameworks/native/services/inputflinger/InputReader.cpp 代码

InputReader主要是将EventHub中的input_event转换成具体的EventEntry,并添加到InputDispatcher的
mInboundQueue里,然后唤醒InputDispacher线程。InputDispacher线程有自己的Looper，被唤醒后
会执行dispatchOnce方法，InputDispatcher处理的事件主要分两种：一种是command命令
（Command是mPolicy处理的具体事务，这个mPolicy就是NativeInputManager，最终对应的上层是
InputManagerService），一种是input event。每次dispatchOnce，会优先执行前者。

由于安卓10为了支持全面屏,优化主界面的手势导航速度,使原来写在SystemUI中的系统部分手势,迁移到了Launcher3中.

主要实现目录:
packages/apps/Launcher3/quickstep/recents_ui_overrides/src/com/android/launcher3/uioverrides/touchcontrollers/TaskViewTouchController,java
最近任务的处理类,这个类里面处理了最近任务的左右移,和all app界面的上下移

frameworks\base\services\core\java\com\android\server\wm\WindowManagerService.java
显示鼠标光标和轨迹.鼠标按下事件不是这里处理,而是被加入到InputManagerInternal中,由各自app的view处理

    public boolean injectInputAfterTransactionsApplied(InputEvent ev, int mode) {
        boolean isDown;
        boolean isUp;

        if (ev instanceof KeyEvent) {//按键事件
            KeyEvent keyEvent = (KeyEvent) ev;
            isDown = keyEvent.getAction() == KeyEvent.ACTION_DOWN;
            isUp = keyEvent.getAction() == KeyEvent.ACTION_UP;
        } else {//运动事件
            MotionEvent motionEvent = (MotionEvent) ev;
            isDown = motionEvent.getAction() == MotionEvent.ACTION_DOWN;
            isUp = motionEvent.getAction() == MotionEvent.ACTION_UP;
        }
        final boolean isMouseEvent = ev.getSource() == InputDevice.SOURCE_MOUSE;//鼠标也归类为motion
        // For ACTION_DOWN, syncInputTransactions before injecting input.
        // For all mouse events, also sync before injecting.
        // For ACTION_UP, sync after injecting.
        if (isDown || isMouseEvent) {
            syncInputTransactions();
        }
        final boolean result =
                LocalServices.getService(InputManagerInternal.class).injectInputEvent(ev, mode);
        if (isUp) {
            syncInputTransactions();
        }
        return result;
    }

构造方法:

    InputReader::InputReader(const sp<EventHubInterface>& eventHub,
            const sp<InputReaderPolicyInterface>& policy,
            const sp<InputListenerInterface>& listener) :
            mContext(this), mEventHub(eventHub), mPolicy(policy),
            mNextSequenceNum(1), mGlobalMetaState(0), mGeneration(1),
            mDisableVirtualKeysTimeout(LLONG_MIN), mNextTimeout(LLONG_MAX),
            mConfigurationChangesToRefresh(0) {
        mQueuedListener = new QueuedInputListener(listener);

        { // acquire lock
            AutoMutex _l(mLock);
            refreshConfigurationLocked(0);
            updateGlobalMetaStateLocked();
        } // release lock
    }

初始化必要的变量，mEventHub对应EventHub对象，mPolicy对应NativeInputManager对象，mGlobalMetaState表示控制键的状态，mGeneration表示输入设备的状态，mQueuedListener用来将加工后的按键事件传到InputDispatcher。这里的mContext,mEventHub等都是隐式创建,他们的声明在InputDispatcher.h中

这里插一句,从InputManagerService的start() 层层调用 最后调用到 InputManager的start()中。

    result = mReaderThread->run("InputReader", PRIORITY_URGENT_DISPLAY);
InputReaderThread开始运行，以下是InputReaderThread的线程循环，返回true则循环不断的调用threadLoop()方法，返回false则退出循环。

    bool InputReaderThread::threadLoop() {
        mReader->loopOnce();
        return true;
    }

该线程中会循环不断的执行mReader->loopOnce();即InputReader中的loopOnce方法

    void InputReader::loopOnce() {
        int32_t oldGeneration;
        int32_t timeoutMillis;
        bool inputDevicesChanged = false;
        Vector<InputDeviceInfo> inputDevices;
        { // acquire lock
            AutoMutex _l(mLock);
    
            oldGeneration = mGeneration;
            timeoutMillis = -1;
        //查看InputReader配置是否修改，如界面大小、方向、键盘布局重新加载、指针速度改变等
            uint32_t changes = mConfigurationChangesToRefresh;
            if (changes) {
                mConfigurationChangesToRefresh = 0;
                timeoutMillis = 0;
                refreshConfigurationLocked(changes); //刷新配置
            } else if (mNextTimeout != LLONG_MAX) {
                nsecs_t now = systemTime(SYSTEM_TIME_MONOTONIC);
                timeoutMillis = toMillisecondTimeoutDelay(now, mNextTimeout);
            }
        } // release lock
        //获取输入事件、设备增删事件，count为事件数量。
        size_t count = mEventHub->getEvents(timeoutMillis, mEventBuffer, EVENT_BUFFER_SIZE);
        { // acquire lock
            AutoMutex _l(mLock);
            mReaderIsAliveCondition.broadcast();
    
            if (count) {//如果有读到事件（count大于0）,处理事件
            //遍历所有的事件，分别进行处理。其处理的事件类型分为四种：原始输入事件、设备加载事件、设备卸载事件及FINISHED_DEVICE_SCAN事件。
                processEventsLocked(mEventBuffer, count);
            }
    
            if (mNextTimeout != LLONG_MAX) {
                nsecs_t now = systemTime(SYSTEM_TIME_MONOTONIC);
                if (now >= mNextTimeout) {
                    mNextTimeout = LLONG_MAX;
                    timeoutExpiredLocked(now);
                }
            }
    
            if (oldGeneration != mGeneration) {
                inputDevicesChanged = true;
                getInputDevicesLocked(inputDevices);
            }
        } // release lock
    
        // 发送一个消息，该消息描述已更改的输入设备。
        if (inputDevicesChanged) {
            mPolicy->notifyInputDevicesChanged(inputDevices);
        }
        mQueuedListener->flush();  //将事件传到InputDispatcher.
    }

loopOnce()函数先复制mConfigurationChangesToRefresh的值，看mConfigurationChangesToRefresh是否有更改,如果mConfigurationChangesToRefresh有修改则刷新Configuration（refreshConfigurationLocked()），timeoutMillis设置为0.
然后通过EventHub->getEvents()，获取输入事件和设备增删事件，count为读取的事件数量，mEventBuffer存储着事件。由上一篇文章可知getEvents()是阻塞的，只有当有事件或者被wake才会被唤醒向下执行。  

接下来我们说下4种事件:
* 设备加载事件

    void InputReader::addDeviceLocked(nsecs_t when, int32_t deviceId) {
        // 通过设备id（deviceId）获取mDevices中该设备下标，从而判断是否包含该设备。
        ssize_t deviceIndex = mDevices.indexOfKey(deviceId);
        //查看mDevices是否包含该设备，-2表示没有包含, 大于等于0表示包含。
        if (deviceIndex >= 0) {
            ALOGW("Ignoring spurious device added event for deviceId %d.", deviceId);
            return;
        }
        //获取设备厂商信息
        InputDeviceIdentifier identifier = mEventHub->getDeviceIdentifier(deviceId);
        //获取设备类型
        uint32_t classes = mEventHub->getDeviceClasses(deviceId);
        //创建设备inputDevice。
        InputDevice* device = createDeviceLocked(deviceId, identifier, classes);
        device->configure(when, &mConfig, 0);
        device->reset(when);
    
        if (device->isIgnored()) {
            ALOGI("Device added: id=%d, name='%s' (ignored non-input device)", deviceId,
                    identifier.name.string());
        } else {
            ALOGI("Device added: id=%d, name='%s', sources=0x%08x", deviceId,
                    identifier.name.string(), device->getSources());
        }
        //将设备添加到mDevices字典中。
        mDevices.add(deviceId, device);
        bumpGenerationLocked();
    }

addDeviceLocked()函数中主要通过设备厂商信息、类型来创建InputDevice，配置InputDevice，并将device添加到mDevices中。其中createDeviceLocked()函数用来创建InputDevice对象，并根据设备类别设置不同的mapper,如（INPUT_DEVICE_CLASS_SWITCH对应SwitchInputMapper）。

* 设备卸载事件

    void InputReader::removeDeviceLocked(nsecs_t when, int32_t deviceId) {
        InputDevice* device = NULL;
        ssize_t deviceIndex = mDevices.indexOfKey(deviceId);
        if (deviceIndex < 0) {
            ALOGW("Ignoring spurious device removed event for deviceId %d.", deviceId);
            return;
        }
    
        device = mDevices.valueAt(deviceIndex);
        mDevices.removeItemsAt(deviceIndex, 1);//从mDevices移除对应的设备
        bumpGenerationLocked();
    
        if (device->isIgnored()) {
            ALOGI("Device removed: id=%d, name='%s' (ignored non-input device)",
                    device->getId(), device->getName().string());
        } else {
            ALOGI("Device removed: id=%d, name='%s', sources=0x%08x",
                    device->getId(), device->getName().string(), device->getSources());
        }
    
        device->reset(when);//设备重置
        delete device; //释放。
    }

将其从mDevices中移除该设备。

* 完成扫描事件

    void InputReader::handleConfigurationChangedLocked(nsecs_t when) {
        // Reset global meta state because it depends on the list of all configured devices.
        updateGlobalMetaStateLocked();
    
        // 将事件封装成NotifyConfigurationChangedArgs对象
        NotifyConfigurationChangedArgs args(when);
        //将该对象放到mQueuedListener队列中。mQueuedListener->flush()时传到InputDispstcher线程
        mQueuedListener->notifyConfigurationChanged(&args);
    }

在设备加载事件或设备卸载事件后会跟着FINISHED_DEVICE_SCAN，用来表示设备加载事件或设备卸载事件已完毕。

* 原始输入事件(即设备自身产生的事件)
type < EventHubInterface::FIRST_SYNTHETIC_EVENT，当满足该条件时表示原始输入事件，对同一设备的原始输入事件调用processEventsForDeviceLocked()函数进行处理。

    void InputReader::processEventsForDeviceLocked(int32_t deviceId,
            const RawEvent* rawEvents, size_t count) {
        //通过设备id获取mDevices中存储的下标
        ssize_t deviceIndex = mDevices.indexOfKey(deviceId);
        if (deviceIndex < 0) {  //没有对应设备
            ALOGW("Discarding event for unknown deviceId %d.", deviceId);
            return;
        }
        //通过下标从mDevices取出对应的设备。
        InputDevice* device = mDevices.valueAt(deviceIndex);
        if (device->isIgnored()) {
            //ALOGD("Discarding event for ignored deviceId %d.", deviceId);
            return;
        }
        //设备处理事件
        device->process(rawEvents, count);
    }

通过设备id从字典中获取InputDevice，调用InputDevice->process()函数进行处理

    void InputDevice::process(const RawEvent* rawEvents, size_t count) {
        size_t numMappers = mMappers.size();
        for (const RawEvent* rawEvent = rawEvents; count--; rawEvent++) {
    
            if (mDropUntilNextSync) {
                ......
            } else {
                for (size_t i = 0; i < numMappers; i++) {
                    InputMapper* mapper = mMappers[i];
                    mapper->process(rawEvent);
                }
            }
        }
    }

该函数中主要遍历所有的事件，将各事件交给InputMapper处理。  
之前createDeviceLocked()函数创建InputDevice的时候，会对InputDevice对象调用addMapper，添加到字典mMappers（一个InputDevice可能有一个或多个mapper，主要取决与设备类型）。InputDevice不知道、也不管哪个InputMapper可以处理这些事件，只需要让所有的InputMapper都去加工这些事件，InputMapper中会对事件进行判断是否是自己该处理的事件，如果不是则什么都不做，如果是则进行相应处理。  
InputMapper有多个子类：SwitchInputMapper()、VibratorInputMapper(震动器)、KeyboardInputMapper(键盘)、CursorInputMapper(鼠标,类似光标的设备)、MultiTouchInputMapper(触摸屏和触控板)、SingleTouchInputMapper、RotaryEncoderInputMapper()、ExternalStylusInputMapper(触控笔)、JoystickInputMapper(游戏杆)等。

先说*KeyboardInputMapper*(也在InputReader.cpp中)

    void KeyboardInputMapper::process(const RawEvent* rawEvent) {
        switch (rawEvent->type) {
        case EV_KEY: { //事件类型：按键类型
            int32_t scanCode = rawEvent->code;
            int32_t usageCode = mCurrentHidUsage;
            mCurrentHidUsage = 0;
        //排除鼠标按键，鼠标按键由CursorInputMapper处理。
            if (isKeyboardOrGamepadKey(scanCode)) {
                int32_t keyCode;
                uint32_t flags;
            //通过EventHub调用mapKey()函数，将扫描码映射出键值。scanCode为扫描码，keyCode用来存键值。
                if (getEventHub()->mapKey(getDeviceId(), scanCode, usageCode, &keyCode, &flags)) {		//映射失败
                    keyCode = AKEYCODE_UNKNOWN;
                    flags = 0;
                }
                processKey(rawEvent->when, rawEvent->value != 0, keyCode, scanCode, flags);
            }
            break;
        }
        //其他类别事件，好像没有做什么。
        case EV_MSC: {
            if (rawEvent->code == MSC_SCAN) {
                mCurrentHidUsage = rawEvent->value;
            }
            break;
        }
        case EV_SYN: {
            if (rawEvent->code == SYN_REPORT) {
                mCurrentHidUsage = 0;
            }
        }
        }
    }

getEventHub()->mapKey()用来将扫描码映射成虚拟键值。如何映射呢？
EventHub创建设备、加载设备时调用openDeviceLocked函数，其中如何设备类型为INPUT_DEVICE_CLASS_KEYBOARD或INPUT_DEVICE_CLASS_JOYSTICK时，会调用EventHub::loadKeyMapLocked函数为此设备加载配置文件，键盘配置文件路径/system/usr/input/或/system/usr/keylayout，不同设备可能会稍有差别。该目录下的文件后缀都是.kl，其中一个处理实体按键的文件内容如下：

    key 116   POWER      WAKE
    key 102   HOME       WAKE
    key 158   BACK       WAKE
    key 212   CAMERA     WAKE
    key 114   VOLUME_DOWN
    key 30    A
    ......

第一列关键字key，第二列表示扫描码，第三列表示虚拟键值的名称，第四列表示此按键的功能。
frameworks/base/include/androidfw/KeycodeLabels.h中数组存储着个虚拟键名和键值。
loadKeyMapLocked函数将虚拟键值的名转换为键值存在结构体中，以扫描码为键。通过mapKey()函数可以获取到扫描码对应的键值和flag。
电源键扫描码为116，键值为26，flags为1。  

接着看processKey()函数对事件进行加工

    void KeyboardInputMapper::processKey(nsecs_t when, bool down, int32_t keyCode,
            int32_t scanCode, uint32_t policyFlags) {
        //按键 按下	
        if (down) {
            // 根据屏幕方向，转换键值
            if (mParameters.orientationAware && mParameters.hasAssociatedDisplay) {
                keyCode = rotateKeyCode(keyCode, mOrientation);
            }
        
            //KeyboardInputMapper中的mKeyDown结集合用来存储KeyDown结构体，记录按下的键。
            ssize_t keyDownIndex = findKeyDown(scanCode);
            if (keyDownIndex >= 0) { //表示该扫描码之前被按下，也就是现在是重复按下。
            //确保多次按下键值一致。
                keyCode = mKeyDowns.itemAt(keyDownIndex).keyCode;
            } else {
                // POLICY_FLAG_VIRTUAL 不做处理
                if ((policyFlags & POLICY_FLAG_VIRTUAL)
                        && mContext->shouldDropVirtualKey(when,
                                getDevice(), keyCode, scanCode)) {
                    return;
                }
            //通过扫描码和键值生成keyDown对象，添加到mKeyDowns集合中。
                mKeyDowns.push();
                KeyDown& keyDown = mKeyDowns.editTop();
                keyDown.keyCode = keyCode;
                keyDown.scanCode = scanCode;
            }
            mDownTime = when;
        } else {
            // Remove key down.
            ssize_t keyDownIndex = findKeyDown(scanCode);
            if (keyDownIndex >= 0) {
                // mKeyDowns移除抬起的键
                keyCode = mKeyDowns.itemAt(keyDownIndex).keyCode;
                mKeyDowns.removeAt(size_t(keyDownIndex));
            } else {
                //如果按键没有被按下就只被抬起，则事件忽略不处理。
                return;
            }
        }
    
        bool metaStateChanged = false;
        //控制键的状态、控制键包括alt、shift、ctrl、meta、NumLock、ScrollLock、CapsLock等。
        int32_t oldMetaState = mMetaState;
        //检查是否是控制键，并返回控制键状态。
        int32_t newMetaState = updateMetaState(keyCode, down, oldMetaState);
        if (oldMetaState != newMetaState) {//与之前状态对比，判断控制键状态是否更改
            mMetaState = newMetaState;
            metaStateChanged = true;
            updateLedState(false);
        }
    
        nsecs_t downTime = mDownTime;
    
        if (down && getDevice()->isExternal()
                && !(policyFlags & (POLICY_FLAG_WAKE | POLICY_FLAG_WAKE_DROPPED))) {
        
            policyFlags |= POLICY_FLAG_WAKE_DROPPED;
        }
    
        if (metaStateChanged) {//更新控制状态
            getContext()->updateGlobalMetaState();
        }
    
        if (down && !isMetaKey(keyCode)) {
            getContext()->fadePointer();
        }
        //按键信息封装到NotifyKeyArgs对象中。
        NotifyKeyArgs args(when, getDeviceId(), mSource, policyFlags,
                down ? AKEY_EVENT_ACTION_DOWN : AKEY_EVENT_ACTION_UP,
                AKEY_EVENT_FLAG_FROM_SYSTEM, keyCode, scanCode, newMetaState, downTime);
        getListener()->notifyKey(&args);
    }

processKey()函数主要管理mKeyDowns，将按下的按钮保存在mKeyDowns中，抬起的从中移除。
。还有控制键状态的更新。最后将按键事件封装在NotifyKeyArgs对象中。之后就是向InputDispatcher中发送。

getListener() -> InputListenerInterface* InputReader::ContextImpl::getListener() 该函数返回的对象是InputReader构造函数中的mQueuedListener，调用其notifyKey()函数并不会马上发送到InputDispatcher中，而是在InputReader::loopOnce()中调用mQueuedListener->flush()，这才会将这次所有已加工的事件发送到InputDispatcher中。

接着说*TouchInputMapper*触摸事件

    void TouchInputMapper::process(const RawEvent* rawEvent) {
        mCursorButtonAccumulator.process(rawEvent);
        mCursorScrollAccumulator.process(rawEvent);
        mTouchButtonAccumulator.process(rawEvent);

        if (rawEvent->type == EV_SYN && rawEvent->code == SYN_REPORT) {
            reportEventForStatistics(rawEvent->when);
            sync(rawEvent->when);
        }
    }