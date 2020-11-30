测试:
1/创建需要用adb运行的java代码.eg:Test.java(如果没有java环境,可以使用Android Studio\jre\bin下的javac和java)

    public class Test {
        public static void main(String[] args) {
            System.out.println("Android test");
        }
    }

2/在java代码所在的文件夹下,运行

    javac Test.java

生成Test.class文件,再运行

    java Test

检验是否成功

3/由于Android虚拟机(dalvik虚拟机或者ART)和pc上的java虚拟机有些不一样,所以.class字节码无法在Android设备上直接运行,这里使用Android SDK中的dx工具进行转换.(Android studio的dx工具位于AndroidSDK/build-tools/(版本号)/目录下,建议添加到环境变量)

    dx --dex --output=Test.dex Test.class

--output=Test.dex指明.dex文件输出路径

4/push生成的.dex文件

    adb push Test.dex /sdcard/

5/adb运行这个.dex文件

    adb shell app_process -Djava.class.path=/sdcard/Test.dex /data/local/tmp Test
        /data/local/tmp表示切换到/data/local/tmp目录下运行 
        Test表示start-class-name 

app_process格式:

    app_process [vm-options] cmd-dir [options] start-class-name [main-options]
        vm-options – VM 选项
        cmd-dir –父目录 (/system/bin)
        options –运行的参数 :
            –zygote
            –start-system-server
            –application (api>=14)
            –nice-name=nice_proc_name (api>=14)
        start-class-name –包含main方法的主类  (com.android.commands.am.Am)
        main-options –启动时候传递到main方法中的参数

6/代码中通过反射调用这个.dex文件

    public Class<?> loadClass(){
        //这里我直接把Test.dex文件push到sdcard了
        PathClassLoader pathClassLoader=new PathClassLoader("/sdcard/Test.dex", ClassLoader.getSystemClassLoader());
        try {
            //如果Test类存在包名,注意把包名加上eg:loadClass("com.example.Test");
            return pathClassLoader.loadClass("Test");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        return null;
    }
    public void invoke(Class<?> cls){
        String[] strings=new String[1];
        try {
            //这里直接使用反射调用的main方法,如果存在其它方法,也可以使用反射来调用
            Method method=cls.getDeclaredMethod("main",String[].class);
            method.invoke(null,strings);
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }catch (InvocationTargetException e) {
            e.printStackTrace();
        }
    }
    public void invoke(){
        Class<?> cls=loadClass();
        if (cls!=null) {
            invoke(cls);
        }
    }

7/类存在包名:
https://blog.csdn.net/u011956004/article/details/78923261


## 错误集:
dx由于没有找到java.exe报错:

    ERROR: No suitable Java found. In order to properly use the Android Developer
    Tools, you need a suitable version of Java JDK installed on your system.
    We recommend that you install the JDK version of JavaSE, available here:
    http://www.oracle.com/technetwork/java/javase/downloads

    If you already have Java installed, you can define the JAVA_HOME environment
    variable in Control Panel / System / Avanced System Settings to point to the
    JDK folder.

    You can find the complete Android SDK requirements here:
    http://developer.android.com/sdk/requirements.html

分析:
查看dx.bat脚本,可以看到 if not defined java_exe goto :EOF ,即java_exe这个变量不存在,往上看,java_exe赋值来自 ..\tools\lib\find_java.bat
查看find_java.bat脚本,发现报错信息的输出来自 :CheckFailed ,是由 if not defined java_exe goto :CheckFailed ,java_exe不存在引起,而java_exe赋值是一个for循环

修改方法:
将find_java.bat中的java_exe,强制指定为 Android Studio\jre\bin下的java.exe

    - for /f "delims=" %%a in ('"%~dps0\find_java%arch_ext%.exe" -s') do set java_exe=%%a
    - if not defined java_exe goto :CheckFailed
    + set java_exe=E:\android_studio2\jre\bin\java.exe


