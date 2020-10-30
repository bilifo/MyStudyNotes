# 简述
apn即"接入点名称",用来标识GPRS(用无线分组业务,是GSM移动电话用户可以使用的一种移动数据业务。是人们常说的2.5G网络,现在被3G,4G取代)的业务种类.
它决定了手机通过哪种接入方式来访问网bai络。对于手机用户来说，可以访问的外部网络类型有很多，例如：Internet、WAP网站、集团企业内部网络、行业内部专用网络。而不同的接入点所能访问的范围以及接入的方式是不同的，网络侧如何知道手机激活以后要访问哪个网络从而分配哪个网段的IP呢，这就要靠APN来区分了，即APN决定了用户的手机通过哪种接入方式来访问什么样的网络。

# Android系统中APN的配置
Android系统的APN配置文件：frameworks/base/core/res/res/xml/apns.xml   
第三方的APN配置文件：device/generic/goldfish/data/etc/apns-conf.xml   
在编译该product（goldfish）时会将device/generic/goldfish/data/etc/apns-conf.xml文件拷贝到system/etc/目录下，最后打包到system.img中  

# Apn参数解析
|参数|作用|
|-|-|
|Carrier|apn的名字，可为空，只用来显示apn列表中此apn的显示名字。|
|numeric|运营商编号，如46000|
|Mcc|由三位数组成。 用于识别移动用户的所在国家;|
|Mnc|由两位或三位组成。 用于识别移动用户的归属PLMN。 MNC的长度（两位或三位数）取决于MCC的值。|
|Apn|APN网络标识（接入点名称），是APN参数中的必选组成部分。此标识由运营商分配。|
|Proxy|代理服务器的地址|
|Port|代理服务器的端口号|
|Mmsc|MMS中继服务器/多媒体消息业务中心，是彩信的交换服务器。|
|Mmsproxy|彩信代理服务器的地址|
|Mmsport|彩信代理服务器的端口号|
|Protocol|支持的协议IPV4IPV6，不配置默认为IPV4。|
|roaming_protocol|漫游时连接该APN所用的协议，如IPV4IPV6|
|carrier_enabled|用于标识APN是否可用|
|bearer|无线接入，如LTE和eHRPD|
|bearer_bitmask|无线接入技术位掩码，用于标明当前APN可以包含的RAT|
|User|用户|
|Password|密码|
|server|服务器地址|
|Authtype|apn的认证协议，PAP为口令认证协议，是二次握手机制。CHAP是质询握手认证协议，是三次握手机制。None(0)、PAP(1)、CHAP(2)、PAP or CHAP(3)|
|mvno_type|移动虚拟网络运营商（Mobile virtual network operator）的类型，可用的数据有spn,IMSI,GID(Group Identifier Level 1) |  
|mvno_match_data| MVNO_TYPE数据，这个值是和MVNO_TYPE对应的。例如:SPN:A MOBILE,BEN NL,IMSI:302720x94,2060188 GID:4E,33|
|sub_id|用于表明这个APN属于哪个subscription，此值从siminfo表获取 |
|profile_id| Profile id，profile是modem侧存储信息的方式，这个值将APN和modem侧的profile联系起来|
|modem_cognitive| 用于表明这个APN是否会在modem侧设置|
|max_conns| APN支持的最大连接数量|
|wait_time| 使用该APN进行数据连接时，如果失败，retry要等待的时间|
|max_conns_time| 限制APN最大连接的时间 mtu 使用该APN建立的连接，可以传输的最大单元 |
|edited| 表明该APN是否被用户或运营商添加、编译或删除的状态|
|user_visible| APN是否对用户可见|
|user_editable| 用户是否可以编辑APN|
|owned_by| APN的拥有者，0或者1 |
|apn_set_id |APN集合id，如果用户或者框架选择了一个apn作为首选APN，那么所有与选中apn相同集合id的APN拥有更高的优先级|



# apn接入点类型
|类型|作用|
|-|-|
|Default|默认网络连接|
|Mms|彩信专用连接，此连接与default类似，用于与载体的多媒体信息服务器对话的应用程序|
|Supl|是Secure User Plane Location“安全用户面定位”的简写，此连接与default类似，用于帮助定位设备与载体的安全用户面定位服务器对话的应用程序|
|Dun|Dial Up Networking拨号网络的简称，此连接与default连接类似，用于执行一个拨号网络网桥，使载体能知道拨号网络流量的应用程序|
|Hipri|高优先级网络，与default类似，但路由设置不同。只有当进程访问移动DNS服务器，并明确要求使用requestRouteToHost(int, int)才会使用此连接|
|ims| 普通通话,可以不用上层设置,moden端默认会设置|
|

此表中的数据连接优先级是:Hipri>Dun>Supl>Mms>Default

# 虚拟运营商的APN
虚拟运营商（MVNO）没有自营网段，使用了主运营商的网段，因而和主运营商有相同的MCCMNC。为了能够与主运营商区分，虚拟运营商的APN还包含了MVNO参数。MVNO参数分为SPN/PNN/IMSI/GID1，是从SIM卡对应栏位读取的值，目的是从该值中判断该SIM卡是否属于MVNO。
在加载MVNO SIM卡的APN时，会同时去匹配MCCMNC和MVNO参数

# apn在手机中的存储
apn文件：System/etc/apn-conf.xml  
apn数据存储的数据库：/data/data/com.android.providers.telephony/databases/ telephony.db Carriers表