KaiOS FAQ
====

基于KaiOS v2.5R2。

[TOC]

## 目录

* [注意事项](#注意事项)
* [开发工具](#开发工具)
* [客制化](#客制化)
* [API使用](#api使用)
* [系统应用](#系统应用)
* [应用商店](#应用商店)
* [移动与无线连接](#移动与无线连接)
* [工厂测试](#工厂测试)
* [其他](#其他)

---
## 注意事项

* **不要在应用中使用navigator.engmodeExtension。**
    - navigator.engmodeExtenstion仅做测试用；
    - 安全和性能无法保障，可能导致一些系统稳定性问题；
    - KaiOS不对engmode和mmitest以外使用该API的应用提供技术支持。
    <br>

* **不要滥用[HTMLElement.focus()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus)。**
    - 强制focus，尤其在System应用可能导致系统丢失焦点，终端无响应；
    - 不要使用setTimeout和Element.focus()来规避一些丢焦问题。
    <br>

* **不要滥用[Settings API](https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/Settings_API)。**
    - mozSettings一般只在System和Settings中使用；
    - 频繁的mozSettings调用严重影响系统性能，并有可能导致Settings数据库异常；
    - 不要将Settings API用于应用进程间通信。
    <br>

* **避免在Javascript主线程中运行耗时较长的代码。**
    - Gecko, System中可能诱发时序问题引起的丢焦；
    - 可能导致较长时间的终端无响应。

---
## 开发工具

#### Q. 什么是WebIDE, 如何安装使用？
* [WebIDE](https://developer.mozilla.org/en-US/docs/Archive/WebIDE)是Mozilla为Firefox OS, Firefox for Android等提供的连接桌面Firefox浏览器到设备远程调试的工具。最新版本的Firefox已不再更新，后续可能会被移除。KaiOS 2.5基于Firefox48，建议在[Mozilla ftp](https://ftp.mozilla.org/pub/firefox/releases/)下载Firefox v48~v59之间版本，v60及以上版本WebIDE无法正常连接KaiOS设备。
      <br>
    - 关闭Firefox自动更新；
      <img width="480px" src="assets/tools/webide-disable-update.png">
      <br>
    - `adb root` 开启终端adbd的root权限；
      <br>
    - `adb forward tcp:6000 localfilesystem:/data/local/debugger-socket`[连接PC和设备](https://developer.mozilla.org/en-US/docs/Archive/WebIDE/Setting_up_runtimes#Remote_runtime);
      <img width="480px" src="assets/tools/webide-adb-forward.png">
      <br>
    - 打开WebIDE, 连接tcp:6000的Remote Runtime；
      <img width="680px" src="assets/tools/webide-remote-runtime.png">
      <br>
    - 点击左侧Remote apps中任意app，开始debug。
      <img width="680px" src="assets/tools/webide-remote-apps.png">
      <br>
  
* 开发工具的使用见[Firefox Developer Tools](https://developer.mozilla.org/en-US/docs/Tools)，一些tips:
      <br>
    - Tools栏右上角设置按钮可以打开一些额外的工具, Storage不可用（可能会导致WebIDE断开）；
      <img width="680px" src="assets/tools/webide-settings.png">
      <br>

    - [Memory](https://developer.mozilla.org/en-US/docs/Tools/Memory) 仅在Firefox48下可用，可用来查看应用的js堆内存状态，优化应用内存；
      <br>
    - System应用进程中中的额外iframe如callscreen可以在右上角切换；
      <img width="680px" src="assets/tools/webide-switch-iframe.png">
      <br>

    - Main Process中可以调试Gecko中Javascript源码；
      <img width="680px" src="assets/tools/webide-main-process.png">
      <br>

    - [Responsive design mode](https://developer.mozilla.org/en-US/docs/Tools#Responsive_Design_Mode)(非WebIDE, 浏览器的Developer Tools) 下选择Nokia 8810 4G，查看网页在KaiOS设备中布局。
      <img width="680px" src="assets/tools/responsive-design-mode.png">

---
#### Q. WebIDE如何获取和修改设备Preference，如何屏幕截图?
* 设备连接WebIDE后，右侧工具栏"Device Preferences" 点开可以获得和修改设备当前pref值；
* "Screenshot" 可以截取设备主屏。
    <img width="680px" src="assets/tools/webide-device-preferences.png">

#### Q. 离线或者其他原因导致WebIDE adb helper插件不可用时，如何手动安装本地插件？

1. 下载对应的最新插件版本 xxx.latest.xpi
https://ftp.mozilla.org/pub/labs/fxos-simulator/adb-helper/


2. 下载并且安装firefox nightly
https://download-installer.cdn.mozilla.net/pub/firefox/nightly/2017/11/2017-11-19-22-01-26-mozilla-central/


3. 打开firefox nightly进行如下操作：
-  nightly中输入 about:config
-  reference 中设置如下两项
```
xpinstall.signatures.required should be set to false
extensions.legacy.enabled should be set to true
```

4. 重启浏览器并且安装第一步下载的adbhelper插件
settings -> add-ons -> install Add-on from file

ref: [Test a local build of ADB Helper](https://github.com/mozilla/adbhelper#test-a-local-build-of-adb-helper)

---
#### Q. KaiOS系统怎么抓取ril log？
* ADB log中会有少量的ril信息，详细的信息需要芯片厂商提供。比如高通需要QXDM log。

---
#### Q. 系统中的js如果要输出log进行调试，怎么从手机上抓log看？
A. 用adb log。

代码里面写`dump("advvdffsdf"+变量);`用`adb logcat` 就可以看LOG。再比如`DUMP('STK_CMD_GET_INPUT: Response = ', value);`

---
#### Q. 假设打开一个app，当正在点击的时候，对应的js代码突然崩溃了，这个时候要怎么办？
A. 通过log定位exception，或者通过dump分析backtrace。一般js错误都不会导致app崩溃，只是不会跑这个js脚本，logcat里面会打印JavaScript　Error的错误。

---
#### Q. KaiOS上有哪些测试工具和脚本需要我们学习并可能会用到的？

* `*#*#0574#*#*` : 进入logmanager应用
* `*#8378269#` 进入工程模式
* `*#2886#` 进入mmitest应用

---
#### Q. Gaia层是否都可以在Web Developer之类的PC工具上调试？如何调试？Native code如何调试？
A. Webapps可以用Firefox Web IDE来调试。
> 注意不是所有的js都能被调试，有些没加载出来的就不能调试，native code如果是js文件可以直接把手机里面的/system/b2g/omni.ja拿出来修改直接push进手机重启生效。(比如 MmsService.js)

---
#### Q. 如何令User Mode软件可以连接ADB？
A. User版本连接ADB首先需要打开usb debug开关, 这个开关在User版本上一般默认关闭.

这个开关由一个property 值控制: ro.debuggable
（或者OEM通过增加暗码的方式打开ADB，取决于OEM是否真的在出货的user版本决定开启ADB）.

可以在编译文件里面设为1,

比如自己编译的时候想要默认打开的,在main.mk中

```
ifeq (true,$(strip $(enable_target_debugging)))
  # Target is more debuggable and adbd is on by default
  ADDITIONAL_DEFAULT_PROPERTIES += ro.debuggable=1
  # Enable Dalvik lock contention logging.
  ADDITIONAL_BUILD_PROPERTIES += dalvik.vm.lockprof.threshold=500
  # Include the debugging/testing OTA keys in this build.
  INCLUDE_TEST_OTA_KEYS := true
else # !enable_target_debugging
  # Target is less debuggable and adbd is off by default
  ADDITIONAL_DEFAULT_PROPERTIES += ro.debuggable=0
endif # !enable_target_debugging
```

还有一个方法:在settings--> device--> device information--> more information.在“OS version”上,按顺序“左软键,左软键,右软键,左软键,右软键,右软键”,可打开关闭调试
但会出现 adb.exe: device unauthorized. 问题
---
## 客制化

#### Q. 什么是设备Preference，如何定制？
* [Preference](https://developer.mozilla.org/en-US/docs/Mozilla/Preferences/A_brief_guide_to_Mozilla_preferences)（以下简称pref）是Mozilla产品的系统设置，Firefox浏览器中可以通过about:config打开查看，KaiOS设备Device Preferences可以[通过WebIDE查看](#q-webide如何获取和修改设备preference如何屏幕截图)。
    - KaiOS设备默认pref在 `gecko/b2g/app/b2g.js`；
    - Gecko pref模块所有pref在 `gecko/libpref/init/all.js`；
    - 设备自定义pref文件如dev-pref.js会被拷贝到`system/b2g/defaults/pref`下，首次开机将覆盖`b2g.js`和`all.js`中设置；
      <img width="680px" src="assets/customization/dev-pref.png">
    - 不要直接修改`b2g.js`和`all.js`。
      <br>

* 不同的平台配置参考路径，一些项目可能在vendor/目录下：
    - QCOM: `device/qcom/msm8909_512/default-prefs/proc-pref.js`
    - UNISOC: `device/sprd/pike2/sp7731ef_18c10/default-prefs/dev-pref.js`
    - MTK:  `device/kaiostech/kaios72/dev-pref.js`

---
#### Q. 什么是UA, 如何定制？
* UA即浏览器User Agent, 当前设备UA可以在用如下方式查看：
    - WebIDE Console中输入`navigator.userAgent`；
    - Browser中打开在线工具，如 http://www.enhanceie.com/ua.aspx ；
* KaiOS 2.5R2的默认UA为：`Mozilla/5.0 (Mobile; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.5.2`。
* OEM可以加入device model，如`Nokia 8810 4G`默认UA为：
      `Mozilla/5.0 (Mobile; Nokia 8810 4G; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.5`。
* 一般网站会识别"Mobile"关键字，给出移动端网页；部分网站可能无法做到兼容；不建议加入"Android"字样做以适合此类网站，网站可能有Android only代码，导致在KaiOS设备上无法正常浏览部分内容。
* UA生成逻辑见 `gecko/netwerk/protocol/http/nsHttpHandler.cpp::BuildUserAgent()`。方法内增加mProductName.AssignLiteral("Nokia 8810 4G");//增加Nokia 8810 4G

---
#### Q. 如何针对特定的网址修改UA?
* 修改如下两个pref：

```
  pref("general.useragent.updates.enabled", true);
  pref("general.useragent.updates.url", "");
```

* 在`/gecko/b2g/app/ua-update.json.in`里面修改，新增所需网址：
```
  // bug 878653, redstarbelgrade.info
  "redstarbelgrade.info": "\\(Mobile#(Android; Mobile",
  // bug 55881, lequipe.fr
  "lequipe.fr": "\\(Mobile#(Android; Mobile",
  // bug 55881, orangemali.com
  "orangemali.com": "\\(Mobile#(Android; Mobile"
```

---
#### Q. 如何设置MMS UA Profile?
* MMS UA Profile 在`gecko/dom/mobilemessage/gonk/MMSService.js`里设置:(这个UA profile 和 前面UA不一样,前面的UA代表的是网络请求头的一个字符串)

```
    // UAProf headers.
    let uaProfUrl, uaProfTagname = "x-wap-profile";
    try {
      uaProfUrl = Services.prefs.getCharPref('wap.UAProf.url');
      uaProfTagname = Services.prefs.getCharPref('wap.UAProf.tagname');
    } catch (e) {}

    if (uaProfUrl) {
      xhr.setRequestHeader(uaProfTagname, uaProfUrl);
    }
```
* 默认值在 `gecko/modules/libpref/init/all.js`
```
// MMS UA Profile settings
pref("wap.UAProf.url", "");
pref("wap.UAProf.tagname", "x-wap-profile")
```
* 添加相关pref覆盖默认值即可；不过gecko\b2g\chrome\content\settings.js中的值会覆盖它.此后可检查Http Request头x-wap-profile项判断是否设置成功。
* 检查方法:
  1/发送彩信时,使用 " adb shell tcpdump -i any -s 0  -U -w /data/tcpdump.pcap " 抓取tcpdump日志
  2/然后使用 "Wireshark" 网络分析器,过滤查找"http",看 Hypertext Transfer Protocol里的User-Agent,有没有配置的url
* UA profile 文件
    - 一般是 .xml或.rdf格式，描述终端设备相关信息；"wap.UAProf.tagname"均是使用"x-wap-profile".
    - 由OEM或Operator服务器维护, 文件url填入上述"wap.UAProf.url"。

---
#### Q. 如何配置APN?
* APN 配置在`gaia/shared/resources/apn.json`, 匹配mcc/mnc获取。System和Setting应用都会打包该文件进 application.zip，System会读取做apn初始化设置，Settings则会显示相关mcc/mnc下可用APN list。

```
    "218": {
      "90": [
          {"carrier":"BHMobileInternet","apn":"active.bhmobile.ba","type":["default","supl"],"protocol":"IPV4V6"},
          {"carrier":"BHMobileMMS","apn":"mms.bhmobile.ba","mmsc":"http://mms.bhmobile.ba/servlets/mms","mmsproxy":"195.222.56.41","mmsport":"8080","type":["mms"],"protocol":"IPV4V6"}
      ],
      "03": [
          {"carrier":"HT Eronet WAP","apn":"wap.eronet.ba","proxy":"10.12.3.10","port":"8080","type":["default","supl"]},
          {"carrier":"HT Eronet GPRS","apn":"gprs.eronet.ba","type":["default","supl"]},
          {"carrier":"Ht Eronet MMS","apn":"mms.eronet.ba","mmsc":"http://mms.gprs.eronet.ba/mms/wapenc","mmsproxy":"10.12.3.11","mmsport":"8080","type":["mms"]}
      ],
      "05": [
          {"carrier":"m:tel","apn":"3g1","proxy":"192.168.61.10","port":"80","type":["default","supl"]},
          {"carrier":"mtelgprs","apn":"3g1","type":["default","supl"]},
          {"carrier":"mtelmms","apn":"mtelmms","mmsc":"http://mmsc.mtel.ba/mms/wapenc","mmsproxy":"192.168.61.11","mmsport":"80","type":["mms"]}
      ]
    },
```
* `apn.json`源自[AOSP device sample](https://android.googlesource.com/device/sample/+/refs/heads/master/etc/apns-full-conf.xml)，由`gaia/shared/resources/apn`下`apns_conf_xxx.xml`文件生成，生成方式请参考该目录下README.md。APN相关field意义请参考Android相关文档。
* `apn.json`修改后，需重新编入System和Settings应用，恢复出厂设置以使之生效。
* `adb shell ls /system/etc` 看到的`apns-conf.xml`一般来自`vendor/xxx`，由QCOM/MTK/UNISOC编入，在KaiOS系统中不会生效。

---
#### Q. 如何定制开关机动画？

* 开机动画包括三部分:
    - **Splash 开机首帧**；实现在Bootloader，一般需烧入单独的splash image分区，修改请咨询QCOM/MTK/UNISOC；
      相关代码（QCOM）`bootable\bootloader\lk\platform\msm_shared\include\splash.h`。
    - **Boot Animation 开机动画**；`gonk-misc\bootanimation.zip`，格式同Android，相关代码`gecko/widget/gonk/libdisplay/BootAnimation.cpp`。
    - **System 初始logo**；接bootanimation.zip最后一帧，可以是mp4或者png图片，默认使用`gaia/shared/resources/branding/initlogo.png`，相关代码在`apps/system/js/init_logo_handler.js`(2.5R2)。
    <br>
    
* 关机动画在System应用中`init_logo_handler.js`。
    - `apps/system/resources/power/carrier_power_off.mp4`

---
#### Q. 开机的声音在哪控制？

* 原生不支持在`BootAnimation.cpp`中播放开机铃声，目前设计是在System应用中，因此开机铃声会晚于BootAnimation；参考`init_logo_handler.js`:

  ```
    _playDefaultPowerOnSound: function() {
      ...
      self.osLogoSoundElement = document.createElement('audio');
      self.osLogoSoundElement.src = '/resources/sounds/poweron-sound.ogg';
  ```
* 理论上可以修改`BootAnimation.cpp`在native层更早播放开机铃声，但部分平台未实现该功能。

---
#### Q. 如何配置手机的默认存储大小？
* 需要添加`device.storage.size`的pref。
```
// Config stroage size to 512MB
pref("device.storage.size", 512);
// Config stroage size to 4G
pref("device.storage.size", 4096);
```

---
#### Q. 请问software.version需要手动更新吗？Commercial name干什么用的？什么规则？build name需要手动更新吗？
- software.version对应版本号，有客户自行定义。假设每周出一个正式版本，那么需要客户手动更新它，而且新的版本号要高于旧版本号，因为FOTA根据它判断哪个版本更新一些。

- Commercial name也叫CU Ref，也是由客户自行定义，定义的规则参见百度云上的CU RERFRENCE RULE.pptx。请注意CU Ref对应产品，假设客户某项目有两个产品类型，一个单卡，一个双卡，分别对应两个软件版本，那么就需要两个CU Ref对应这两个软件版本，而且不会轻易变化。FOTA也会判断CU Ref，不同版本之间不能交叉升级。

- build name是自动生成的，用来区别不同人或者不同时间编译出的版本。

---
#### Q. 如何关闭SimBasedCustomization
如果开启了KaiOS的SIM based customization，但又没有真的配置对应sim的profile，则
会在首次开机或换sim卡后，提示“无法找到xxx运营商的profile”、“Can not find xxx profile"提示

如果你的产品没有计划配置某些运营商的profile以激活完整的SIM based customization
功能，或者你的客户已经在抱怨开机后这一提示，则可关闭这个功能。

很简单，可把这一行注释掉。

```
diff --git a/src/sim_config.js b/src/sim_config.js
index e3c5e16..78a1dd0 100644
--- a/src/sim_config.js
+++ b/src/sim_config.js
@@ -15,8 +15,8 @@ class SimConfig extends BaseModule {
     let lock = navigator.mozSettings.createLock();
     let req = lock.get('sim.base.customization.enabled');
     req.onsuccess = () => {
-      this.configEnabled = !!req.result['sim.base.customization.enabled'] ||
-        req.result['sim.base.customization.enabled'] === undefined;
+      this.configEnabled = !!req.result['sim.base.customization.enabled']; //||
+ //       req.result['sim.base.customization.enabled'] === undefined;
       this.checkSimConfig();
     };
     this.lastApplyIccId = localStorage.getItem('sim.config.apply.iccid');
```

还可参考： 
https://bugzilla.kaiostech.com/show_bug.cgi?id=57794
https://bugzilla.kaiostech.com/show_bug.cgi?id=53358

---
#### Q. Torch/手电筒 功能节点配置
A. 需要在releasenote中标明，节点路径需要odm配置在ro属性中。

ro.kaios.torch.node
ro.kaios.torch_enable_value
ro.kaios.torch_disable_value

ODM自己检测方法:

1. 是否包涵该节点配置
```
adb shell
getprop | grep torch
```

2. 配置的节点是否真正可用，可操作
```
adb root && adb shell
echo 1 > /sys/class/flashlight/torch/enable
echo 0 > /sys/class/flashlight/torch/enable
```


参考:

[release-note](https://git.kaiostech.com/quoin/release-note/blob/jio/Kaios_jio_quoin_20180308_7.pdf)

[bug59868](https://bugzilla.kaiostech.com/show_bug.cgi?id=59868)

---
#### Q. 如何定制 ringtones？
A. 主要步骤如下:

-  gaia/apps/ringtones/js/built_in_ringtones.js中,可以查看支持的内置铃声的格式有这些：
```
var mimeTypeMap = {
    '.mp3': 'audio/mp3',
    '.mp4': 'audio/mp4',
    '.ogg': 'audio/ogg',
    '.opus': 'audio/ogg',
    '.mid': 'audio/x-midi'
  };
```


-  铃声路径在  gaia/shared/resources/media/ringtones/目录中，并且在该目录的list.json中新增相关配置，请参照已有格式。

-  gaia\build\settings.js 文件里，
```
function setRingtone(settings, config) {
      // Grab ringer_firefox.opus and convert it into a base64 string
      let ringtone_name = 'ringer_kai.ogg';
      let ringtone_l10nID = 'ringer_kai';
      setTone(settings, config, 'ringtone', ringtone_name, ringtone_l10nID);
}
```
       其中   let ringtone_name = 'ringer_kai.ogg'; 是更改默认的铃声名字

-  在gaia/shared/locales/sounds/sounds.en-US.properties中，新增配置铃声，参照已经配置的格式。这步是解决本地化翻译。

-  编译命令： 
```
              APP=settings make install-gaia
              APP=ringtones make install-gaia
```

---
#### Q. 配置默认的键盘输入法

gaia/build/config/common-settings.json

  "keypad.layouts.english_us": true,
  "keypad.layouts.french_ca": false,
  "keypad.layouts.portugese_br": false,

....

想要默认为法语,那么法语置true,其他置false即可

---
#### Q. 如何预置一个快速拨号的号码

例如把5变成一个显示为“SOS”的号112的快速拨号

Config a setting DB key as below:

file location: gaia/distribution/settings.json


"custom.speeddials":[{"key":5,"name":"SOS","tel":112}]


and this function is handle by Launcher application, you may read it for more information. 
launcher/src/speed_dial_store.js
launcher/src/speed_dial_helper.js

(info from Guang)

---
#### Q. 如何修改应用的图标？

A. 在kaiOS主菜单显示的图标，是属于app的图标。分几种情况：

1. OEM客户可以修改KaiOS发布了源码的、KaiOS自主App的图标。而KaiOS自主App中
“不”提供源码的App，截止2019年6月，只有KaiStore，它的应用图标OEM不可以修改。

2. OEM/ODM不可以修改任何预置的第三方App的图标，包括但不限于Google、Whatsapp、
Facebook等知名应用的图标。它们多数本质上不是KaiOS和OEM的知识产权，因此不可以
被OEM修改甚至替换，且多数受到OEM和KaiOS授权合同中关于App布局要求的严格约定，
例如Assistant，facebook, WA等。修改它们的应用图标在后续的认证中受阻。

第三方App的源码并未由KaiOS提供，但某些App图标恰好是明文存储的——请不要误以为这些App图标可以被替换。

最后，技术上替换是不会一直“有效”的。这些App，包括KaiStore，都通过kaiStore在线升级。
一旦升级，图标会被新版本替换。有些Hosted app甚至不需升级，只需服务激活和使用，就能自更新App图标，如Youtube。 

---
#### Q. KaiOS如何管理图标资源-Icon资源 - Icon LOGO Resource rff 字体 font 
A. 基本分为两部分
1. gaia-icons里面的都是系统图标，用在状态栏显示上。
他们的kaios自己的参考源文件在代码的位置是
./gaia/shared/gaia-icons/tree/master/images
OEM应该是有权限来获取shared这个git的，在这个下面有单独的图标文件，并不是ttf的,可以识别出每个图标的名字，用于调用。但这些资源并不直接被代码调用，而是转换成ttf。
OEM计划替换图标的话，需要替换的是ttf文件。
新创一个图标也要遵循这个代码逻辑。

2. 各个应用自己的图标，这个在每个单独的应用里面存在，现在并没有一个完整的包来专门存放。比如clock这个应用，它的图标在clock/style/icons/下面。其他的应用也是类似的。

---
#### Q. 如何客制化小图标gaia-icons
gaia-icons.ttf通过字体工具[ttfautohint](https://www.freetype.org/ttfautohint/index.html)把简单图片字库化的处理后生成的字库文件。系统内部通过在html中添加`data-icons="play"`,或者`element.setAttribute('data-icon', 'play')`的方式，向元素上添加图片。

客制化的方式如下：

+ **仓库创建与维护**: 在github(或者其他git服务器)基于KaiOS [gaia-icons](https://git.kaiostech.com/shared/gaia-icons) 维护一个客户自己的gaia-icons的仓库。如果没有获取该仓库的权限，请找项目的PM。并且需要在每次需要把KaiOS对gaia-icons的更新同步到这个仓库里面.[例子](https://github.com/why19861124/gaia-icon)

+ **字体生成与预览**: 参考KaiOS gaia-icons 中的 [README.md](https://git.kaiostech.com/shared/gaia-icons/blob/master/README.md)，尝试生成包涵特殊客制化小图标的gaia-icons.ttf。
生成TTF文件之后可以通过浏览器直接打开gaia-icons中的index.html来预览添加的图片，是否添加成功并且显示正常。推荐使用[Ubuntu 18.04.2 LTS](https://ubuntu.com/download/desktop/thank-you?version=18.04.2&architecture=amd64)来进行字库生成及维护。


+ **更新资源文件**: 在gaia-icons定制好之后，需要将系统中的文件替换掉。

  [1]更新 `gaia\shared\elements\gaia-icons\fonts\gaia-icons.ttf`

  [2]查看需要添加客制化icon的应用，在应用的一级目录下是否包涵`package.json`且其中`dependencies`字段的属性中有`"gaia-icons": "git+ssh://git@git.kaiostech.com:shared/gaia-icons.git"`, 如果包涵把改条属性的值换成**仓库创建与维护**的路径即可,否则不用做任何修改。
    ```
    "gaia-icons": "git+ssh://git@git.kaiostech.com:shared/gaia-icons.git"
    =>
    "gaia-icons": "url-of-the-project-maintain"
    ```

+ **常见问题**
  1. 执行grunt时出现：

      `
      Running "webfont:files" (webfont) task
      *** Error in `ttfautohint': malloc(): memory corruption: 0x0000000001b7e620 ***
      Font gaia-icons with 403 glyphs created.

      Running "webfont:embedded" (webfont) task
      *** Error in `ttfautohint': malloc(): memory corruption: 0x0000000001466620 ***
      Font gaia-icons with 403 glyphs created.
      `

      A: 编译环境需要Ubuntu 18.04.2 LTS


Ref: [bug61033](https://bugzilla.kaiostech.com/show_bug.cgi?id=61033)

#### Q. 关于不插SIM卡时的紧急电话号码定制 - Emergency Call  ECC number 

拨打紧急电话emergency call（ECC）的通话不是一个普通的电话呼叫业务。

每个国家/地区固定的紧急电话emergency call的号码识别和建立是modem侧配置的，
各个平台厂商有不同的实现细节，但基本上都是一个根据MCC配置的表格，且“各自”都有例
行维护。

若当在某个国家测试时发现紧急电话的号码的识别不正常时，应将bug提交给平台厂商研究
而不是交给KaiOS。
//////
不插入SIM卡的情况下，因为MCC为空，不入网，不知道国家，此时紧急电话号码的识别
需要KaiOS一侧代码和平台厂商的ECC功能合作实现。

大致思路是:
1,在no-sim(sim还没有识别)的时候,将ril.ecclist替换成 ro.ril.nosim.ecclist.
2,有卡后再将ril.ecclist替换回原来的ecclist.

－－－－－－－－以下为参考代码－－－－－

```
diff --git a/vendor_ril/icc/IccService.js b/vendor_ril/icc/IccService.js
index 839789d..bcf010a 100755
--- a/vendor_ril/icc/IccService.js
+++ b/vendor_ril/icc/IccService.js
@@ -8,6 +8,7 @@ const {classes: Cc, interfaces: Ci, utils: Cu, results: Cr} = Components;
 
 Cu.import("resource://gre/modules/XPCOMUtils.jsm");
 Cu.import("resource://gre/modules/Services.jsm");
+Cu.import("resource://gre/modules/systemlibs.js");
 
 var RIL = {};
 Cu.import("resource://gre/modules/ril_consts.js", RIL);
@@ -244,12 +245,60 @@ IccService.prototype = {
       ._deliverListenerEvent("notifyStkSessionEnd");
   },
 
+  _updateEccList: function(aServiceId, aCardState) {
+    if (DEBUG) {
+      debug("_updateNoSimEccList for service Id: " + aServiceId +
+            ", CardState: " + aCardState);
+    }
+    //Sub 0 is the default sub for emergency call if no sim.
+    if(aServiceId !== 0) {
+      return;
+    }
+    let eccKey = "ril.ecclist";
+    let roEccNoSimkey = "ro.ril.nosim.ecclist";
+    let origEccKey = "ril.old.ecclist";
+
+    //Card absent
+    if (aCardState === Ci.nsIIcc.CARD_STATE_UNKNOWN ||
+        aCardState === Ci.nsIIcc.CARD_STATE_UNDETECTED) {
+      if (DEBUG) {
+        debug("Sim not present, update ecclist to sim absent ecclist");
+      }
+
+      let noSimEcclist = libcutils.property_get(roEccNoSimkey, "");
+      try {
+        if(noSimEcclist !== "") {
+          let origEcclist = libcutils.property_get(eccKey, "");
+          libcutils.property_set(origEccKey, origEcclist);
+          libcutils.property_set(eccKey, noSimEcclist);
+        }
+      } catch (e) {
+        dump("update sim absent ecclist with error " + e);
+      }
+    } else {//Card present
+      if (DEBUG) {
+        debug("Sim present, update ecclist to ro.ril.ecclist");
+      }
+
+      let origEcclist = libcutils.property_get(origEccKey, "");
+      try {
+        if(origEcclist !== "") {
+          libcutils.property_set(eccKey, origEcclist);
+          libcutils.property_set(origEccKey, "");
+        }
+      } catch (e) {
+        dump("update sim present ecclist with error " + e);
+      }
+    }
+    return;
+  },
   notifyCardStateChanged: function(aServiceId, aCardState) {
     if (DEBUG) {
       debug("notifyCardStateChanged for service Id: " + aServiceId +
             ", CardState: " + aCardState);
     }
 
+    this._updateEccList(aServiceId, aCardState);
     this.getIccByServiceId(aServiceId)._updateCardState(aCardState);
   },
```
 
（Info from Tao）

---
## API使用

#### Q. 是否能提供详细的KaiOS App层的API文档
A. Mozilla网站上发布了大部分api, 只有少数kaios新加的需要直接查代码，并不多。

- https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API

---
#### Q. BOM/DOM讲解
A. 都是标准的，可以从网络搜索资源，下面是一些例子：

- http://blog.csdn.net/qq877507054/article/details/51395830
- http://blog.csdn.net/xiao_tommy/article/details/53231165

也可以参考《Javascript从入门到精通》等类似的书籍。

---
#### Q. web-api讲解
A. 是标准的，可以从网站上搜索得到，下面是一些资源：

基础的讲解：
- https://www.cnblogs.com/guyun/p/4589115.html

深入点的讲解：
- http://www.yuanjiaocheng.net/webapi/first.html

适用于KaiOS的讲解：
- https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API

---
#### Q. kaios是否有扩展的api，请介绍。
A. 扩展的不多，具体不遇到也不会用到，遇到了就去gecko查一下。然后kaios新加的库大部分放在gecko/koost目录下。

---
#### Q. KaiOS如何使用Telepony.dial/dialEmergecy API接口
A. 应用中可以使用 navigator.mozTelephony.dial(number, type, sRtt, serviceId);

详细参考:
```
  /**
   * Make a phone call with specific type or send the mmi code depending on the number provided.
   * @param type
   *        The call type you are going to dial.
   *        One of Telephony.CALL_TYPE_* values.
   * @param isRtt
   *        Is it a Real-Time-Text call.
   *        RTT call is only applicable to LTE only.
   * TelephonyCall - for call setup
   * MMICall - for MMI code
   */
  [Throws]
  Promise<(TelephonyCall or MMICall)> dial(DOMString number, unsigned short type, boolean isRtt, optional unsigned long serviceId);

  [Throws]
  /**
   * @param isRtt
   *        Is it a Real-Time-Text emergency call or not.
   *        RTT call is only applicable to LTE only.
   */
  Promise<TelephonyCall> dialEmergency(DOMString number, boolean isRtt, optional unsigned long serviceId);
```
code from dom/webidl/Telephony.webidl

It is not yet update in MDN:
https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/Telephony/dial

---
#### Q. 如何读取SIM卡中的STK Name
A. 可以参考如下的文件：
- gaia/apps/system/js/icc_worker.js
- gaia/apps/settings/js/icc.js
- gaia/apps/system/src/stk_dialog.js
- gaia/apps/system/js/icc.js

在icc_worker.js 中，有一些处理 对应stk 命令的处理函数 例如： '0x15': function STK_CMD_LAUNCH_BROWSER
找相应的处理函数，可以先到icc_worker.js 中找。

```
    var icc_worker = {
        ...
        // STK_CMD_LAUNCH_BROWSER
        '0x15': function STK_CMD_LAUNCH_BROWSER(message) {
        DUMP('STK_CMD_LAUNCH_BROWSER:', message.command.options);
        var options = message.command.options;

        if (options.confirmMessage) {
        icc.discardCurrentMessageIfNeeded(message);
        }

        icc.responseSTKCommand(message, {
        resultCode: icc._iccManager.STK_RESULT_OK
        });
        var text = '';
        if (!STKHelper.isIconSelfExplanatory(options.confirmMessage)) {
        text = STKHelper.getMessageText(options.confirmMessage);
        }
        var icons = options.confirmMessage ? options.confirmMessage.icons : null;
        icc.showURL(message, options.url, icons, text);
        },
        ...
    }
```

---
#### Q. KaiOS系统中怎么判断不同运营商(以便根据不同运营商切换4G和LTE图标)
A. 请参考 apps/system/js/operator_variant_handler.js 中的：

```
    var request = iccCard.matchMvno(listMvnoType, listMvnoMatchData);
```

---
#### Q. iccCard.matchMvno函数返回的值是什么，是运营商名还是MCC号之类。是否支持全部 DSD Setting 中的运营商。Statusbar.js中怎么调用operator_variant_handler中的这个函数来获取request值。
A. matchMvno是个api, 返回的是个bool值，获取方式参考 apps/system/js/operator_variant_handler.js 中的

```
    var iccCard = navigator.mozIccManager.getIccById(this._iccId);
    var request = iccCard.matchMvno(listMvnoType, listMvnoMatchData);
```

---
#### Q. 状态信号图标中的dataIcon显示的4g和lte图标在apps\system\js\statusbar.js，icon.dataset.icon = type;设置。可以根据type选择系统已有的信号图片，但是图片本身没找到，请问怎么自己修改图片。
A. 这个是font的处理方法。使用一张图片 /KaiOS/apps/system/style/statusbar/images/icon.png，要修改就修改这个图片，会根据key去显示对应的部分。statusbar.css里面会根据 `sb-icon-xxx` 来规定每个图标显示的属性。

---
#### Q. ril.data.enabled属性设置为true后，signal信号图标旁边会显示的4G/LTE图标，这个dataIcon图标怎么替换图片资源，除了在代码中修改icon.dataset.icon = type。
A. 这个icon.dataset.icon = type;对应的就是：

```
    mobileDataIconTypes: {
        'lte': 'lte', // 4G LTE
        'ehrpd': '4g', // 4G CDMA
        'hspa+': 'hspa-plus', // 3.5G HSPA+
        'hsdpa': 'hspa', 'hsupa': 'hspa', 'hspa': 'hspa', // 3.5G HSDPA
        'evdo0': 'ev', 'evdoa': 'ev', 'evdob': 'ev', // 3G CDMA
        'umts': '3g', // 3G
        'tdscdma': '3g', // TDS-CDMA
        'edge': 'edge', // EDGE
        'gprs': '2g',
        '1xrtt': '1x', 'is95a': '1x', 'is95b': '1x' // 2G CDMA
        // TODO: iwlan, lte_ca types also need to be considered.
    },
```

mobileDataIconTypes 里面的数据对应的是, /KaiOS/gaia/shared/elements/gaia-icons/fonts/gaia-icons.ttf 里面的图名。如果需要增加资源，需要修改ttf并且把名字修改到 mobileDataIconTypes 里面。

---
#### Q. KaiOS如何获取网络的MCC和MNC，如何读取SIM卡中的IMSI号？
A. mcc mnc 和 imsi 都可以在 iccinfo　api 中获取，参见链接：
- https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/MozMobileCCInfo

---
#### Q. MozMobileICCInfo.mcc和MozMobileICCInfo.mnc就是手机上的SIM卡的运营商的MCC和MNC号以及MozMobileICCInfo.spn是SIM卡的Network名，对吗？但是MozMobileICCInfo是个Interface，获取SIM卡的MNC和MCC号的具体调用怎么写？
A. 是的，是sim卡的MCC/MNC，具体调用请参考app/system/js/app_usage_metrics.js。app通过接口获取信息可以参考api网站，也可以在app里面去查找相关代码。

---

#### Q. 是否处于漫游状态的图标判定在
A. `apps\system\js\statusbar.js`

```
    var simSlots = SIMSlotManager.getSlots();
        var isDirty = false; // Whether to reprioritise icons afterwards.
        for (var index = 0; index < simSlots.length; index++) {
            var simslot = simSlots[index];
            var conn = simslot.conn;
            var voice = conn.voice;
            var data = conn.data;
```

#### Q. roaming.hidden = !connInfo.roaming; 这一句但是属性roaming的值是在哪里设置的。
A. navigator.mozMobileConnections[0].data.roaming，也是API参考:
- https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/MozMobileConnection

或者
- https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/MozMobileConnectionInfo

如果是双卡，可以使用navigator.mozMobileConnections[1].data.roaming查询另一张卡。

---
#### Q. API中获取的是subscriber's home network。我需要根据sim卡的MCC和MNC以及网络获取的MCC和MNC对比，如果同属于National roaming pair中的MCC和MNC即使是不同网络也不算是漫游状态，请问怎么获取当前所在地网络的MCC和MNC。
A. 请参考下面的信息，应该是只要配置一下就可以了。QCOM平台在vendor里面配置 config_same_named_operator_considered_non_roaming 配置上就可以了。vendor/qcom/property/b2g_telephony/config/。这个上面的目录搜这个，配置上就可以了。

`
    bool ServiceStateTracker::IsOperatorConsideredNonRoaming
`

这个是code : vendor/qcom/property/b2g_telephony/ServiceStateTracker.cpp

另外MCC/MNC如何获取：

sim卡归属：　

```
    navigator.mozIccManager.getIccById('89860116831018622993').iccInfo.mcc
    navigator.mozIccManager.getIccById('89860116831018622993').iccInfo.mnc
```

当前网络：
```
    navigator.mozMobileConnections[0].data.network.mcc
    navigator.mozMobileConnections[0].data.network.mnc
```

---
#### Q. KaiOS界面加载的都是本地资源，为什么还是感觉很慢(比如Setting中各个选项的summary副标题要在打开整体界面后几秒才显示出来)。加载速度是否能优化。
A. 现在的机制是先加载html，然后有选择的加载js文件。有一些js是延后加载的。所以用户实际看到的效果是先看到页面，然后内容才会更新显示。这个也在持续优化中，但是目前余地不是很大。

---
#### Q. 是否有完整的app的Permissions列表说明
A. 请参考 /gecko/dom/apps/PermissionsTable.jsm

```
    this.PermissionsTable =  { geolocation: {
                                app: PROMPT_ACTION,
                                privileged: PROMPT_ACTION,
                                certified: PROMPT_ACTION
                            },
                            "geolocation-noprompt": {
                                app: DENY_ACTION,
                                privileged: DENY_ACTION,
                                certified: ALLOW_ACTION,
                                substitute: ["geolocation"]
                            },
```
---
#### Q. webapp和gaia，gecko以及webapp之间的通信
A. 目前webapp之间的通信可以选择用IAC方式来通讯。可以参考/apps/launcher/src/util/dial_helper.js里面的电话处理过程（mmi_handler）。gecko之间用xpcom(idl)调用，和库调用类似。gecko通过webidl 将接口暴露给gaia
。
```
  mmiHandler(promise, sentMMI) {
    this.mmiloading = true;
    this.emit('mmiloading');
```

---
#### Q. webapp可使用存储方式有哪些，如何使用。比如如何用数据库，怎么保存一些简单的config等
A. 一般存储使用indexDB和preference，app一般不会直接操作数据库，具体操作放在gecko中处理，暴露接口出来给gaia使用，比如系统级别的配置可以保存到settings数据库中，具体接口如下，很多app都有使用可以在代码里面查到：

```
navigator.mozSettings.createLock().set(｛key:value｝);
navigator.mozSettings.createLock().get(key)；
```

key的定义可以放在 common-settings.json 里面。
它对indexＤＢ的操作实际放在了gecko: /gecko/dom/settings/SettingsDB.jsm里面。

---
## 系统应用
### 编译

#### Q. 为什么apps-production.list没有的app，仍然在应用里看得到(如Browser)
A. Browser应用实际的名字是Search。

---
#### Q. Gaia编译中的参数作用，需要讲解一下最常用的几个
A. 请参考/gaia/README.md文件里的说明。常用的几个如下：

Removing everything and install a clean profile

`make reset-gaia`

Enabling debugging mode on the device

`DEVICE_DEBUG=1 make install-gaia`

Building Gaia locally without a network connection

`OFFLINE=1 make install-gaia`

Keeping React apps clean when build failed

`GAIA_PRISTINE=1 make install-gaia`

Building Gaia without re-bundling apps

`make install-gaia NO_BUNDLE=1`

Building a specific Gaia app

`make install-gaia APP=search`

Building Gaia with low memory specific configurations

`GAIA_MEMORY_PROFILE=low make install-gaia`

---
#### Q. 关于编译命令，如何单编模块或应用，编译后如何打包进system img
A.

单独编译模块：
- 连接手机, `adb root;adb remount;adb shell`
- 单独编译app，在 /gaia 目录下，`make install-gaia APP=xxx`

整编gaia:

`make reset-gaia`

不需要重新打包system.img，通过上述命令可以直接把编译后的应用安装到手机中。
如果想仅仅更新system.img，参考如下命令：

- `adb reboot bootloader`
- `sudo fastboot flash system out/target/product/msm8909_512/system.img`
- `sudo fastboot reboot`


#### Q. app在编译的时候会被重新配置，比如拷贝shared库到app目录，修改index.html和webapp.manifest等，能否简单介绍一下这个过程？
A. 编译react JS编写的应用的时候，会从网络下载相关的依赖包，这个在yarn.lock文件定义，生成node_modules文件夹，同时，如果有需要，也会从/gaia/shared/locales下的文件夹拷贝一些文件，比如voice mail等等，主要是功能相关的一些字符串。一般来讲，不需要改动这部分机制，如果想深入了解，请参考gaia下的make文件。

#### Q. gaia和app之间的联系和区别？？settings中的一些数据放在gaia中的为什么不直接放在setting中。apps中某一个app比如setting中的数据在gaia目录下，他们是怎么通讯的
A. 目前常用的通讯方式是IAC(Inter Application Communication)gaia里面放的一些公用的文件和资源，app只管自己。一般直接在app html文件引用或者使用load函数导入。

---
#### Q. 想删某个app，是直接删除源码，还是修改某个文件让某个app不编译
A. 修改Gaia/build/config下面的几个文件，把不需要参加编译的应用去掉就行了。

- /gaia/build/config/phone/apps-engineering.list
- /gaia/build/config/phone/apps-production.list

#### Q. 如何修改Node_Modules的代码.
问题：OEM/ODM在开发中，会遇到需要修改launcher\node_modules下面js代码的情况，而这部分代码是首次编译时从.yarn_mirror里面释放出来的，如何保留OEM/ODM自己的修改？
A. 可以参考/gaia/build/build-bundle.sh 中的
```
# Build React app
# Arguments:
#   appDir
build() {
    local -r appDir=$1
    local -r appName=$(basename "$appDir")
    pushd "$appDir"
    {
        out "Compiling '$appName' app..."

        # Install node modules for system/remote
        if [[ "$appName" == 'system' ]]; then
            pushd remote
            {
                out "Installing node modules for '$appName/remote'..."
                trap 'cleanup "$appName/remote"; exit' INT TERM EXIT
                yarn
                trap - INT TERM EXIT
            }
            popd
        fi

        trap 'cleanup "$appName"; exit' INT TERM EXIT
        yarn && make -j 2
        trap - INT TERM EXIT
    }
    popd
    pass "'$appName' app build succeeded."
}
```

在执行完yarn之后，尝试copy你们需要的文件。

#### Q. 如何预置或push应用到测试机中
A. 
***App 预置方法：
1.将应用目录拷贝到app目录下，应该有三个文件（application.zip/metadata.json/update.webapp）.如果是Host app有两个文件（manifest.webapp/metadata.json）。
2.将路径配置到gaia/build/config/phone/apps-production.list, 文件夹名字保持一致就可以了。（比如：Search文件夹改成googlesearch，配置就是apps/googlesearch）.

***WebIED 安装：
1.安装需要manifest.webapp这个文件， 所以解压application.zip.
2.手机连接webIDE, Open Packaged APP打开解压后的文件夹。点击中间三角按钮安装。

（KaiOS没有SD卡app安装功能）

***另外这些预置入的app需要和app store关联起来的。
***App的是在name在application.zip里面的manifest.webapps 配置的，不是zip包名字。


***App preinstall:
1. Copy the app to app folder. Should be three files(application.zip/metadata.json/update.webapp).  Two files(manifest.webapp/metadata.json) for Host App.
2. Config the path in gaia/build/config/phone/apps-production.list. Keep the folder name consistant. E.g. Rename Search to googlesearch. Then the config should be apps/googlesearch.

***WebIDE install:
1. unzip application.zip. The install need manifest.webapp file.
2. Phone connect to webIDE. Open the folder of unzipped APP. Click the triangle button to install.

***Preinstalled app must be compatible with the apps defition of Store for this model. 

---
#### Q. 编译时怎么取消代码混淆
分两部分：

+ 单独编译某个应用时用`APP=xxx GAIA_OPTIMIZE=0  make install-gaia`；修改编译系统gaia/Makefile 中所有GAIA_OPTIMIZE赋值的时候都设为 0

+ 如若编译的目标应用还是react应用的话，还需要修改webpack配置文件: `webpack.config.prod.js`, 去掉插件[UglifyJsPlugin](https://webpack.js.org/plugins/uglifyjs-webpack-plugin/).

```
return [new webpack.DefinePlugin(defineOptions)]
    .concat(plugins || [])
    .concat([
      new UglifyJsPlugin({uglifyOptions: uglifyOptions})
    ]);

==>

return [new webpack.DefinePlugin(defineOptions)]
    .concat(plugins || []);
```

---
### 国际化

#### Q. apps\clock\locales\es\clock.en-US.propertperties和gaia\locales\en-US\apps\clock\ck\clock.propertperties间有什么联系么？
A. Gaia下面的文件是把所有的字符串翻译过之后的文件。在编译的时候，会从这个文件重新生成apps下面的对应语言文件。

---
#### Q. 在 .properties文件中定义的字符串，在显示出来（标题或左右键）第二个单词的首字母会自动变为大写。如：定义的为：clear all 显示出来为：Clear All。这种情况在哪里可以控制么？
A. 在app.css里面，sk-button有个属性，capitalize，每个单词的首字母都会大写，写成none就行。

#### Q. 哪里查找国家或地区的语言代码（language ID）
请参考华天虎先生在线帖子。
https://www.cnblogs.com/Robert-huge/p/5481515.html

#### Q. 阿拉伯语数字显示习惯切换，Arabic，number，character，Arabian

KaiOS有一个功能可以将所有菜单翻译（包括状态条中的时间区域）中的数字，按照数字选择用阿拉伯数字 1/2/3/4/...显示，还是用阿拉伯问的数字字符显示，就如同可以在汉语中自动将字符串中的1/2/3翻译成一/二/三
这个功能的开关是gecko中的pref
“bidi.numeral”  
该值选4，则所有菜单翻译中的阿拉伯数字显示为阿拉伯字符
该值设0，该转换功能关闭。
(info from Jin) 

#### Q. 如何缩短语言列表以节省系统ROM占用-System Partition Menu Memory Input method storage language list
HowToReducelanguageslist-SystemPartition
翻译和输入法资源存储在system partition，无用资源太多会减少未来FOTA次数。
KaiOS有一个文档 “如何缩短语言列表以节省系统ROM占用-HowToReducelanguageslist-SystemPartition Menu Input-20190423.doc”
如果你的项目是256MB内存，512MB ROM，请向KaiOS CPM索要此文件。

---
### 系统 - apps/system

#### Q. KaiOS的SystemUI是在哪个目录里控制的,因为在frameworks里的SystemUI中修改无效

A. 在KaiOS中，有2个应用会涉及到system UI:
- apps/system
- apps/launcher

---
#### Q. 请介绍系统通知（比如电量，时间，信号强度变化等等）实现机制及如何使用
A. 状态栏大部分在 app/system/js/statusbar.js 中出里，一般都是监听gecko上报的消息处理显示。

---
#### Q. 长按#键只需要一般模式和静音模式间切换
和Kai设计的相左的特殊需求，不能进分支。
需在system-dev的sound-store.js 或者 system的sound-manager.js 修改`holdhash`的响应。

Patch for system-dev
```
diff --git a/src/sound_store.js b/src/sound_store.js
index 4037132..49f205a 100644
--- a/src/sound_store.js
+++ b/src/sound_store.js
@@ -322,7 +322,15 @@ class SoundManager extends BaseModule {
     if (Service.query('getTopMostWindow').isHomescreen &&
         Service.query('getTopMostWindow').isFocusedInApp() &&
         Service.query('getTopMostUI').name === 'AppWindowManager') {
-      this.toggleVibrate();
+      if (this.currentVolume['notification'] === 0) {
+        if (this.vibrationEnabled) {
+          this.setMute(true);
+        } else {
+          this.setMute(false);
+        }
+      } else {
+        this.setMute(true);
+      }
     }
   }

@@ -874,7 +882,7 @@ class SoundManager extends BaseModule {
       // At least rollback to 1,
       // otherwise we don't really leave silent mode.
       settingObject['audio.volume.' + channel] =
-        (this.cachedVolume[channel] > 0) ? this.cachedVolume[channel] : 1;
+        (this.cachedVolume[channel] !== 0 ) ? this.cachedVolume[channel] : 1;

       this.pendingRequest.v();
       SettingsStore.set(settingObject).then(() => {
```

Patch for system:
```
diff --git a/js/sound_manager.js b/js/sound_manager.js
index fb6a897..db8c767 100644
--- a/js/sound_manager.js
+++ b/js/sound_manager.js
@@ -287,7 +287,15 @@
         if (Service.query('getTopMostWindow').isHomescreen &&
             Service.query('getTopMostUI').name === 'AppWindowManager' &&
             document.activeElement.tagName.toLowerCase() === 'iframe') {
-          this.toggleVibrate();
+          if (this.currentVolume['notification'] === 0) {
+            if (this.vibrationEnabled) {
+              this.setMute(true);
+            } else {
+              this.setMute(false);
+            }
+          } else {
+            this.setMute(true);
+          }
         }
         break;
       case 'volumeup':
@@ -854,7 +862,7 @@
       // At least rollback to 1,
       // otherwise we don't really leave silent mode.
       settingObject['audio.volume.' + channel] =
-        (this.cachedVolume[channel] > 0) ? this.cachedVolume[channel] : 1;
+        (this.cachedVolume[channel] !== 0) ? this.cachedVolume[channel] : 1;

       this.pendingRequest.v();
       if (channel === this.getChannel()) {

```

refbug:

[bug 64765](https://bugzilla.kaiostech.com/show_bug.cgi?id=64765)

[bug 60531](https://bugzilla.kaiostech.com/show_bug.cgi?id=60531)

#### Q. 通话过程中来短信，alert&vibrate
- 通过修改通话过程中ringtone的AudioChannel来改变Audio Policy,来改变notification_toaster的行为。具体音频策略可以查看：apps/system/js/audio_channel_policy.js
```
--- a/src/notification_toaster.js
+++ b/src/notification_toaster.js
@@ -76,13 +76,18 @@ class NotificationToaster extends BaseComponent {
     var manifestURL = this.state.notification.manifestURL;
     if (!this.silent) {
       var ringtonePlayer = new Audio();
-
+      var telephony = navigator.mozTelephony;
       if (behavior) {
         ringtonePlayer.src = behavior.soundFile || this._sound;
       } else {
         ringtonePlayer.src = this._sound;
       }
-      ringtonePlayer.mozAudioChannelType = 'notification';
+      if (telephony && telephony.active) {
+        ringtonePlayer.mozAudioChannelType = 'publicnotification';
+        ringtonePlayer.volume = 0.3;
+      } else {
+        ringtonePlayer.mozAudioChannelType = 'notification';
+      }
       ringtonePlayer.play();
       window.setTimeout(function smsRingtoneEnder() {
         ringtonePlayer.pause();
```

---
#### Q. 为什么通知中已经存在的旧消息不能随系统语言切换
为什么即使system通知如 "SIM changed" 或 "Battery full"等也不能随系统语言切换而切换？
A. This is how it designed. 
Notification api 收到的参数统一是字符串内容，而非String ID，因此不能随着系统语言动态切换。

---
#### Q. Instance settings 手电筒，亮灭状态没法跟踪系统实际状态
有一笔提交在[bug39276](https://bugzilla.kaiostech.com/show_bug.cgi?id=39276) 没有被合并到kaios2.5 客户分支。

会导致诸如:

Bug 59765 - 重启手机，按上键进入常用设置，Flashlight下方不显示字体on或off

Bug 64945 - 【系统APP】【手电筒】在状态栏打开手电筒，进入相机，手电筒不会自动关闭，退出相机，手电筒不亮，但通知栏手电筒图标仍是开启状态

之类的问题，请知悉。

Patch 如下：
```
diff --git a/src/util/flashlight_helper.js b/src/util/flashlight_helper.js
index 8807847..b9a36e1 100644
--- a/src/util/flashlight_helper.js
+++ b/src/util/flashlight_helper.js
@@ -5,9 +5,11 @@ class FlashlightHelper extends BaseModule {
 
   constructor(props) {
     super(props);
+    this.capability = false;
 
     // Do feature detection for flashlight.
     if (navigator.getFlashlightManager) {
+      this.capability = true;
       navigator.getFlashlightManager().then(this.init.bind(this));
     }
   }

```

#### Q. 开启按键震动后，为什么Launcher和主菜单的按键都没有震动效果？
A. 该问题只存在于KaiOS R1分支中，可参考如下代码修改客户产品代码
 apps/system/src/hardware_button.js里面的逻辑：

```
       throw 'Instance should not be start()\'ed twice.';
     }
     this._started = true;
+    this.key = {};
     // Kick off the FSM in the base state
     this.state = new HardwareButtonsBaseState(this);
@@ -272,12 +273,27 @@
    * @param  {Object} evt Event.
    */
   HardwareButtons.prototype.handleEvent = function hb_handleEvent(evt) {
-    // console.log(evt.type, evt.key);
-    if (evt.type === 'keydown' &&
-        evt.key !== 'flip' &&
-        this._vibrationEnabled) {
-      navigator.vibrate(50);
+    if (this._vibrationEnabled && evt.key !== 'flip') {
+      switch (evt.type) {
+        case 'mozbrowserbeforekeydown':
+          this.key[evt.key] = evt.type;
+          break;
+        case 'keydown':
+          if (this.key[evt.key]) {
+            delete this.key[evt.key];
+          }
+          navigator.vibrate(50);
+          break;
+        case 'mozbrowserafterkeydown':
+          if (this.key[evt.key]) {
+            navigator.vibrate(50);
+            delete this.key[evt.key];
+          }
+          break;
+      }
```

#### Q. 如何修改#号键的长按行为

A. 假如，需要长按#静音，是在apps/system/js/sound_manager.js 中修改，
可以尝试在这个文件里面的holdhash事件中处理：
```
SoundManager.prototype.handleEvent = function sm_handleEvent(e) {
  switch (e.type) {
      case 'holdhash':
      case 'hold4':
        if (Service.query('getTopMostWindow').isHomescreen &&
            Service.query('getTopMostUI').name === 'AppWindowManager' &&
            document.activeElement.tagName.toLowerCase() === 'iframe') {
          this.toggleVibrate();
        }
        break;
      ...
    }
}
```

#### Q. 如何实现对耳机插拔动作的识别和弹窗用户提示 
A.可尝试如下代码
在sound_store.js里面，
```
  setHeadsetState(enabled) {
    if (this.isHeadsetConnected === enabled) {
      return;
    }
    this.isHeadsetConnected = enabled;
    this.publish('headphones-status-changed', this.isHeadsetConnected);
    if (this.isHeadsetConnected) {
      Service.request('showIcon', 'HeadphoneIcon', <HeadphoneIcon />);
+      Service.request('SystemToaster:show', {
+        text: navigator.mozL10n.get('StringID-to-show'),
+        timeout: 1500
+      });
    } else {
      Service.request('hideIcon', 'HeadphoneIcon');
    }
  }
```
（Info from Sheldon in case 60849)

---
#### Q. 关于密码输入格式错误的注意-pin code input method.20190101
所有关于pin code输入格式相关问题的bug必须提供视频。因为pin code输入界面太多，
名称都很近似，处理问题的工程师需要明确了解具体页面后，才能准确判断该页面输入格式
是kaios原生设计的问题，还是客户在定制时无意改变了上下文设置的输入方式。

---
### 输入法 - apps/keyboard

#### Q. 关于输入法按键/键盘配置的提醒 - 输入法,语言,阿拉伯语,全键盘, QWERTY,丝印,keyboard
A. OEM/ODM确认键盘的硬件印刷细节时应注意此问题：
对于12键传统键盘，KaiOS只定义了英文输入对应的键盘布局，其他语种都没有定义，第三方输入法集成后每个按键输出的字符是输入法定义的。
全键盘布局在手机行业更没有统一标准，还涉及ALT/Shift类按键功能的定义，项目应该立项时和KaiOS及输入法供应商讨论键盘设计的可行性。

KaiOS没有默认联想输入法，想要支持联想输入，一定在依赖第三方解决方案。

某些小语种因为字符数量多，键盘上符号位置和布局可能没有国际通行标准。如果产品键盘需要丝印字符，应先同输入法厂商确认双方的按键/键盘定义是否一致。

输入法厂商切换不同键盘布局标准可能不是免费的，要切记。

每个小语种键盘设计一定要先和输入法厂商直接确认，再生产。如果按照既往习惯采用某个设计和按键印刷方式，因为国内普遍无法测试到，恐怕最后客户见到样机才能发现手机输出的符号和键盘上印制的是不一致的，此时发现，就太晚了。

---
#### Q. 如何全局音量调整菜单时长 （global volume timer） 

kaios的全局音量调整页面的默认时间是2秒。如果要调短，可参考如下patch。注意不要改错js文件！！

```
diff --git a/src/sound_view.js b/src/sound_view.js
index 308416187..67ab8f0b8 100644
--- a/src/sound_view.js
+++ b/src/sound_view.js
@@ -9,7 +9,7 @@ export default class SoundView extends BaseComponent {
 
   DEBUG = false;
 
-  TIMEOUT = 2000;
+  TIMEOUT = 500; // This value depends on your needs,for exampe, I set TIMEOUT = 500, The larger the value, the slower

   constructor() {
     super();
```
（Info from Haiyue）

---
### 设置 - apps/settings

#### Q. 如何添加一个地区的时区？
* 在settings/resources/tz.json添加对应的时区信息
* 在settings/locales/settings.en-US.properties添加对应的翻译
* 更新底层的时区表，这个需要平台(SPRD/MTK/QCOM)支持

refer to [bug 58602](https://bugzilla.kaiostech.com/show_bug.cgi?id=58602)

---
#### Q. 添加FDN的Edit功能
A. settings里面合入以下patch，至于softkey edit放在哪里自主选择，patch里面是放在了CSK：

```
diff --git a/js/panels/call_fdn_list/panel.js b/js/panels/call_fdn_list/panel.js
index 8145d3d..b2afd7e 100755
--- a/js/panels/call_fdn_list/panel.js
+++ b/js/panels/call_fdn_list/panel.js
@@ -17,7 +17,7 @@ define(function(require) {
         this._elements.contactsContainer =
           panel.querySelector('#fdn-contactsContainer');
         this.gaiaHeader = document.querySelector('#simpin2-dialog gaia-header');
-        this._removeEnable = false;
+        this._removeOrEditEnable = false;
       },

       _initSoftkey: function() {
@@ -38,8 +38,21 @@ define(function(require) {
             }
           }]
         };
-        if (this._removeEnable) {
+        if (this._removeOrEditEnable) {
           params.items.push({
+            name: 'Edit',
+            l10nId: 'edit',
+            priority: 2,
+            method: function() {
+              self.setCurrentContact();
+              SettingsService.navigate('call-fdnList-add', {
+                mode: 'edit',
+                contact: self._currentContact,
+                name: self._currentContact.name,
+                number: self._currentContact.number
+              });
+            }
+          }, {
             name: 'Remove',
             l10nId: 'fdnRemove',
             priority: 3,
@@ -85,9 +98,9 @@ define(function(require) {
             this.contactArray[i] = contacts[i];
           }
           if (contacts.length) {
-            this._removeEnable = true;
+            this._removeOrEditEnable = true;
           } else {
-            this._removeEnable = false;
+            this._removeOrEditEnable = false;
           }
           this._initSoftkey();
           window.dispatchEvent(new CustomEvent('refresh'));
diff --git a/js/panels/call_fdn_list_add/panel.js b/js/panels/call_fdn_list_add/panel.js
index 61e9806..a4ed035 100644
--- a/js/panels/call_fdn_list_add/panel.js
+++ b/js/panels/call_fdn_list_add/panel.js
@@ -44,7 +44,7 @@ define(function(require) {
               priority: 2,
               method: function() {
                 self.gaiaHeader.dataset.href = '#call-fdnList';
-                self._updateContact('add', self._elements.fdnNameInput.value,
+                self._updateContact(self._mode, self._elements.fdnNameInput.value,
                   self._elements.fdnNumberInput.value);
               }
             }, {

```

#### Q. 关于KaiOS account注册登录必须有IMEI -Account, register, login, find my phone
A. 于KaiOS account注册登录前提条件s是插入SIM卡，并打开数据连接。

菜单地址：进入settings -> Account -> KaiOS Account ->Create Account 

///

1. 登陆KaiOS账号的设备必须有IMEI，否则无法登陆，否则提示"Server unavailable,Please try again later"
2. 登陆KaiOS账号的另一个条件是该设备必须是合法授权的KaiOS设备（软件），因而要求必须正确配置相关客户Key和CU Ref（这也是KaiStore可正常登陆的条件）。

Please make sure two conditions,
1. IMEI is valid. 
2. the SW of your device can successfully access KaiStore, which means the store and push keys, and CU Ref are well configured. 

#### Q. Storage菜单下存储空间尺寸和分区的关系 - Storage user application media system
A. 设置Settings中Storage项下各部分的空间计算关系如下：
1. media size  和 Application size  都是从真实的flash 分区文件系统读取的实际大小，
2. 其中 media size 显示的是 /usbmsc的大小，也即通过PC可读写的内置SDCARD的大小,
3. Application size 是 /userdata 分区，即内置系统 /data 目录可用的大小。 
4. 菜单最后的System空间（一些产品常隐藏该带单项），是将ROM/FLASH实际尺寸减去Media和Application放给用户的可用空间，得到的“系统预先占用”空间的尺寸。 
5. Dom 会根据 mount 的文件系统实际的 block 使用情况反馈给app
通过调用 volume.freeSpace()、 volume.usedSpace()、navigator.getDeviceStorage('apps').freeSpace() 、 navigator.getDeviceStorage('apps').usedSpace() 

#### Q. 如何修改展锐平台的VoLTE VoWifi 优先级 （wifi prefer, volte prefer）
A. Kaios volte and vowifi 菜单在
settings->network&connectivity ->Volte/Vowifi.如果你的样机中没有，说明编译时尚未启用volte功能。

*在此用户菜单中，用户可选择是否关闭或开启这些两个功能
*当两个都开启时，且两个服务在某个时刻网络测均支持时，kaios默认策略是VoWIFI优先（省电，省钱）

如果某个运营商要求此时仍然VoLTE优先，比如EE，则需要做如下改动：

gaia/build/config/common-settings.json 中搜'wifi-preferred' 改为'cellular-preferred'
settings/js/panels/volte_vowifi/panel.js 中，也做同样修改。
（info from Zhenquan)

### 桌面 - apps/launcher

#### Q. 快捷键原生在哪里处理的？
A. 可以看launcher里面的Mainview.js。另外也可以看看instant_settings文件夹里面的东西。

#### Q. 如何增加一个新的功能按键，比如直接启动facebook app的按键
A. 可以参考 apps/launcher/src/main_view.js里面的onKeyDown函数，

    switch (key) {
      case 'Call':
        LaunchStore.launch('manifestURL', 'app://communications.gaiamobile.org/manifest.webapp');
        break;
      case 'SoftLeft':
        LaunchStore.launch('iac', 'launcher-panel', { target: 'notice' });
        break;
      case 'SoftRight':
        LaunchStore.launch('manifestURL', 'app://contact.gaiamobile.org/manifest.webapp');
        break;
      case 'ArrowLeft':
        if (Service.query('Sidemenu.itemCount') > 0) {
          Service.request('openSheet', 'sidemenu');
        }
        break;
      default:
        break;
    }
    
添加新增按键的实际键值，然后仿照SoftRight的方式，调用对应的应用。

(Info from Sheldon in case 65229)

---
#### Q. FB和google图标需要按指定位置排放，这个默认值在哪个路径可以改啊？

A. 首先facebook, google 地图，语音助手，youtube 在桌面上的位置不允许修改。修改
后不可能通过Google、Facebook和KAPIC认证。
其次主菜单中应用位置也是有预定义的。某些重点App的位置不可以调整。具体先要参考
每个OEM发给ODM的Exhibit E - KaiOS Legal Brand Guidelines.pdf 文档中对主菜单顺序
的基本定义。
最后，如果是修改主带单中其他未定义成“固定位置”的应用的位置，是在 app/launcher/src/app_store.js 里面：

```
  orderedApps = [
    'Communications/call_log',
    'Contact',
    'KaiOS Plus',
    'Messages',
    'Facebook',
    'Camera',
    'JioTV',
    'JioMusic',
    'JioChat',
    'Assistant',
    'JioCinema',
    'JioGames',
    'JioXpressNews',
    'FM Radio',
    'Clock',
    'Gallery',
    'Calendar',
    'Calculator',
    'Settings',
    'Browser',
    'Unit Converter',
    'Music',
    'Video',
    'Note',
    'HelloJio',
    'JioVideoCall',
    'MyJio',
  ]
```

#### Q. 把WhatsApp放到桌面第一个快捷方式的代码 - Whatsapp shortcut homescreen KaiStore
A. 根据KaiOS和授权客户的合同约定，WhatsApp只能替换桌面上的KaiStore 图标，不允许替换其他应用图标的位置。
如下为替换动作的参考代码，

```
diff --git a/src/sidemenu/sidemenu.js b/src/sidemenu/sidemenu.js
index 4c278c4..7f160ca 100644
--- a/src/sidemenu/sidemenu.js
+++ b/src/sidemenu/sidemenu.js
@@ -33,7 +33,7 @@ export default class Sidemenu extends BaseComponent {
   ready = false;
   isActive = false;
   items = [
-    ['origin', 'app://kaios-plus.kaiostech.com'],
+    ['manifestURL', 'https://api.kaiostech.com/apps/manifest/ahLsl7Qj6mqlNCaEdKXv'],
     ['manifestURL', 'https://api.kaiostech.com/apps/manifest/oRD8oeYmeYg4fLIwkQPH'],
     ['manifestURL', 'https://api.kaiostech.com/apps/manifest/OSlAbgrhLArfT7grf4_N'],
     ['manifestURL', 'https://www.google.com/maps/preview/pwa/kaios/manifest.webapp'],
```

#### Q. 如何增加拨号盘暗码-快速访问

键盘暗码通常是为了完成一个快速操作，要么是显示一份信息，要么是引导一个KaiOS的app。
 
- 对于显示信息的，类似在kaios launcher中输入*#06# 查看IMEI。该实现非常简单，可阅读和摹写launcher app中的这部分代码： 文件名：  /apps/launcher/src/util/dial_helper.js
搜 '*#06#' 关键词即可找到代码段。 

- 对于启动或跳转某个app的，类似在kaios launcher中输入*#2886#启动MMITest App 功能，可阅读和摹写launcher app中的代码： 文件名：  /apps/launcher/src/util/dial_helper.js
搜 '*#2886#' 关键词即可找到代码段。 

当然，调用前提是你知道类似MMITest App的名字, 或许是你开发的新app。

---
### 浏览器 - apps/search

#### Q. 请不要使用百度网页测试KaiOS浏览器相关功能 - Baidu browser html CSS 

A. Baidu/百度主页及相关页面如百度图片和百度地图等均不支持QVGA尺寸，
一般也不能识别KaiOS的User Agent并提供移动设备版本页面。
OEM/ODM不应该以百度的网页测试KaiOS的浏览器功能及兼容性，也不必将相关发现反馈KaiOS。
推荐使用Google的相关网页测试。

#### Q. 如何预置浏览器的书签/topsite -browser bookmark topsite
A.KaiOS将书签称为topsite
在apps/search/build/topsites.json 
可以预置进类似Google，Facebook这样的一个URL进去,可直接摹写这两个bookmark的配置代码。

#### Q. 在浏览网页时，客户要求可以查看网页安全相关信息。如是否使用ssl传输，以及ssl版本等内容。查找了webapi，未找到相关接口。请问kaios是否有实现，请列出接口及使用说明。

- 支持SSL，而且Browser UI有pad lock icon显示。
- 支持TLS，但目前Browser UI没有pad lock icon显示，需要自行修改。
- 更多具体技术信息请参考网页： 
  `https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security`
- gecko里面调用的对应接口，并未向App层开放。

    ```
    gecko/security/manager/ssl/nsIBadCertListener2.idl
    boolean notifyCertProblem(in nsIInterfaceRequestor socketInfo, in nsISSLStatus status,in AUTF8String targetSite);
    ```

- 关于如何增加Gecko和Gaia之间的接口，请参看百度云链接中Kai Training\WebIDL目录中的文档：以Camera为例,讲解webidl的使用.ppt。
- Padlock icon在gaia/apps/contact/node_modules/gaia-icons/images/lock.svg
- 可以用 `var sslState = this.app.getSSLState();`  getSSLState方法获取到sslState状态；
- 在/gecko/security/manager/ssl/nsISSLStatus.idl里面，有如下信息：

```
    readonly attribute nsIX509Cert serverCert;

    readonly attribute ACString cipherName;
    readonly attribute unsigned long keyLength;
    readonly attribute unsigned long secretKeyLength;

    const short SSL_VERSION_3   = 0;
    const short TLS_VERSION_1   = 1;
    const short TLS_VERSION_1_1 = 2;
    const short TLS_VERSION_1_2 = 3;
    readonly attribute unsigned short protocolVersion;
```

   > 包括目前的版本信息，cipherName以及key，但是并没有传到gaia层。在nsISSLStatus.h里面，所有的接口都没有实现。

- 目前从browser输入网址，进入的页面显示在system应用里面，app_chrome.js以及app_window.js处理，锁图标的显示也在这边。
- TLS的部分在/gecko/network/base/TLSServerSocket.cpp以及h里面。这里面有实现的代码：

```
nsresult
TLSServerConnectionInfo::HandshakeCallback(PRFileDesc* aFD)
{
  nsresult rv;

  ScopedCERTCertificate clientCert(SSL_PeerCertificate(aFD));
  if (clientCert) {
    nsCOMPtr<nsIX509CertDB> certDB =
      do_GetService(NS_X509CERTDB_CONTRACTID, &rv);
    if (NS_FAILED(rv)) {
      return rv;
    }

    nsCOMPtr<nsIX509Cert> clientCertPSM;
    rv = certDB->ConstructX509(reinterpret_cast<char*>(clientCert->derCert.data),
                               clientCert->derCert.len,
                               getter_AddRefs(clientCertPSM));
    if (NS_FAILED(rv)) {
      return rv;
    }

    mPeerCert = clientCertPSM;
  }

  SSLChannelInfo channelInfo;
  rv = MapSECStatus(SSL_GetChannelInfo(aFD, &channelInfo, sizeof(channelInfo)));
  if (NS_FAILED(rv)) {
    return rv;
  }
  mTlsVersionUsed = channelInfo.protocolVersion;

  SSLCipherSuiteInfo cipherInfo;
  rv = MapSECStatus(SSL_GetCipherSuiteInfo(channelInfo.cipherSuite, &cipherInfo,
                                           sizeof(cipherInfo)));
  if (NS_FAILED(rv)) {
    return rv;
  }
  mCipherName.Assign(cipherInfo.cipherSuiteName);
  mKeyLength = cipherInfo.effectiveKeyBits;
  mMacLength = cipherInfo.macBits;

  if (!mSecurityObserver) {
    return NS_OK;
  }

  // Notify consumer code that handshake is complete
  nsCOMPtr<nsITLSServerSecurityObserver> observer;
  {
    MutexAutoLock lock(mLock);
    mSecurityObserver.swap(observer);
  }
  nsCOMPtr<nsITLSServerSocket> serverSocket;
  GetServerSocket(getter_AddRefs(serverSocket));
  observer->OnHandshakeDone(serverSocket, this);

  return NS_OK;
}
```

握手之后的callback函数里面，channelInfo里面有对应信息。

#### Q. 为什么KaiOS Browser打开的网页为PC网页而非类似Android移动设备网页-Mobile webpage
A.比如KaiOS 浏览器在打开qq音乐网站时打开的是电脑端的页面。如果对比Android和IOS手机发现他们的浏览器是直接打开的qq音乐的移动端页面。

如果网站不能正确理解和处理来自KaiOS 设备的UA，判断为是移动设备，就会把KaiOS浏览器当作普通Mozilla浏览器，下发电脑端的网页。

这是一个历史性的问题，暂时无法解决，而且无法由设备供应商主动改正。

This is same reason caused by User Agent. The website push different pages for different UA. This can't be controlled by Mobile device.

---
### 联系人 - apps/contact

#### Q. SDN菜单位置
A. SDN显示在Contacts->settings->service number.
KaiOS目前不支持将SDN显示在Contacts/电话本。

#### Q. SIM卡联系人支持ICE号码设置 - contacts 
A. 
ICE = In case of emergency. 
在联系人应用中的Options->Settings,select "Set ICE Contacts"，如果选择联系人，会发现SIM卡联系人不能设置为ICE。为什么？
KaiOS的设计鼓励用户将关键联系人（如ICE）保存本机，而不是在SIM卡移除后功能失常。
如果OEM想开启SIM卡联系人可设置ICE，可参考如下的代码：

>ice_editor_view.js
```
  Service.request('push', '/pick/ice', {
    noSimContact: true
  }).then((result) => {  
```

#### Q. 如何修改电话本的联系人默认排序为姓氏排序 - contacts sorting first last family name
A. 目前默认是名字排序，而非姓氏（family name）。
可参考如下代码，具体行数会变化
```
diff --git a/src/contact_store.js b/src/contact_store.js
index 0e400c1..1c3bce3 100644
--- a/src/contact_store.js
+++ b/src/contact_store.js
@@ -108,7 +108,7 @@ class ContactStore extends BaseModule {
 
   get sortingRule() {
     let rule = window.localStorage.getItem('sort');
-    return rule || 'givenName';
+    return rule || 'familyName';
   }
 
   get source() {
```
（info from Kui）

---
#### Q. 如何预置联系人
A.
- 合入如下的 gecko patch：

```
    diff --git a/dom/contacts/fallback/ContactDB.jsm b/dom/contacts/fallback/ContactDB.jsm
    index 091d823..df0a38f 100644
    --- a/dom/contacts/fallback/ContactDB.jsm
    +++ b/dom/contacts/fallback/ContactDB.jsm
    @@ -133,7 +133,7 @@ ContactDB.prototype = {
        }

        let chan = jsm.NetUtil.newChannel({
    -        uri: NetUtil.newURI(contactsFile),
    +        uri: jsm.NetUtil.newURI(contactsFile),
            loadUsingSystemPrincipal: true});

        let stream = chan.open2();
```

- 在 /gaia/distribution 路径下创建 contact.json 文件。如果没有的话，请手动创建。

- 在 contact.json 文件中加入如下的内容：

```
    [
        {
        "name": ["John Doe"],
        "givenName": ["John"],
        "familyName": ["Doe"],
        "tel":[{"type":["mobile"],"value":"123"}],
        "category": ["DEVICE", "KAICONTACT"]
        },
        {
        "name": ["Wan Wang"],
        "givenName": ["Wan"],
        "familyName": ["Wang"],
        "tel":[{"type":["mobile"],"value":"12566"}],
        "category": ["DEVICE", "KAICONTACT"]
        }
    ]
```

---
### 通话 - apps/callscreen, apps/communications

#### Q. 双卡拨打电话选择SIM问题逻辑 
A. KaiOS明确将双卡主次关系设计为
```
When FTU,
if there is no SIM card inserted currently, preferred data card will be "SIM1*" and preferred call card will be "Always ask";
if there is one SIM card inserted currently, that card will be the preferred data and call card;
if there are two SIM cards inserted currently, SIM1 will be the preferred data and call card.
When removing or inserting SIM card(s),
if there is no SIM card inserted currently, preferred data card will be "SIM1*" and preferred call card will be "Always ask";
if there is one SIM card inserted currently, that SIM will be assigned to preferred data card or auto-assigned data card;
if there are two SIM cards inserted currently, the latest remembered card will be assigned to preferred data card. (If both cards are new cards,
SIM1 will be auto-assigned data card.)
--- from KaiOS spec.
```
简单的说，刷机后插双卡开机，拨号默认SIM1；若过完开机向导再插入双卡，拨号则默认每次询问。

如果要客制化，双卡插入过开机向导，Call 默认选择Ask always，可参考如下代码
```
KaiOS/gaia/apps/system
diff --git a/src/sim_settings_helper.js b/src/sim_settings_helper.js
index b4ef74a46..ef5c2bf62 100644
--- a/src/sim_settings_helper.js
+++ b/src/sim_settings_helper.js
@@ -280,7 +280,7 @@ class SimSettingsHelper extends BaseModule {
     }
     // First time run and first set.
     if (!notFirstSet) {
-      if (SIMSlotManager.noSIMCardOnDevice() || serviceName === 'outgoingData') {
+      if (SIMSlotManager.noSIMCardOnDevice() || serviceName === 'outgoingData' || serviceName === 'outgoingCall') {
         cardIndex = this.ALWAYS_ASK_OPTION_VALUE;
       } else {
         cardIndex = SIMSlotManager.isSIMCardAbsent(0) ? 1 : 0;
```

---
#### Q. 如何获取手机中 Communications 数据库文件

A. 连接手机
```
adb root
adb remount
adb pull /data/local/storage/default/1006+f+app+++communications.gaiamobile.org/idb /YourFile/idb/
```

---

### 信息 - apps/sms

#### Q. 关于西班牙语，土耳其语，葡萄牙语的短信的编码 SMS encoding Turkish, Spanish, Portuguese

KaiOS支持3GPP GSM 7 bit default alphabet extension table，即3RPP 23038 R8。
但是该功能生效需要当地SIM卡。只有插入这些国家的SIM卡，才会激活对应语言的extension table。测试验证应该注意。

例如绝大多数土耳其人民一定会用土耳其卡。一个土耳其人到了法国在，在用法国的卡，短信长度变长了，因为短信的字符扩展表失效。

KaiOS的设计，不影响法国销售本来要在法国销售的设备，也不影响土耳其市场的销售

假设在法国测试这个功能，要验证土耳其语葡萄牙语，如果用本地卡，就可能报bug。但这只是测试方法问题。

---
#### Q. KaiOS不支持存储在SIM卡的短信息读取和显示
A. KaiOS不支持从SIM卡读取已存短信，也不支持本机和SIM卡间拷贝复制短信。

---

### 相机 - apps/camera

#### Q. 录像机分辨率怎么默认为中？
A. 在初始化过程中修改默认选中的项。
- 具体code在camera/js/controllers/settings.js中处理

```
    diff --git a/js/controllers/settings.js b/js/controllers/settings.js
    index 94e71a5..43ba3c5 100644
    --- a/js/controllers/settings.js
    +++ b/js/controllers/settings.js
    @@ -456,6 +456,7 @@ SettingsController.prototype.configureRecorderProfiles = function(sizes) {
    if (maxFileSize) { formatted = [formatted[0]]; }

    setting.resetOptions(formatted);
    +  setting.select(1, { silent: true });
    };
```

其中formatted数组包涵3个选项，［low, standard, high］

0 => low

1 => standard

2 => hight

至于为什么只生成这3种分辨率请看： *format-recorder-profiles.js*

ref bug: [bug58487](https://bugzilla.kaiostech.com/show_bug.cgi?id=58487)

---
#### Q. Camera 录像分辨率选项显示不全(只显示一个)；如何定制显示的分辨率格式？
* 首先**所有**支持的录像的分辨率都是通过gecko的mozCamera接口给到应用层。

   * [CameraControl.capabilities](https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/CameraCapabilities)

   *  [CameraCapabilities.recorderProfiles](https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/CameraCapabilities/recorderProfiles)


* 底层上传所有支持的分辨率文件定义在标准的android多媒体**media_profile.xml**配置文件中

  * 高通项目参考路径: KaiOS/device/qcom/common/media/media_profiles.xml
  * 展讯项目参考路径: KaiOS/vendor/sprd/release/IDH/device/sprd/pike2/sp7731ef_18c10/media_profiles.xml

* 在camera应用中，会通过一些应用设置选项过滤掉一些不常用，或者不支持的分辨率(exclude 字段中的值会被过滤掉)；当然，这个值在不同的需求的项目中也可以自己定义。


```
  recorderProfilesBack: {
    title: 'video-resolution',
    header: 'video-resolution-header',
    icon: 'video-resolution',
    options: [],
    exclude: ['1080p', '720p', 'cif', 'high', 'default', 'low'],
    persistent: true,
    optionsLocalizable: false,
  },
```
过滤机制是写在 *format-recorder-profiles.js* 中：
```
  //遍历所有传上来的分辨率，经过系列判断生成候补分辨率
  for (var key in profiles) {
    // 检查profile必须拥有key 才正确
    if (!profiles.hasOwnProperty(key)) {
      continue;
    }

    profile = profiles[key];
    video = profile.video;

    // 过滤掉写在exclude中的profile
    if (exclude.indexOf(key) > -1) { continue; }

    pixelSize = video.width * video.height;

    tempProfiles.push({
      key: key,
      title: key + ' ' + video.width + 'x' + video.height,
      pixelSize: pixelSize,
      raw: profile
    });
  }

  // 以分辨率从大到小对候补分辨率进行排序
  tempProfiles.sort(function(a, b) { return a.pixelSize - b.pixelSize; });


// 依次返回 候补分辨率中最小的三种分辨率
// 例如: [9, 8, 6, 3, 2, 0] => ［0, 2, 3］
  var localized = options.app.localized();
  while ((tempProfiles.length > 0) && (formattedProfiles.length < 3)) {
    var title = '';
    switch (formattedProfiles.length) {
      case 0:
        title = 'low-resolution';
        break;
      case 1:
        title = 'standard-resolution';
        break;
      case 2:
        title = 'high-resolution';
        break;
    }

    profile = tempProfiles.shift();
    formattedProfiles.push({
      key: profile.key,
      title: localized ? options.app.l10nGet(title) : title,
      pixelSize: profile.pixelSize,
      raw: profile.raw,
      localized: localized
    });
  }
  console.log('format-recorder-profiles formattedProfiles=' +
    JSON.stringify(formattedProfiles));
  return formattedProfiles;
```

**总结,如果要定制camera的分辨率，则需要客户在知晓自己硬件设备支持的分辨率的情况下（配置好media_profiles.xml）； 通过配置Camera应用中js/config/settings.js文件中的exclude字段的值来进行定制，exclude的含义是不包含，里面添加的是你需要去掉的profile。**

例如，

+ 假设上报上来的所有支持的分辨率(key)值是： qvga, cif, 480p, 720p, high(key叫high而已)
+ exclude 中的key是［high，low］
+ 过滤之后从低到高取3个 ＝> qvga, cif, 480p
+ 假设不想要qvga这个最低profile那么刻意的把它过滤掉即可，这时exlude中写 [high, low, qvga]
+ 过滤后的从低到高取3个 => cif, 480p, 720p
+ 需要注意的是，假设过滤后不足3个(为2个)那么就会只显示low 和 standerd

*输入* 是所有支持的profile（底层上报的）
*输出* 是在过滤之后的所有分辨率从低到高的3个

ref bug: [bug66621](https://bugzilla.kaiostech.com/show_bug.cgi?id=66621)
ref bug: [bug58487](https://bugzilla.kaiostech.com/show_bug.cgi?id=58487)

---
#### Q. 去掉Camera闪光灯功能及图标

Camera中配置设置菜单的列表的代码在 apps/camera/js/config/settings.js

```
diff --git a/js/config/settings.js b/js/config/settings.js
index 1908ebe..b92cd7e 100644
--- a/js/config/settings.js
+++ b/js/config/settings.js
@@ -93,6 +93,11 @@ module.exports = {
     icon: 'flash-on',
     options: [
       {
+        key: 'off',
+        icon: 'flash-off',
+        title: 'flash-off'
+      },
+      {
         key: 'auto',
         icon: 'flash-auto',
         title: 'flash-auto'
@@ -101,11 +106,6 @@ module.exports = {
         key: 'on',
         icon: 'flash-on',
         title: 'flash-on'
-      },
-      {
-        key: 'off',
-        icon: 'flash-off',
-        title: 'flash-off'
       }
     ],
     persistent: true
@@ -207,9 +207,6 @@ module.exports = {
         key: 'cameras'
       },
       {
-        key: 'flashModesPicture'
-      },
-      {
         key: 'timer'
       },
       {
@@ -230,9 +227,6 @@ module.exports = {
         key: 'cameras'
       },
       {
-        key: 'flashModesVideo'
-      },
-      {
         key: 'recorderProfiles'
       },
       {
```

该patch原理是去掉设置菜单中的flashmode选项，并且把flashmode的off图标设置为默认。

Ref bug: [bug60396](https://bugzilla.kaiostech.com/show_bug.cgi?id=60396)

#### Q. 如何修改闪光灯是否支持 - flash light.20190202

A.删除闪光灯需要OEM修改代码

关于快速去掉闪光灯的方法还是需要手动在camera/js/config/settings.js里面配置，具体有四个参数需要修改；
1、  settingsMenuPhoto去掉key: 'flashModesPicture'
2、  settingsMenuVideo去掉 key: 'flashModesVideo'
3、  settingsMenuPhotoSecureMode去掉 key: 'flashModesPicture'
4、  settingsMenuVideoSecureMode 去掉 key: 'flashModesVideo'
 
另外在camera页面的左上角会有一个闪光灯开/关的状态logo，这个需要在controllers/controls.js文件下注释掉调用updateFlashMode方法的地方。

---
#### Q. 怎么启动人脸识别face detection功能
A. 1, KaiOS的人脸识别支持来自底层camera模块

2, KaiOS默认是开启了脸部识别的。By Pref "camera.control.face_detection.enabled"

3, 因为该功能需要芯片组支持，需要集成独立的功能模块。具体应该与芯片提供商确认。 
如果库存在，会有类似如下的log

this feature need chipset support, in QCOM case, it need put the face detection library. and if there is no library, it will not running with log as bellow:

ubsampling optimizations
```
01-08 01:07:38.187   277  7492 D QCameraParameters: int32_t qcamera::QCameraParameters::setNumOfSnapshot(): nBurstNum = 1, nExpnum = 1
01-08 01:07:38.187   277  7492 D QCameraParameters: int32_t qcamera::QCameraParameters::setFaceDetection(bool): face process mask not changed, no ops here
01-08 01:07:38.187   277  7492 D QCamera2HWI: int qcamera::QCamera2HardwareInterface::sendCommand(int32_t, int32_t&, int32_t&): FaceDetection -> Disabled
```
4, 具体集成方式也应直接询问平台厂商。suggest u ask platform vender if the chipset support face detect feature, and what & where the face detection library put.
(Info from Shi in case 59401)

### 视频 - apps/video

##### Q. 如何修改实现视频的循环播放-演示app demo app video cycle repeat 

A. 展会Demo App是个复杂的topic，每个OEM有自己的想法，KaiOS不提供这类应用方案。

ODM可以简单的实现如下的视频播放器里的循环播放的功能，再尝试按照展示要求，从菜
单合适的上下文调起视频播放器，播放指定演示视频即可。
```
/////
diff --git a/js/video.js b/js/video.js
index 5f317b6..ea698dc 100755
--- a/js/video.js
+++ b/js/video.js
@@ -836,6 +836,7 @@ function updateVideoControlSlider() {
   dom.durationText.textContent =
     (remainingTime > 0) ? '-' + MediaUtils.formatDuration(remainingTime) : '---:--';
 
+
   // Don't move the play head if the user is dragging it.
   if (!dragging) {
     movePlayHead(percent);
@@ -1153,7 +1154,7 @@ function playerEnded() {
   // event and in that case we will remain paused at the end of the video.
   if (playing) {
     dom.player.currentTime = 0;
-    pause();
+    play();
   }
   //back to non full screen
   if (isFullScreen) {
diff --git a/js/view.js b/js/view.js
index 14751cb..8c9d5d4 100755
--- a/js/view.js
+++ b/js/view.js
@@ -464,7 +464,7 @@ navigator.mozSetMessageHandler('activity', function viewVideo(activity) {
     // event and in that case we will remain paused at the end of the video.
     if (playing) {
       dom.player.currentTime = 0;
-      pause();
+      play();
     }
     //back to non full screen
     if (isFullScreen) {
```

(info from Haiyue)

### 电子邮件 - apps/email

#### Q. 如何增加预置的电子邮件参数（customize email account profile preset pop3 imap smtp）
A. 在apps/email/autoconfig 目录下有几十个预置的邮箱参数文件。
如果要为某个客户增加某个邮件的预设资料，请先拿到邮箱参数，试验用的账号，密码。
根据pop3协议还是imap协议，摹写已经存在的这个类型的数据项，包括文件命名方式等细节，完全的摹写，然后加入到这个目录，并编译测试。

---
### FOTA - apps/fota

#### Q. 关于FOTA差分升级和整包升级-FOTA,Package.20190101
1.哪些情况是可以正常使用差分升级
2.哪些情况下是必须用整包来升级

A. 一般情况下 ，差分升级都是可以的。对于制作Fota升级包的源版本和目标版本没什么特别要求或者限制，包括更新了modem或者NV这些，不会影响到Fota升级包的制作。

全包升级主要用来解决system分区因为差分升级出现空间不足时候, 可以用全包升级。

---------另外-----
全包的命名和差分包命名相一致。可以将全包当成所有版本的差分包。

目前server端还不支持全包，所以全包升级请从SD卡安装
(info from Jenny)

---
#### Q. FOTA升级包下载方式配置 fota download wifi telecom
用户可在此处配置查分包下载方式
`Settings -> Device -> Device information -> Software update -> Settings -> Download via -> Wi-Fi only`
但是出场预置的查分包下载方式在哪里设置？

A. 例如若设为WifiOnly，可尝试如下修改：
gecko/b2g/app/b2g.js
里面增加
pref("fota.download.via", 0);

---
#### Q. FOTA压力测试工具
A. KaiOS有FOTA压力测试工具，用来对FOTA升级过程反复离线，需要离线进行FOTA的自动升级和降级压力测试
具体用法如下
[test environment]: ubuntu
[Precondition]: Device under test was upgraded to the source version,
Prepare the diff-package：
diff-package1: from source version to target version
diff-package2: from target version to source version
[The test method]:
adb command:
python fota_stress_test.py diff-package1 diff-package2 Test_times

ps: 1. you can put the fota stress script/diff-package1.zip/diff-package2.zip in the same folder
and the log will also show in this folder
1. 必须在UserDebug 版本始用，User 版本无法工作。
(Info from Yuan in case 57155)

---
#### Q. "FOTA engine start failed!" error - FOTA 引擎 启动 失败
A. KaiOS系统FOTA配置必须先保证参数正确。请先认真阅读“KaiOS FOTA config guide vx.y.pdf”和“KaiOS_FOTA_Guide V0.x.ppt” 和“OEM CU Ref Introduction v1.x.pdf”三个文档，正确配置FOTA基本参数再使用FOTA。

---
### 时钟 - apps/clock
#### Q. 关机闹钟是否支持？
A. KaiOS不支持关机闹钟。如果客户想支持关机闹钟，需要和平台厂商合作实现。

---
### 相册 - apps/gallery

#### Q. Gallery和FileManager中打开图片时对尺寸的限制是怎样的?
Refer to 67945, only for v2.5

A:

From gallery,

apps/gallery/build/build.js

```
  if (options.GAIA_MEMORY_PROFILE === 'low') {
    this.DEFAULT_VALUE.maxImagePixelSize = 2 * 1024 * 1024;
```

apps/gallery/js/MetadataParser.js

```
      var imagesizelimit = CONFIG_MAX_IMAGE_PIXEL_SIZE;
      if (metadata.type === 'pjpeg') {
        // As a semi-educated guess, we'll say that we can handle pjpegs
        // 2/3rds the size of the largest PNG we can handle.
        imagesizelimit *= 2 / 3;
      }
```

So we can't display a 1080x1350 jpeg file as 1080x1350 (1458000) > 2 * 1024 * 1024 * 2/3 (1398101.333).

---

From FileManager,

apps/gallery/js/open.js

```
      if (blob.type === 'image/jpeg') {
        imagesizelimit *= Downsample.MAX_AREA_REDUCTION;
      }

```

We have this `MAX_AREA_REDUCTION`multiplied that allows much larger image size to open a single jpeg file.

So it's up to you to modify current behavior.

You may either set max size limit to `3 * 1024 * 1024` to make it able to open a 1080x1350 file in Gallery. (May have some memory issue, but I think it's fine.)

Or remove `imagesizelimit *= Downsample.MAX_AREA_REDUCTION;` in `open.js` to make a same behavior.

We'd better not modify codes in open.js as it's fine to open much larger files in file manager or Downloads.

---
### 录音机 - apps/soundrecorder
#### Q. 如何修改录音机应用的默认录音格式 - sound recorder format oga opus

A.  KaiOS 录音机应用默认录音格式为.opus. OEM/ODM 若想改变该默认格式，
应先自行确认产品所选平台编解码能力，确定平台可支持后，参考case 63512定制录音格式。

---
### 收音机 - apps/fmradio

#### Q. 如何设置FMradio内置天线

目前大部分终端FM应用需插入耳机做外置天线使用，否则进入应用会提示需插入耳机，无法使用FM.
对于带FM内置天线的终端，可以将 "dom.fmradio.antenna.internal" 这个pref打开，使FM在未插入耳机时可正常使用.

```
    pref("dom.fmradio.antenna.internal"", true);
```

相关代码见 `gecko/dom/fmradio/FMRadio.cpp`.

---
## 应用商店

#### Q. 如何配置Store的KeyID对?

每个项目访问KaiOS Store使需要使用特殊的key/ID pair(也称为Service ID/Key)，只有正确配置才能访问KaiStore，此guide讲述如何配置。

**1. 以项目M为例，首先由KaiOS的CPM申请Key/ID pair，以下为举例说明：**
  - 项目M用于Push的Key/ID pair

    ID:  xxxxxxxxxxxxID1xxx(这个ID名字是为了方便说明的举例，正常的ID形式类似于iwT3Qlw42pm6E7nnwyBJ)

    Key: xxxxxxxxxxxkey1xxx(这个key名字是为了方便说明的举例，正常的ID形式类似于p9GkBaA8Io6ZUkJGSs9y)

  - 项目M用于Store的Key/ID pair:

    ID:  xxxxxxxxxxID2xxx(举例，形式类似于8xCPdQ4gfCGOJbvgeKcp)

    Key: xxxxxxxxxxkey2xxx(举例，形式类似于4SB4kaCvu-qaio3glxSa)

  - 另外还需要用于Metrics的Key/ID，但不用申请，复用Store的

  - 请注意每个项目的Key/ID pair都不同，请务必使用项目指定的。

**2. 如何在code中使用Key/ID pair？**

  - Step 1: 在代码根目录下创建三个存放key的新文件:

    a). store_key.txt contains key of Store as: xxxxxxxxxxkey2xxx

    b). push_key.txt contains key of Push as: xxxxxxxxxxxkey1xxx

    c). metrics_key.txt contains key of Metric as: xxxxxxxxxxkey2xxx

     该文件只能有一行，不要有任何回车换行符，也不能有文件头(比如记事本会产生文件头)，请严格参考附件压缩包，最终的文件尺寸应该在20字节，而不是23字节。

  - Step 2: in gaia/Makefile

    修改"SHARE_PERF_USAGE?" to 1

  - Step 3: in gecko/b2g/app/b2g.js **(此步有待改进，不应直接修改b2g.js，请参考57976)**

      - a). 修改"apps.token.uri" to https://api.kaiostech.com/v3.0/applications/xxxxxxxxxxID2xxx/tokens

      - b). 增加一个首选项：pref("device.commercial.ref","xxxxx-xxxxxxxxxxxx");这里的CU Ref由客户自己定义，客户应该已经配置FOTA时定义过，使用一样的。

      - c). 修改"dom.push.token.uri" to https://api.kaiostech.com/v3.0/applications/xxxxxxxxxxxxID1xxx/tokens

      - d). 修改"metrics.token.uri" to https://api.kaiostech.com/v3.0/applications/xxxxxxxxxxID2xxx/tokens

      - e). 设置完后请用WebIDE检查是否成功

  - Step 4: 设置环境变量
  export KAI_APPS_KEY_FILE=/xxx/xxx/xxx/store_key.txt;
  export KAI_PUSH_KEY_FILE=/xxx/xxx/xxx/push_key.txt;
  export KAI_METRICS_KEY_FILE=/xxx/xxx/xxx/metrics_key.txt

  请使用从根目录开始的绝对路径，请先尝试命令行的方式，然后再考虑改脚本的方式以方便编译
  然后开始编译./build.sh

**3. 编译结束后，请将三个key文件、b2g.js、omni.ja文件打包发给CPM检查(邮件不要直接附js文件，收不到)**

- adb pull /system/b2g/omni.ja		用此方法取出omni.ja

---
#### Q. 为什么KaiStore一旦灭屏，app即退出，下次必须重新启动联网？
KaiStore 开始集成支付功能，从安全考虑，屏幕熄灭代表用户离开，用户离开则不应再挂着Store业务，这样对用户更安全。
另外kaios的app下载、安装都不需要store保持前台，故StoreApp退出并不影响用户已经选择的下载或升级的业务。

---
#### Q. 关于KaiStore的菜单翻译-Menu Translate string 
A.KaiStore的所有菜单的翻译均由KaiOS负责，且KaiStore是编译后发布的，ODM/OEM没有源代码，不可以修改任何Store行为。

因为store不开放源码，也只能由KaiOS处理翻译。

多数语言kaiStore都有支持，ODM/OEM若在Store中发现不支持的出货语言，先检查代码中对新增语言的language code是否按照规范定义？若有定义却未显示翻译的，可将语言列表提供给CPM检查是否尚未支持。

language code不对就会找不到对应翻译，下面的链接中可参考对照：
https://git.kaiostech.com/KaiOS/gaia/blob/master/locales/languages_services.json

---
#### Q. Whatsapp集成问题排查顺序
A. WhatsApp集成测试应按照如下顺序排查问题
1. 先进入KaiStore，若不能正常访问Store,则为网络问题。假如确保网络畅通，
2. 若KaiStore打开5秒内闪烁连接错误，则为CU Ref并未配置，或所配置CU Ref未提交KaiOS后台，或配置CU Ref中含有小写字母，或Store key配置错误，或编译错误。
3. 若KaiStore能正常访问，但是不存在“social” 应用分类，或该分类下没有WhatsApp 一行，则CU Ref未被授权访问WhatsApp
4. 若存在WhatsApp但不能下载，则可能是相关组件版本错误，尝试关机再开，排除临时错误，若两次重启仍不能安装，需要代码分析。
5. 若WhatsApp下载和安装时间较长，但3分钟以内可以完成，则不是bug。
6. 若WhatsApp下载正常但启动后停留在“requesting SMS”界面且不显示号码失效等信息，则英确认测试设备可以访问facebook/Google。
7. 若测试设备可以访问外网，仍停留在“requesting SMS”，则需进一步代码分析，现实多发生在测试版WA验证中，ODM参与极少。
8. 若测试设备收到WhatsApp提示号码被禁用，请xx小时候后重试，则为短期登陆过于频繁，请停止继续尝试登陆。若此页面提供电话回拨提供验证码的选项，可选择该方式回播以恢复账号。若不显示，也不是bug。

---
## 移动与无线连接
### Telephony/RIL
#### Q. 平台是否支持BIP (Bearer Independent Protocol)
A.高通平台和展讯平台都支持，区别是高通平台做在Modem侧，展讯平台做在AP侧。

---
#### Q. 如何集成PLMN表？
A. 目前AP侧没有列表，不过高通这边是有一张的。你们可以提case给到高通咨询。
`amss_8909\modem_proc\uim\mmgsdi\src\Mmgsdi_se13_table.h`

---
#### Q. KaiOS切换单卡和双卡的接口是什么
A. 可以通过system property属性设置，比如:

- `adb shell setprop persist.radio.multisim.config dsds` 设置为双卡
- `adb shell setprop persist.radio.multisim.config “”` 设置为单卡

然后重启生效。

也可以看看 `ro.moz.ril.numclients`，控制卡槽数量，2是双卡，1是单卡。

#### Q. Device must support MVNO detection - GID1, SPN, IMSI.app层：apps\system\js\statusbar.js获取GID1的接口是什么？
A. 没有直接获取GID的接口，但有match　GID/SPN/IMSI的接口，apps/system/js/operator_variant_handler.js

```
var iccCard = navigator.mozIccManager.getIccById(this._iccId);
var request = iccCard.matchMvno(listMvnoType,listMvnoMatchData);
```

---
#### Q. 现在市场上见到双卡手机只有一张卡能够注册LTE网络（通常称这张卡为主卡），KaiOS是不是使用的这个策略？如果不是，请描述一下KaiOS的策略，如何设置那张卡可以注册LTE。另外客户有些需求需要根据SIM卡能否注册LTE做配置，请问如何查询哪张SIM卡可以注册LTE？
A.

分几点回答：

- 高通8905平台+KaiOS v2.5支持双卡，但只有一张卡能注册LTE，此时另外一张卡只能注册2G。

- 任何一张卡都可以设置为主卡，菜单SettingNetwork&ConnectivitySim ManagerData中选中的卡就是主卡。

- 如何查询哪张卡是主卡？读取settings 值：`ril.data.defaultServiceId`
webIDE 可以读：

```
var request = navigator.mozSettings.createLock().get('ril.data.defaultServiceId'); request.onsuccess = (() => {console.log(JSON.stringify(request.result['ril.data.defaultServiceId']))})
```

---

#### Q. 关于漫游时时IPV4V6的选择-IPV4 IPV6 Roaming .20190101

问题：-------------
settings->Mobile Network & data->APN settings->Options -> APN Editor
里roaming_protocol没定义的条目，Roaming Protocol显示Not defined。
但是这样不符合3GPP TS 24.301, 定义APN Protocol值必须是以下中的一个:

Bits	
0	0	1		IPv4
0	1	0		IPv6
0	1	1		IPv4v6
1	0	0		unused; shall be interpreted as "IPv6" if received by the network
1	0	1		non IP

请问Roaming Protocol是 Not defined时，在roaming状态下手机建立PS连接，实际使用的值是什么。

------------解释------------
Not define means IPV4 only, in Qcom platform. 
Q's code will set protocal to IPV4 only when gaia give undefined protocal.
other Modems' behavior need check with them case by case. 

#### Q. 关于国内双卡测试中相同ICCID的SIM卡测试禁忌
A. 国内运营商常出现两张SIM卡定义相同的ICCID的情况，特别是同一批买入的同一个运营商的测试卡。
但这种情况是违反了3GPP对SIM卡中ICCID使用规则。
KaiOS上层UI依赖SIM卡的ICCID区别主副卡身份。
如果测试双卡双待的ODM，恰好使用了两张相同ICCID的sim卡，会出现很多不确定的问题，比如两卡无法在UI中区分。
因此提醒，除非目标产品定义为销往中国市场的运营商产品，否则建议OEM/ODM采用不同运营商的两张SIM卡测试双卡行为，否则会有很多奇怪的双卡界面相关问题。
而KaiOS暂时还无法解决此类协议冲突。

---

#### Q. 如何定制simlock？
A. 配置settings值,配置文件在: `gaia/build/config/common-settings.json`
```
配置格式：
'custom.nck.behavior' = {
  'carrier-non_carrier': behaviorValue,
  'carrier-blank':　behaviorValue,
  'non_carrier-carrier': behaviorValue,
  'non_carrier-non_carrier': behaviorValue,
  'non_carrier-blank': behaviorValue,
  'blank-carrier': behaviorValue,
  'blank-non_carrier': behaviorValue,
}
```
key|value
--|--
carrier|运营商卡
non-carrier|非运营商卡
blank|无卡
>key中carrier，non-carrier, blank分别代表卡槽1和卡槽2的状态，分别表示运营
商卡，非运营商卡和无卡。

behaviorValue|value
--|--
'toast'|toast提示
'attentionDialog'|弹出框
'inputDialog'|输入框
'attentionDialogNoskip'|弹出框没有skip按钮
'inputDialogNoskip'|输入框没有skip按钮


>例如某运营商要求：
1.当卡槽1无卡，卡槽2插非运营商的卡时提示用户卡槽1插运营商的卡
2.当卡槽1插运营商的卡，卡槽2无卡需要输入nck码
```
'custom.nck.behavior' = {
  'carrier-blank':‘attentionDialogNoskip’,
  'blank-non_carrier': ‘inputDialog’
}
```

#### 短信收发问题日志抓取
settings中开启 
Settings->navigate to tab 'Device', 
enter item 'Developer'->enable items  'RIL output in ADB', 'Console enabled''Debug traces' and 'Network output in ADB','Wi-fi output in ADB';


#### 无法发送短信问题:cs域未成功注册
某些运营商在LTE only下,关闭volte和vowifi,无法发送短信,却可以使用数据上网,这是因为该运营商的lte没有cs域

检查是否存在cs 或 ps域:
通过下面的Log来判断RIL_REQUEST_VOICE_REGISTRATION_STATE代表CS domain,
RIL_REQUEST_DATA_REGISTRATION_STATE代表PS domain, state值为1（Home）或者5(roaming)时代表注册上了, 具体定义请参考hardware/ril/include/telephony/ril.h里的注释， 这里同安卓一样。

Volte_shut_off(1).txt:7362: 01-15 21:13:23.080 D/SERVICE_STATE_TRACKER(  497): RIL_REQUEST_VOICE_REGISTRATION_STATE state = 5,mRadioTechnology = 14 gxf
Volte_shut_off(1).txt:8086: 01-15 21:13:24.643 D/SERVICE_STATE_TRACKER(  497): RIL_REQUEST_VOICE_REGISTRATION_STATE state = 2,mRadioTechnology = 0 gxf

Volte_shut_off(1).txt:16022: 01-15 21:14:15.447 D/SERVICE_STATE_TRACKER(  497): RIL_REQUEST_DATA_REGISTRATION_STATE state = 5, mDataRadioTechnology = 14, mTAC =-1 gxf
Volte_shut_off(1).txt:16440: 01-15 21:14:17.795 D/SERVICE_STATE_TRACKER(  497): RIL_REQUEST_DATA_REGISTRATION_STATE state = 2, mDataRadioTechnology = 0, mTAC =-1 gxf
Volte_shut_off(1).txt:16926: 01-15 21:14:18.105 D/SERVICE_STATE_TRACKER(  497): RIL_REQUEST_DATA_REGISTRATION_STATE state = 5, mDataRadioTechnology = 14, mTAC =-1 gxf

或者通过WEBIDE 看下navigator.mozMobileConnections 里voice、data

#### 如何查看信号强弱
log关键字:SIGNAL_STRENGTH

---

### BT/WIFI/NFC

#### Q. 如何如何添加WIFI AP列表使UE能自动连接这些AP
A.
- 可以在/data/misc/wifi/wpa_supplicant.conf 中添加需要自动连接的AP，但是在UE factory reset后添加的AP会被删除。
- 如果需要新增添加/system/etc/wifi/wpa_supplicant.conf
- source code路径是/device/qcom/msm8909/wpa_supplicant_overlay.conf

#### Q. 如何手动连接WIFI热点
1. 连接无密码WIFI

```
var wifi = navigator.mozWifiManager;

function sortNetworksByStrength(a, b) {
  return a.signalStrength > b.signalStrength ? -1 : 1;
}

var request = wifi.getNetworks();

request.onsuccess = function () {
  console.log('The following networks are available:');

  var networks = this.result;
  networks.sort(sortNetworksByStrength);
  
  // Let's try to connect the device to the strongest network
  wifi.associate(networks[0]);
}
```

2. 连接有密码WIFI

```
var wifi = navigator.mozWifiManager;

var request = wifi.getNetworks();

request.onsuccess = function () {
  // Let's get the first network
  var network  = this.result[0];
  var security = network.security[0];

  if (security === 'WEP') {
    network.wep = prompt('This network requires a WEP password:');
  }

  else if (security === 'WPA-PSK') {
    network.psk = prompt('This network requires a WPA Key:');
  }

  else if (security === 'WPA-EAP') {
    network.eap      = prompt('Which EAP method should be used:');
    network.identity = prompt('Which identity should be used:');
    network.password = prompt('This network requires a password:');
    network.pin      = prompt('Thanks to finally provide your own PIN:');
  }
  
  // Let's try to connect the device to the network
  wifi.associate(network);
}
```

此处需要注意的是，如果上述方式不起作用，可以尝试如下的代码：

```
      var net = {
        ssid: "SSID",
        keyManagement: "WPA-PSK",
        psk: "password"
      }

      var associateRequest = wifi.associate(new window.MozWifiNetwork(net));

      associateRequest.onsuccess = function() {
        console.log("设备进入到提供的网络的连接工作流程ok");
      };
      associateRequest.onerror = function(err) {
        console.log("设备进入到提供的网络的连接工作流程fail");
        console.log(err);
      };
```

keyManagement是必须要设定的属性，要不然无法正常连接。

更多参考信息： [WIFI information](https://developer.mozilla.org/en-US/docs/Archive/B2G_OS/API/WiFi_Information_API)

#### Q. 关于Wifi中的NVRAM Warning AP- NVRAM AP 热点 WIFI.20190317

A. 首先这不是bug，是某平台的防呆设计。
当设备未正常刷WIFI MAC地址时，此时WIFI MAC地址为某个默认的无效值，该平台的BSP模
块即会在可用wifi网络中自动增加此热点“nvram warning”。

但毕竟该AP的MAC地址仍是无效的（全0），它的出现会导致KaiOS WiFi连接AP的过程出现
某些不确定的奇怪行为。但因为这是一个平台防呆设计，KaiOS不计划对此做任何弥补性的
优化。

#### Q. 对蓝牙文件接收及其他含有通知的任务的限制 - Bluetooth reject notificaiton bar alert
A. KaiOS有几个最高优先级的显示界面，分别是电话中/calling，锁屏/lockscreen，蓝牙配对/pairing，timer/alarm等警示页面。
这些页面下所有其他提示信息窗都不能显示，也不会被显示，比如蓝牙模块收到信文件发送。
所有关于通知信息在上述屏幕没有显示的客户问题，KaiOS现有设计架构都无法处理，应当做无法改变的系统设计约束对待。
开发者自己开发的应用，也不应“期待”或尝试在这些场景下增加具备提示的能力。开发工作将很艰巨。

---

## 工厂测试
#### Q. 如何手工关闭M平台的MDlogger 以测试产品performance

连接adb，输入

```
adb root
adb remount
adb shell rm /system/bin/mdlogger
adb reboot
```

这样mdlogger就被关掉了。
此时可以比较测试两台机器做相同操作的反应速度差异
（info from viral）

---
#### Q. 如何开机直接进入MMITest开始测试，而非进入Launcher
A. 可参考如下代码。

```
diff --git a/build/settings.js b/build/settings.js
@@ -185,7 +185,7 @@ function overrideSettings(settings, config) {
 }
 
 function setHomescreenURL(settings, config) {
-  let appName = 'launcher';
+  let appName = 'mmitest';
 
   if (typeof(settings['homescreen.appName']) !== 'undefined') {
     appName = settings['homescreen.appName'];
```
（Info from Shi in case 49146）

---
## 其他
#### Q. 如何制作KAPIC版本
-----------背景-------
MTK和高通平台目前不需要执行下列操作，OEM提供出货等级的User mode版本即可执行KAPIC测试。

对于展讯平台设备，做KAPIC认证所需版本需要开启ADB。

--------如何build？-------------
请从这个地址下载adb.c文件的压缩包，解压缩成.c文件后，在system/core/adb目录，“临时”为此编译替换项目的这个文件，然后编译一次生成测试软件。
链接：https://pan.baidu.com/s/13tIzKmUsIi1GlFNSvN9Zzw 
提取码：u2t5 

除了这个替换，其他功能和编译选项应和出货用软件的配置一致。

该版本即可实现user版本下ADB可用。

注意：该版本只为生成KAPIC认证软件。不能出货。

---
#### Q. AudioChannelClient使用
1. 定义
<https://bugzilla.kaiostech.com/show_bug.cgi?id=51295>
2. 使用场景 
后台播放music/FM，FM/music 切换频道/切换歌曲间隙不让后台播放声音；
录像/录音的时候不让后台music/FM播放(现在代码的策略是播放一个静音的文件)等等。
3. 使用举例
 <https://bugzilla.kaiostech.com/show_bug.cgi?id=62603>
 <https://bugzilla.kaiostech.com/show_bug.cgi?id=62682>

---
#### Q. KaiOS音量在耳机和扬声器不能分开管理
A. KaiOS的耳机音量和扬声器的音量等级参数是同一套，调整任何一个都会直接改变另一个。目前的设计就是如此。有需求的OEM请自行开发定制。

---
#### Q. 关于表情的支持情况 - Emoji emoticon
A. KaiOS的Emoji支持情况总结如下：
1. KaiOS不支持emoji 输入，但是支持显示。
2. Emoji是通过字体 noto color emoji素材支持的。KaiOS目前基线不会随时根据网上开源资源升级而更新发布内容。OEM想扩充的话，可到此地址下载最新版本，替换默认素材文件。
 http://www.google.cn/get/noto/

3. 目前WA的Kaios 版本不支持Emoji。彻底不支持。
4. 从其他OS的WA，发送WA私有emoji，或者说WA定义的Emoji信息 到KiaOS设备的WA的情况，会出现两者Emoji库不兼容的问题。目前WA没有升级这部分功能的计划。
5. 如果发送的Emoji是android的Emoji，也即从Android输入法的emoji菜单输入到WA好友，在WA 的kaios 版本，基本可以正常阅读。短信等其他功能依然。
6. WA自己定义的Emoji跨应用兼容性不需要考虑。当然用户也没有机会在非WA的环境下互发WA自己的Emoji。如果碰巧发出的WA自己定义的Emoji和安卓平台编码相同，KaiOS的WA内大多可以显示。但有个已知bug：一旦遇到不兼容的Emoji，则WA内会把所有emoji显示为乱码，而非只是不兼容的那个。

---
#### Q. 如何修改耳机默认音量-default volume headset
A.当手机插入耳机后,系统会检测到有输出设备改变,会执行MaybeUpdateVolumeSettingToDatabase方法,调用AUDIO_STREAM_MUSIC的默认音量.
所以修改耳机默认音量可以对如下值进行修改:
例如:修改耳机默认音量为:6

```
diff --git a/dom/system/gonk/AudioManager.cpp b/dom/system/gonk/AudioManager.cpp
index 6e524e9b039b..7522b7a6eeef 100644
--- a/dom/system/gonk/AudioManager.cpp
+++ b/dom/system/gonk/AudioManager.cpp
@@ -90,7 +90,7 @@ static const uint32_t sDefaultStreamVolumeTbl[AUDIO_STREAM_CNT] = {
   3,  // voice call
   8,  // system
   8,  // ring
-  8,  // music
+  6,  // music
   8,  // alarm
   8,  // notification
   8,  // BT SCO
```
(Info from Jianyu)

---
#### Q. 推荐SCM人员的Git入门培训
A. 可以从这个网站开始学习git始用：
https://backlog.com/git-tutorial/cn/intro/intro1_1.html
（suggested by Hongxiu) 

---
#### Q. 怎么从Log里看b2g进程是否成功完全启动
A. `adb root; adb shell; b2g-info` 可以查看当前kaios相关的进程。

---
#### Q. 执行curl指令报CERTIFICATE_VERIFY_FAILED错误
A. 原因是没有配置CA证书，可以参考下面的解决方法：

```
1，让客户在external/curl　androidconfigure 里面配置--with-ca-path=“客户自己的CA证书”

2，或者使用Mozilla的ca-bundle.crt证书，在curl指令中指定证书的路径，例如：
curl -a --cacert /system/etc/ca-bundle.crt --capath /system/etc https://www.cnblogs.com

```

---
#### Q. KaiOS应用开发如何起步 - application develop new app
OEM/ODM工程师学习KaiOS新应用开发的最快捷方式，就是通读计算器这个应用。
这个app只有700行左右代码，除去逻辑计算的行数就更少了。但它包含一个应用构造要用的所有“基础”内容。
再通过检索它如何放进最终的代码编译出来，就能了解一个app从无到有建立需要的全部线索。
