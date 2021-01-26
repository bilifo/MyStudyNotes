/**
项目需求在 PhoneWindowManager 增加一个只关闭触摸板事件的方法.就从native的InputDispatcher,到jni的com_android_server_input_InputManagerService,最后到framwork的WindowManagerService.
*/
git diff frameworks/base/services/core/java/com/android/server/input/InputManagerService.java 
        frameworks/base/services/core/java/com/android/server/policy/PhoneWindowManager.java 
        frameworks/base/services/core/java/com/android/server/policy/WindowManagerPolicy.java  
        frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java 
        frameworks/base/services/core/jni/com_android_server_input_InputManagerService.cpp 
        frameworks/native/services/inputflinger/InputDispatcher.cpp 
        frameworks/native/services/inputflinger/InputDispatcher.h
============================以下是git diff =======================
============native 层===============

    diff --git a/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.cpp b/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.cpp
    old mode 100644
    new mode 100755
    index b921d95..63bb075
    --- a/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.cpp
    +++ b/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.cpp
    @@ -238,6 +238,7 @@ InputDispatcher::InputDispatcher(const sp<InputDispatcherPolicyInterface>& polic
        mAppSwitchSawKeyDown(false), mAppSwitchDueTime(LONG_LONG_MAX),
        mNextUnblockedEvent(nullptr),
        mDispatchEnabled(false), mDispatchFrozen(false), mInputFilterEnabled(false),
    +    mDispatchMotionEnabled(true),//初始化 mDispatchMotionEnabled 的值为true
        mFocusedDisplayId(ADISPLAY_ID_DEFAULT),
        mInputTargetWaitCause(INPUT_TARGET_WAIT_CAUSE_NONE) {
        mLooper = new Looper(false);
    @@ -430,13 +435,16 @@ void InputDispatcher::dispatchOnceInnerLocked(nsecs_t* nextWakeupTime) {
        }

        if (done) {
    +        if(mDispatchMotionEnabled){//pjl++  mDispatchMotionEnabled 作为禁用触摸移动事件motion的开关 true:允许分发事件  false:不允许事件传递
                if (dropReason != DROP_REASON_NOT_DROPPED ) {
                    dropInboundEventLocked(mPendingEvent, dropReason);
                }
                mLastDropReason = dropReason;

                releasePendingEventLocked();
                *nextWakeupTime = LONG_LONG_MIN;  // force next poll to wake up immediately
    +        }
        }
    }

    @@ -5240,4 +5248,31 @@ bool InputDispatcherThread::threadLoop() {
        return true;
    }

    +//pjl++ 按照原本就有的setInputDispatchMode方法,仿写的,就是对 mDispatchMotionEnabled 进行设置true or false
    +void InputDispatcher::setInputDispatchMotionMode(bool enabled) {
    +#if DEBUG_FOCUS
    +    ALOGD("setInputDispatchMotionMode: enabled=%d", enabled);
    +#endif
    +    bool changed;
    +    { // acquire lock
    +        std::scoped_lock _l(mLock);
    +
    +        if (mDispatchMotionEnabled != enabled) {
    +            mDispatchMotionEnabled = enabled;
    +            changed = true;
    +        } else {
    +            changed = false;
    +        }
    +
    +#if DEBUG_FOCUS
    +        logDispatchStateLocked();
    +#endif
    +    } // release lock
    +
    +    if (changed) {
    +        // Wake up poll loop since it may need to make new input dispatching choices.
    +        mLooper->wake();
    +    }
    +}
    +
    } // namespace android
    diff --git a/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.h b/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.h
    old mode 100644
    new mode 100755
    index 753b748..1012e9c
    --- a/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.h
    +++ b/LINUX/android/frameworks/native/services/inputflinger/InputDispatcher.h
    @@ -345,6 +345,8 @@ public:
        */
        virtual void setInputDispatchMode(bool enabled, bool frozen) = 0;

    +    virtual void setInputDispatchMotionMode(bool enabled) = 0;//pjl++ 声明 InputDispatcher.cpp 中的新增方法
    +
        /* Sets whether input event filtering is enabled.
        * When enabled, incoming input events are sent to the policy's filterInputEvent
        * method instead of being dispatched.  The filter is expected to use
    @@ -437,6 +439,7 @@ public:
                const sp<InputApplicationHandle>& inputApplicationHandle) override;
        virtual void setFocusedDisplay(int32_t displayId) override;
        virtual void setInputDispatchMode(bool enabled, bool frozen) override;
    +    virtual void setInputDispatchMotionMode(bool enabled) override;//pjl++ 也是声明,但不知道为什么要再次写
        virtual void setInputFilterEnabled(bool enabled) override;

        virtual bool transferTouchFocus(const sp<IBinder>& fromToken, const sp<IBinder>& toToken)
    @@ -1041,6 +1044,9 @@ private:
        bool mDispatchFrozen GUARDED_BY(mLock);
        bool mInputFilterEnabled GUARDED_BY(mLock);

    +    //pjl++ 声明 mDispatchMotionEnabled 变量
    +    bool mDispatchMotionEnabled GUARDED_BY(mLock);
    +
        std::unordered_map<int32_t, std::vector<sp<InputWindowHandle>>> mWindowHandlesByDisplay
                GUARDED_BY(mLock);
        // Get window handles by display, return an empty vector if not found.

============jni 层===============

    diff --git a/LINUX/android/frameworks/base/services/core/jni/com_android_server_input_InputManagerService.cpp b/LINUX/android/frameworks/base/services/core/jni/com_android_server_input_InputManagerService.cpp
    old mode 100644
    new mode 100755
    index b3f24b8..b7fedf0
    --- a/LINUX/android/frameworks/base/services/core/jni/com_android_server_input_InputManagerService.cpp
    +++ b/LINUX/android/frameworks/base/services/core/jni/com_android_server_input_InputManagerService.cpp
    @@ -228,6 +228,8 @@ public:
        void setCustomPointerIcon(const SpriteIcon& icon);
        void setPointerCapture(bool enabled);
        void setMotionClassifierEnabled(bool enabled);
    +
    +       void setInputDispatchMotionMode(bool enabled);//pjl++ InputManagerService.cpp 新增方法声明

        /* --- InputReaderPolicyInterface implementation --- */

    @@ -857,6 +859,10 @@ void NativeInputManager::setInputDispatchMode(bool enabled, bool frozen) {
        mInputManager->getDispatcher()->setInputDispatchMode(enabled, frozen);
    }

    +void NativeInputManager::setInputDispatchMotionMode(bool enabled) {//pjl++ 创建 NativeInputManager 的 setInputDispatchMotionMode 方法,这里是调用 getDispatcher() 的 setInputDispatchMotionMode 方法
    +    mInputManager->getDispatcher()->setInputDispatchMotionMode(enabled);
    +}
    +
    void NativeInputManager::setSystemUiVisibility(int32_t visibility) {
        AutoMutex _l(mLock);

    @@ -1569,6 +1575,14 @@ static void nativeSetInputDispatchMode(JNIEnv* /* env */,
        im->setInputDispatchMode(enabled, frozen);
    }

    +//pjl++ 创建 jni 的(提供给java调用的) nativeSetInputDispatchMotionMode 方法,这里调用了 NativeInputManager 的 setInputDispatchMotionMode
    +static void nativeSetInputDispatchMotionMode(JNIEnv* /* env */,
    +        jclass /* clazz */, jlong ptr, jboolean enabled) {
    +    NativeInputManager* im = reinterpret_cast<NativeInputManager*>(ptr);
    +
    +    im->setInputDispatchMotionMode(enabled);
    +}
    +
    static void nativeSetSystemUiVisibility(JNIEnv* /* env */,
            jclass /* clazz */, jlong ptr, jint visibility) {
        NativeInputManager* im = reinterpret_cast<NativeInputManager*>(ptr);
    @@ -1802,6 +1816,8 @@ static const JNINativeMethod gInputManagerMethods[] = {
                (void*) nativeSetPointerCapture },
        { "nativeSetInputDispatchMode", "(JZZ)V",
                (void*) nativeSetInputDispatchMode },
    +       { "nativeSetInputDispatchMotionMode", "(JZZ)V",  //jni的新增方法声明
    +            (void*) nativeSetInputDispatchMotionMode },
        { "nativeSetSystemUiVisibility", "(JI)V",
                (void*) nativeSetSystemUiVisibility },
        { "nativeTransferTouchFocus", "(JLandroid/view/InputChannel;Landroid/view/InputChannel;)Z",
=========framework 层===========

    diff --git a/LINUX/android/frameworks/base/services/core/java/com/android/server/input/InputManagerService.java b/LINUX/android/frameworks/base/services/core/java/com/android/server/input/InputManagerService.java
    old mode 100644
    new mode 100755
    index 86e54f5..756fa27
    --- a/LINUX/android/frameworks/base/services/core/java/com/android/server/input/InputManagerService.java
    +++ b/LINUX/android/frameworks/base/services/core/java/com/android/server/input/InputManagerService.java
    @@ -220,6 +221,7 @@ public class InputManagerService extends IInputManager.Stub
        private static native void nativeSetInputWindows(long ptr, InputWindowHandle[] windowHandles,
                int displayId);
        private static native void nativeSetInputDispatchMode(long ptr, boolean enabled, boolean frozen);
    +    private static native void nativeSetInputDispatchMotionMode(long ptr, boolean enabled);//pjl++ 增加从jni处获得的native方法的声明
        private static native void nativeSetSystemUiVisibility(long ptr, int visibility);
        private static native void nativeSetFocusedApplication(long ptr,
                int displayId, InputApplicationHandle application);
    @@ -1539,6 +1541,10 @@ public class InputManagerService extends IInputManager.Stub
            nativeSetInputDispatchMode(mPtr, enabled, frozen);
        }

    +    public void setInputDispatchMotionMode(boolean enabled) {//pjl++  调用 jni 的 nativeSetInputDispatchMotionMode 方法
    +        nativeSetInputDispatchMotionMode(mPtr, enabled);
    +    }
    +
        public void setSystemUiVisibility(int visibility) {
            nativeSetSystemUiVisibility(mPtr, visibility);
        }

_

    diff --git a/LINUX/android/frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java b/LINUX/android/frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java
    old mode 100644
    new mode 100755
    index bc813c7..b064009
    --- a/LINUX/android/frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java
    +++ b/LINUX/android/frameworks/base/services/core/java/com/android/server/wm/WindowManagerService.java
    @@ -7850,4 +7850,9 @@ public class WindowManagerService extends IWindowManager.Stub
                        0 /* configChanges */, !PRESERVE_WINDOWS, true /* notifyClients */);
            }
        }
    +      
    +   //这里有个细节,WindowManagerService.java类是实现  WindowManagerPolicy.WindowManagerFuncs 接口的.
    +    @Override
    +    public void setInputDispatchMotionMode(boolean enabled) {//pjl++ mInputManager对象是 InputManagerService 实例,增加 WindowManagerService 的 setInputDispatchMotionMode 方法,就是调用 InputManagerService 的同名方法
    +        mInputManager.setInputDispatchMotionMode(enabled);
    +    }
    }

