PackageManagerService（简称 PMS），是 Android 系统核心服务之一，处理包管理相关的工
作，常见的比如安装、卸载应用等

PMS是系统服务，那么应用层肯定有个PackageManager作为binder call client端来供使用，但
是这里要注意，PackageManager是个抽象类，一般使用的是它的实现类：
ApplicationPackageManager。

PackageManager提供的功能主要包含如下几点：
* 提供一个应用程序的所有信息（ApplicationInfo）。
* 提供四大组件的信息。
* 查询permission相关信息。
* 提供包的信息。
* 安装、卸载APK。

PMS作为系统服务,也是从systemserver中启动:
frameworks/base/services/java/com/android/server/SystemServer.java


