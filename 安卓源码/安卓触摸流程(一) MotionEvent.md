Android 将所有的输入事件都放在了 MotionEvent 中,在安卓最早的几个版本中已经将MotionEvent改动完毕

MotionEvent 负责集中处理所有类型设备的输入事件

输入事件流程:
物理硬件层---(电平变化)--->底层驱动---(linux标准通讯协议)--->HAL层EventHub--->InputReader--->InputDispatcher

**事件类型**

    public static final int ACTION_DOWN             = 0;//第一个手指按下时
    public static final int ACTION_UP               = 1;
    public static final int ACTION_MOVE             = 2;//按住一点在屏幕上移动
    public static final int ACTION_CANCEL           = 3;//当前的手势被取消了，并且再也不会接收到后续的触摸事件
    public static final int ACTION_OUTSIDE          = 4;//表示用户触碰超出了正常的UI边界.
    public static final int ACTION_POINTER_DOWN     = 5;//代表用户又使用一个手指触摸到屏幕上
    public static final int ACTION_POINTER_UP       = 6;

**事件坐标**

    event.getX(); //触摸点相对于View左上角为原点坐标系的X坐标
    event.getY(); //触摸点相对于View左上角为原点坐标系的Y坐标
    event.getRawX(); //触摸点相对于屏幕左上角为原点坐标系的X坐标
    event.getRawY(); //触摸点相对于屏幕左上角为原点坐标系的Y坐标

单点触控:
ACTION_DOWN--->ACTION_MOVE--->ACTION_UP  

多点触控:
ACTION_DOWN--->ACTION_POINTER_DOWN--->ACTION_MOVE--->ACTION_POINTER_UP--->ACTION_UP  

安卓上层的系统服务InputManagerService,源码在路径：frameworks/base/services/core/java/com/android/server/input/InputManagerService.java    

**服务的启动**
在SystemServer.java的ServerThread中启动.
创建InputManagerService对象  

    @Override
    public void run() {
        .....
        Slog.i(TAG, "Input Manager");
        //新建InputManagerService对象.
        inputManager = new InputManagerService(context, wmHandler);
    
        Slog.i(TAG, "Window Manager");
        //这是窗口服务，先不说这个。
        wm = WindowManagerService.main(context, power, display, inputManager,
                        uiHandler, wmHandler,
                        factoryTest != SystemServer.FACTORY_TEST_LOW_LEVEL,
                        !firstBoot, onlyCore);
        ServiceManager.addService(Context.WINDOW_SERVICE, wm);
        //将InputManagerService添加到Serviceanager，便于其他用户访问
        ServiceManager.addService(Context.INPUT_SERVICE, inputManager);
    
        ActivityManagerService.self().setWindowManager(wm);
    
        inputManager.setWindowManagerCallbacks(wm.getInputMonitor());
        inputManager.start();//启动服务
    
        display.setWindowManager(wm);
        //向DisplayManagerService设置InputManagerService
        display.setInputManager(inputManager);
        ....
    }

InputManagerService初始化时传递了一个参数wmHandler，其创建如下
    
    HandlerThread wmHandlerThread = new HandlerThread("WindowManager");
            wmHandlerThread.start();
    Handler wmHandler = new Handler(wmHandlerThread.getLooper());

这说明InputManagerService和WindowManagerService会有功能上的一些交互。

启动InputManagerService服务

    public void start() {
        Slog.i(TAG, "Starting input manager");
        nativeStart(mPtr);
        //将inputmanagerservice添加到Wathcdog中，Watchdog检测service是否正常工作
        // Add ourself to the Watchdog monitors.
        Watchdog.getInstance().addMonitor(this);
        //监听数据库中的Settings.System.POINTER_SPEED、Settings.System.SHOW_TOUCHES的变化，具体还不太清楚。
        registerPointerSpeedSettingObserver();
        registerShowTouchesSettingObserver();
        mContext.registerReceiver(new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                updatePointerSpeedFromSettings();
                updateShowTouchesFromSettings();
            }
        }, new IntentFilter(Intent.ACTION_USER_SWITCHED), null, mHandler);
        
        updatePointerSpeedFromSettings();
        updateShowTouchesFromSettings();
    }

nativeStart()函数调用到com_android_server_input_InputManagerService.cpp中的nativeStart()函数,cpp中的该函数主要是调用InputManager的start()方法，并将结果返回给java层

**服务的构造函数**

    public InputManagerService(Context context, Handler handler) {
        this.mContext = context;
        this.mHandler = new InputManagerHandler(handler.getLooper());
        //获取config_useDevInputEventForAudioJack的值，该值为true，则通过inputEvent处理耳机插拔，否则通过UEent处理耳机插拔。默认为false。
        mUseDevInputEventForAudioJack =
                    context.getResources().getBoolean(R.bool.config_useDevInputEventForAudioJack);
        Slog.i(TAG, "Initializing input manager, mUseDevInputEventForAudioJack="
                    + mUseDevInputEventForAudioJack);
        //调用native方法进行初始化操作
        mPtr = nativeInit(this, mContext, mHandler.getLooper().getQueue());
    }