_

    diff --git a/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/WindowManagerPolicy.java b/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/WindowManagerPolicy.java
    old mode 100644
    new mode 100755
    index 6d9c710..6118532
    --- a/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/WindowManagerPolicy.java
    +++ b/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/WindowManagerPolicy.java
    @@ -649,6 +649,8 @@ public interface WindowManagerPolicy extends WindowManagerPolicyConstants {
            * as the top display.
            */
            void moveDisplayToTop(int displayId);
    +       //内部接口WindowManagerFuncs中声明接口方法setInputDispatchMotionMode,由前面的 WindowManagerService 去实现
    +        void setInputDispatchMotionMode(boolean enabled);//pjl++   PhoneWindowManager 中使用了 WindowManagerPolicy,所以要 WindowManagerFuncs 提供 setInputDispatchMotionMode方法(香蕉猴子森林问题愈发明显)
        }

        /**  

_

    diff --git a/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/PhoneWindowManager.java b/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/PhoneWindowManager.java
    index 97809eb..0b1ae49 100755
    --- a/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/PhoneWindowManager.java
    +++ b/LINUX/android/frameworks/base/services/core/java/com/android/server/policy/PhoneWindowManager.java
    @@ -235,6 +235,11 @@ import java.io.PrintWriter;
    import java.util.HashSet;
    import java.util.List;

    +import java.io.FileDescriptor;
    +import android.system.Os;
    +import java.io.FileInputStream;
    +import android.system.Int32Ref;
    +
    /**
    * WindowManagerPolicy implementation for the Android phone UI.  This
    * introduces a new method suffix, Lp, for an internal lock of the
    @@ -3783,14 +3788,36 @@ public class PhoneWindowManager implements WindowManagerPolicy {
                    }

                case KeyEvent.KEYCODE_FN_NUM_LOCK: {
                        Log.d("ljx","KEYCODE_FN_NUM_LOCK="+KeyEvent.KEYCODE_FN_NUM_LOCK);
    +                    mWindowManagerFuncs.setInputDispatchMotionMode(false);//当按下FN和numlock键时,调用功能
                        break;
                    }

    
