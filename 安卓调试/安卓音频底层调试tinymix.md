目前linux中主流的音频体系结构是ALSA（Advanced Linux Sound Architecture），ALSA在内核驱动层提供了alsa-driver，在应用层提供了alsa-lib，应用程序只需要调用alsa-lib提供的API就可以完成对底层硬件的操作.  
但是Android中没有使用标准的ALSA，而是一个ALSA的简化版叫做tinyalsa。Android中使用tinyalsa控制管理所有模式的音频通路，我们也可以使用tinyalsa提供的工具进行查看、调试。

编译安卓源码的tinyalse工具:

    mmm external/tinyalsa/

编译完成后会产生:
    tinymix   得到音频通路相关的各项配置参数。也可以通过添加参数修改其中的配置,这个一般需要结合硬件电路图
    tinyplay  播放音频
    tinycap     录音
    tinypcminfo  查看pcm通道的相关信息

补课:
查看当前声卡:cat /proc/asound/cards
补课end

使用tinymix后会出现:

    Number of controls: 876
    ctl     type    num     name                                     value
    0       INT     3       Voice Rx Device Mute                     -1 -1 -1
    1       INT     3       Voice Tx Device Mute                     -1 -1 -1
    2       INT     3       Voice Tx Mute                            -1 -1 -1
    3       INT     3       Voice Rx Gain                            -1 -1 -1
    4       ENUM    1       TTY Mode                                 OFF
    5       INT     2       Slowtalk Enable                          -1 -1
    6       INT     2       Voice Topology Disable                   -1 -1
    7       INT     2       HD Voice Enable                          -1 -1

这样的配置信息.

使用tinyplay前,要先使用tinymix配置通路

    adb shell "tinymix 'Ext_TOP_Speaker_Amp' 'Music'                       "
    adb shell "tinymix 'Ext_BOTTOM_Speaker_Amp' 'Music'                    "
    adb shell "tinymix 'SLIM RX0 MUX' 'AIF1_PB'                            "
    adb shell "tinymix 'SLIM RX1 MUX' 'AIF1_PB'                            "
    adb shell "tinymix 'CDC_IF RX0 MUX' 'SLIM RX0'                         "
    adb shell "tinymix 'CDC_IF RX1 MUX' 'SLIM RX1'                         "
    adb shell "tinymix 'SLIM_0_RX Channels' 'Two'                          "
    adb shell "tinymix 'RX INT3_1 MIX1 INP0' 'RX0'                         "
    adb shell "tinymix 'RX INT4_1 MIX1 INP0' 'RX1'                         "
    adb shell "tinymix 'COMP3 Switch' 1                                    "
    adb shell "tinymix 'COMP4 Switch' 1                                    "
    adb shell "tinymix 'SLIMBUS_0_RX Audio Mixer MultiMedia1' 1            "
    adb shell "tinyplay /sdcard/Music/1000.wav"

或者

    tinymix 0 I2SR      //0指的是ctl为0的项,选择Stereo DACR的音源为i2s  
    tinymix 1 I2SL      //选择Stereo DACL的音源为i2s  
    tinymix 2 0 0       //将Stereo DAC左右声道的mute关闭  
    tinymix 24 1        //开启喇叭的外部PA芯片  
    tinymix 40 1        //将Stereo DACR的声音路由到AUX口输出（因为实验机器喇叭挂载AUX接口上）  
    tinymix 41 1        //将Stereo DACR的声音路由到AUX口输出（因为实验机器喇叭挂载AUX接口上）  
    tinyplay z.wav  

tinycap录音前,也要使用tinymix配置


通常,在方案商提供的平台上,会存在mixer_*.xml的音频通道配置文件,里面列出了很多tinymix配置,如:
    
    <path name="speaker">
        <ctl name="RX3 MIX1 INP1" value="RX1" />
        <ctl name="SPK DAC Switch" value="1" />
    </path>

即在使用tinyplay前,要配置

    adb shell "tinymix 'RX3 MIX1 INP1' 'RX1' "
    adb shell "tinymix 'SPK DAC Switch' '1' "

如何确定mixer_*.xml的音频通道配置文件:
一般是在vendor/项目/mixer_声卡名.xml,但是有的时候也不准,可以通过抓取开机log,查询使用的是哪个声卡

    01-31 21:45:41.099   331   331 D msm8916_platform: platform_init: mixer path file is /system/etc/mixer_paths_aw8737S.xml