config_useDevInputEventForAudioJack设置是在frameworks/base/core/res/res/values/config.xml中
该值为TRUE使用Linux /dev/input/event子系统的变化来检测开关的耳机/麦克风插孔，值为假时使用uevent框架。默认false。  
nativeInit调用到com_android_server_input_InputManagerService.cpp文件中,;路径为:frameworks\base\services\core\jni\com_android_server_input_InputManagerService.cpp

    static jint nativeInit(JNIEnv* env, jclass clazz,
            jobject serviceObj, jobject contextObj, jobject messageQueueObj) {
        sp<MessageQueue> messageQueue = android_os_MessageQueue_getMessageQueue(env, messageQueueObj);
        if (messageQueue == NULL) {
            jniThrowRuntimeException(env, "MessageQueue is not initialized.");
            return 0;
        }
        //创建NativeInputManager对象
        NativeInputManager* im = new NativeInputManager(contextObj, serviceObj,
                messageQueue->getLooper());
        im->incStrong(0);
        //返回 NativeInputManager对象的指针
        return reinterpret_cast<jint>(im);
    }

nativeInit中主要是创建一个NativeInputManager对象，用来连接java层和native层。查看该类的构造方法  

    NativeInputManager::NativeInputManager(jobject contextObj,
            jobject serviceObj, const sp<Looper>& looper) :
            mLooper(looper) {
        JNIEnv* env = jniEnv();
    
        mContextObj = env->NewGlobalRef(contextObj);
        mServiceObj = env->NewGlobalRef(serviceObj);
    
        {
            AutoMutex _l(mLock);
            mLocked.systemUiVisibility = ASYSTEM_UI_VISIBILITY_STATUS_BAR_VISIBLE;
            mLocked.pointerSpeed = 0;
            mLocked.pointerGesturesEnabled = true;
            mLocked.showTouches = false;
        }
        //创建EventHub对象，该对象主要用来访问设备节点，获取输入事件、设备节点的添加和删除
        sp<EventHub> eventHub = new EventHub();
        //创建InputManager对象，管理InputReader与InputDispatcher.
        mInputManager = new InputManager(eventHub, this, this);
    }

这里的InputManager类,路径frameworks/base/services/input/InputManager.cpp  
其构造方法和initialize()函数:

    InputManager::InputManager(
            const sp<EventHubInterface>& eventHub,
            const sp<InputReaderPolicyInterface>& readerPolicy,
            const sp<InputDispatcherPolicyInterface>& dispatcherPolicy) {
        //创建InputDispatcher对象
        mDispatcher = new InputDispatcher(dispatcherPolicy);
        //创建InputReader对象
        mReader = new InputReader(eventHub, readerPolicy, mDispatcher);
        //初始化
        initialize();
    }

    void InputManager::initialize() {
        mReaderThread = new InputReaderThread(mReader);
        mDispatcherThread = new InputDispatcherThread(mDispatcher);
    }

创建一个InputReaderThread事件读取线程，供InputReader事件读取者运行,/frameworks/native/services/inputflinger/InputReader.cpp
创建了一个InputDispatcherThread事件分发线程，供InputDispatcher事件分发者运行./frameworks/native/services/inputflinger/InputDispatcher.cpp

InputReaderThread,很简单，实际上就是一个线程对象。一旦启动了线程，则执行InputReader的loopOnce方法。  
InputDispatcherThread,也是一个线程对象，一旦线程启动了，则会调用InputDispatcher的dispatchOnce方法。
InputReader持有了InputDispatcher，并且被InputReaderThread线程持有。那么可以推断出，InputReader运行在InputReaderThread线程中，InputReader利用EventHub获取数据后,生成EventEntry事件，加入到InputDispatcher的mInboundQueue队列，再唤醒InputDispatcher线程

在InputDispatcher构造方法中使用new Looper创建一个循环对象,然后在dispatchOnce来分发事件

    void InputDispatcher::dispatchOnce() {
        nsecs_t nextWakeupTime = LONG_LONG_MAX;
        {
            AutoMutex _l(mLock);
            //唤醒等待线程，monitor()用于监控dispatcher是否发生死锁
            mDispatcherIsAliveCondition.broadcast();

            if (!haveCommandsLocked()) {
                //当mCommandQueue不为空时处理
                dispatchOnceInnerLocked(&nextWakeupTime);
            }

            if (runCommandsLockedInterruptible()) {
                nextWakeupTime = LONG_LONG_MIN;
            }
        }

        nsecs_t currentTime = now();
        int timeoutMillis = toMillisecondTimeoutDelay(currentTime, nextWakeupTime);
        mLooper->pollOnce(timeoutMillis); //进入epoll_wait等待状态,只有当callback：通过回调方法来唤醒.timeout：到达nextWakeupTime时间，超时唤醒.wake: 主动调用Looper的wake()方法
    }


MotionEvent.getY() 和 MotionEvent.getRawY() 的区别
getY 表示触摸事件在当前的View内的Y 坐标， getRawY表示触摸事件在整个屏幕上面的Y 坐标

MotionEvent.getActionIndex()
event.getActionIndex() 表示当前触摸手指的index, 用于多点触控。
getActionIndex 只在 ACTION_POINTER_DOWN 和 ACTION_POINTER_UP 的时候用到。
返回当前ACTION_POINTER_DOWN 或者 ACTION_POINTER_UP 对应的手指Index。如果不是ACTION_POINTER_DOWN 和ACTION_POINTER_UP 事件就会一直返回0。

我们拿到当前的触摸手指的Index 之后，就可以拿到当前触摸手指的Id:event.getPointerId(event.getActionIndex()). 在多点触控过程中，Index 可能会变，但是Id 不会变。 我们也可以根据Id 拿到 index，从而计算触摸手指Id 对应的Y 坐标：event.findPointerIndex(mActivePointerId)