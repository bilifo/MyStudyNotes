1.导入依赖

    implementation 'com.orhanobut:logger:2.2.0'
2.配置初始化选项(网上都说是可选,但测试及github上都是必写,可能和安卓6.0后权限有关)

    Logger.addLogAdapter(new AndroidLogAdapter()); /** 使用前必写*/
2.2可选初始化设置

    FormatStrategy formatStrategy
    =PrettyFormatStrategy.newBuilder()
    .showThreadInfo(false)/** (可选)是否显示线程信息 默认：显示*/
    .methodCount(0)/** (可选)调用该log的方法栈栈顶前几个 默认：2*/
    .methodOffset(7)/** (可选)隐藏内部方法调用，直到偏移量。默认的5*/
    .logStrategy(customLog)/** (可选)将日志策略更改为打印输出。默认LogCat*/
    .tag("My custom tag")/** (可选)TAG 为 XXX,默认 TAG: PRETTYLOGGER*/
    .build();
    Logger.addLogAdapter(new AndroidLogAdapter(formatStrategy));

3.打印不同level的Log

    Logger.v(String message); /** VERBOSE级别，可添加占位符*/
    Logger.d(Object object); /** DEBUG级别，打印对象*/
    Logger.d(String message); /** DEBUG级别，可添加占位符*/
    Logger.i(String message); /** INFO级别，可添加占位符*/
    Logger.w(String message); /** WARN级别，可添加占位符*/
    Logger.e(String message); /** ERROR级别，可添加占位符*/
    Logger.e(Throwable throwable, String message); /** ERROR级别，可添加占位符*/
    Logger.wtf(String message); /** ASSERT级别，可添加占位符*/

    支持字符串格式参数
    Logger.d("hello %s", "world");

    Json 和 Xml 支持 (输出将处于调试级别)
    Logger.xml(String xml);
    Logger.json(String json);

    也可以和原生Log一样
    Logger.log(int priority, @Nullable String tag, @Nullable String message, @Nullable Throwable throwable);
4.日志过滤

    AndroidLogAdapter通过检查此函数来检查是否应打印日志。如果要禁用/隐藏日志以进行输出, 可重写方法。
    Logger.addLogAdapter(new AndroidLogAdapter() {
      @Override public boolean isLoggable(int priority, String tag) {//priority 日志等级:Logger.VERBOSE~Logger.ASSERT
        return BuildConfig.DEBUG;//BuildConfig.DEBUG==true
      }
    });
5.保存日志

    FormatStrategy formatStrategy =
    CsvFormatStrategy.newBuilder()
    .tag("custom")/** 抓取指定TAG的日志段*/
    .build();
    Logger.addLogAdapter(new DiskLogAdapter(formatStrategy));
    //在sdcard/logger/目录中
