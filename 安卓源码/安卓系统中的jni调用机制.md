# 流程
android系统启动,先启动 **Kernel创建init进程**,紧接着init进程fork第一个横穿java和c/c++的进程**Zygote进程**.Zygote启动过程中会在**AndroidRuntime.cpp**中的**startVm创建虚拟机**，VM创建完成后，紧接着**调用startReg**完成虚拟机中的JNI方法注册。 (Zygote是由init进程通过解析init.zygote.rc文件而创建的，zygote所对应的可执行程序app_process，所对应的源文件是App_main.cpp，进程名为zygote) 

1.App_main.cpp:

    int main(int argc, char* const argv[])
    {
    
        //生成一个AppRuntime对象，把main传递过来的参数传给AppRuntime
        //class AppRuntime : public AndroidRuntime
        AppRuntime runtime(argv[0], computeArgBlockSize(argc, argv));
        ......
        if (zygote) {//见1.1分析
            runtime.start("com.android.internal.os.ZygoteInit", args, zygote);
        } else if 
        ......
    }

1.1 AndroidRuntime.cpp-->start:

    void AndroidRuntime::start(const char* className, const Vector<String8>& options, bool zygote)
    { 
        ......
        if (startVm(&mJavaVM, &env, zygote) != 0) {
            return;
        }
        onVmCreated(env);
        if (startReg(env) < 0) {//见分析2.1
            ALOGE("Unable to register all android natives\n");
            return;
        }
        ...
    
        /*
        * Start VM.  This thread becomes the main thread of the VM, and will
        * not return until the VM exits.
        */
        char* slashClassName = toSlashClassName(className);
        jclass startClass = env->FindClass(slashClassName);
        if (startClass == NULL) {
            ALOGE("JavaVM unable to locate class '%s'\n", slashClassName);
            /* keep going */
        } else {//ZygoteInit 通过反射找到zygoteInit.main的方法ID。
            jmethodID startMeth = env->GetStaticMethodID(startClass, "main",
                "([Ljava/lang/String;)V");
            if (startMeth == NULL) {
                ALOGE("JavaVM unable to find main() in '%s'\n", className);
                /* keep going */
            } else {//执行zygoteinit.main方法，zygoteinit类为java类
                env->CallStaticVoidMethod(startClass, startMeth, strArray);
        ......
    }

2.1 AndroidRuntime.cpp-->startReg:
    
    int AndroidRuntime::startReg(JNIEnv* env)
    {
        //设置线程创建方法为javaCreateThreadEtc
        androidSetCreateThreadFunc((android_create_thread_fn) javaCreateThreadEtc);
    
        env->PushLocalFrame(200);
        //进程NI方法的注册
        if (register_jni_procs(gRegJNI, NELEM(gRegJNI), env) < 0) {
            env->PopLocalFrame(NULL);
            return -1;
        }
        env->PopLocalFrame(NULL);
        return 0;
    }

register_jni_procs(gRegJNI, NELEM(gRegJNI), env)这行代码的作用就是就是循环调用gRegJNI数组成员所对应的方法。

    static int register_jni_procs(const RegJNIRec array[], size_t count, JNIEnv* env) {
        for (size_t i = 0; i < count; i++) {
            if (array[i].mProc(env) < 0) {
                return -1;
            }
        }
        return 0;
    }

gRegJNI数组，有100多个成员变量，定义在AndroidRuntime.cpp,这些extern方法绝大多数位于 /framework/base/core/jni 目录，大多数情况下 native命名方式为.但也有少数native文件命名方式，有时并非[包名]_[类名].cpp，比如Binder.java(Binder.java所对应的native文件：android_util_Binder.cpp)

    static const RegJNIRec gRegJNI[] = {
        REG_JNI(register_android_os_MessageQueue),
        REG_JNI(register_android_os_Binder),
        ...
    }

REG_JNI是一个宏定义,等价于调用其参数名所指向的函数

    #define REG_JNI(name) { name }
    struct RegJNIRec {
        int (*mProc)(JNIEnv*);
    };

例如REG_JNI(register_com_android_internal_os_RuntimeInit).mProc也就是指进入register_com_android_internal_os_RuntimeInit方法，接下来就继续以此为例来说明：

    int register_com_android_internal_os_RuntimeInit(JNIEnv* env) {
    return jniRegisterNativeMethods(env, "com/android/internal/os/RuntimeInit",
        gMethods, NELEM(gMethods));
    }

    //gMethods：java层方法名与jni层的方法的一一映射关系
    static JNINativeMethod gMethods[] = {
        { "nativeFinishInit", "()V",
            (void*) com_android_internal_os_RuntimeInit_nativeFinishInit },
        { "nativeZygoteInit", "()V",
            (void*) com_android_internal_os_RuntimeInit_nativeZygoteInit },
        { "nativeSetExitWithoutCleanup", "(Z)V",
            (void*) com_android_internal_os_RuntimeInit_nativeSetExitWithoutCleanup },
    };
