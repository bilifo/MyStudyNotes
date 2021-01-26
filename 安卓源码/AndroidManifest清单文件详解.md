每个应用项目必须在项目源设置的根目录中加入 AndroidManifest.xml 文件（且必须使用此名称）。 清单文件会向 Android 构建工具、Android 操作系统和 Google Play 描述应用的基本信息。  

重点是，清单文件需声明以下内容：

1. 应用的软件包名称，其通常与代码的命名空间相匹配。
2. 用到的组件。应用的 Activity、服务和广播接收器均由 Intent 激活。 Intent 是由 Intent 对象定义的消息，用于描述要执行的操作，其中包括要执行操作的数据、应执行操作的组件类别以及其他相关说明。
3. 需要的权限
4. 应用需要的硬件和软件功能。<uses-feature> 元素允许您声明应用所需的硬件和软件功能。

**<action>**
包含于<intent-filter>，<intent-filter> 元素必须包含一个或多个 <action> 元素。如果 Intent 过滤器中没有 <action> 元素，则过滤器不接受任何 Intent 对象。

**<activity>**

|属性|作用|
|-|-|
|android:allowEmbedded|表示该 Activity 可作为其他 Activity 的嵌入式子项启动。此属性尤其适用于子项位于其他 Activity 所拥有容器（如 Display）中的情况。例如，用于 Wear 自定义通知的 Activity 必须声明此属性，以便 Wear 在其位于另一进程内的上下文流中显示 Activity。该属性的默认值为 false。|
|android:allowTaskReparenting|当下一次将启动 Activity 的任务转至前台时，Activity 是否能从该任务转移至与其有相似性的任务 —“true”表示可以转移，“false”表示仍须留在启动它的任务处。</br>如果未设置该属性，则对 Activity 应用由 <application> 元素的相应 allowTaskReparenting 属性所设置的值。默认值为“false”。</br>正常情况下，Activity 启动时会与启动它的任务关联，并在其整个生命周期中一直留在该任务处。当不再显示现有任务时，您可以使用该属性强制 Activity 将其父项更改为与其有相似性的任务。该属性通常用于将应用的 Activity 转移至与该应用关联的主任务。</br>例如，如果电子邮件消息包含网页链接，则点击该链接会调出可显示该网页的 Activity。该 Activity 由浏览器应用定义，但作为电子邮件任务的一部分启动。如果将该 Activity 的父项更改为浏览器任务，则它会在浏览器下一次转至前台时显示，在电子邮件任务再次转至前台时消失。</br>Activity 的相似性由 taskAffinity 属性定义。通过读取任务根 Activity 的相似性即可确定任务的相似性。因此，按照定义，根 Activity 始终位于具有同一相似性的任务中。由于具有“singleTask”或“singleInstance”启动模式的 Activity 只能位于任务的根，因此更改父项仅限于“standard”和“singleTop”模式。（另请参阅 launchMode 属性。）|
|android:alwaysRetainTaskState|系统是否始终保持 Activity 所在任务的状态 —“true”表示是，“false”表示允许系统在特定情况下将任务重置到其初始状态。默认值为“false”。该属性只对任务的根 Activity 有意义；所有其他 Activity 均可忽略该属性。</br>正常情况下，当用户从主屏幕重新选择某个任务时，系统会在特定情况下清除该任务（从根 Activity 上的堆栈中移除所有 Activity）。通常，如果用户在一段时间（如 30 分钟）内未访问任务，系统会执行此操作。</br>不过，如果该属性的值是“true”，则无论用户如何返回任务，该任务始终会显示最后一次的状态。例如，该属性非常适用于网络浏览器这类应用，因为其中存在大量用户不愿丢失的状态（如多个打开的标签）。|
|android:autoRemoveFromRecents|由具有该属性的 Activity 启动的任务是否一直保留在概览屏幕中，直至任务中的最后一个 Activity 完成为止。若为 true，则自动从概览屏幕中移除任务。它会替换调用方使用的 FLAG_ACTIVITY_RETAIN_IN_RECENTS。它必须是布尔值“true”或“false”。|
|android:banner|一种为其关联项提供扩展图形化横幅的可绘制资源。可与 <activity> 标记联用，为特定 Activity 提供默认横幅；也可与 <application> 标记联用，为所有应用 Activity 提供横幅。</br>系统使用横幅，以在 Android TV 主屏幕中表示应用。由于横幅只显示在主屏幕中，因此只有 Activity 可处理 CATEGORY_LEANBACK_LAUNCHER Intent 的应用才能指定该横幅。</br>必须将该属性设置为对包含图像的可绘制资源的引用（例如 "@drawable/banner"）。没有默认横幅。</br>如需了解详细信息，请参阅“电视应用入门指南”中的提供主屏幕横幅。|
|android:clearTaskOnLaunch|每当从主屏幕重新启动任务时，是否都从该任务中移除根 Activity 之外的所有 Activity —“true”表示始终将任务清除至只剩其根 Activity；“false”表示不清除。默认值为“false”。该属性只对启动新任务的 Activity（根 Activity）有意义；任务中的所有其他 Activity 均可忽略该属性。</br>若值为“true”，则每次当用户再次启动任务时，无论用户最后在任务中正在执行哪个 Activity，也无论用户是使用返回还是主屏幕按钮离开，系统都会将用户转至任务的根 Activity。当值为“false”时，可在某些情况下清除任务中的 Activity（请参阅 alwaysRetainTaskState 属性），但也有例外。</br>例如，假设用户从主屏幕启动Activity P，然后从该处转到 Activity Q。接着，该用户按下主屏幕按钮，然后返回到 Activity P。正常情况下，用户将看到 Activity Q，因为这是其最后在 P 的任务中所执行的 Activity。不过，如果 P 将此标志设置为“true”，则当用户按下主屏幕将任务转入后台时，系统会移除 P 上方的所有 Activity（在本例中为 Q）。因此用户在返回任务时只会看到 P。</br>如果该属性和 allowTaskReparenting 的值均为“true”，则如上所述，任何可更改父项的 Activity 都将转移至与其有相似性的任务；而其余 Activity 随即会被移除。|
|android:colorMode|请求在兼容设备上以广色域模式显示 Activity。在广色域模式下，窗口可以在 SRGB 色域之外进行渲染，从而显示更鲜艳的色彩。如果设备不支持广色域渲染，则此属性无效。如需了解在广色域模式下进行渲染的详细信息，请参阅使用广色域内容增强图形。|
|android:configChanges|列出 Activity 将自行处理的配置变更。在运行时发生配置变更时，默认情况下会关闭 Activity 并将其重启，但使用该属性声明配置将阻止 Activity 重启。相反，Activity 会保持运行状态，并且系统会调用其 onConfigurationChanged() 方法。若有多个值，则使用“\|”进行分隔|
|android:directBootAware|Activity 是否支持直接启动，即其是否可以在用户解锁设备之前运行。默认值为 "false"。|
|android:documentLaunchMode|指定每次启动任务时，应如何向其添加新的 Activity 实例。该属性允许用户让多个来自同一应用的文档出现在概览屏幕中。该属性有四个值:“intoExisting”,“always”,“none”,“never”|
|android:enabled|系统是否可实例化 Activity — "true" 表示可以，“false”表示不可以。默认值为“true”。\<application\>元素拥有自己的 enabled 属性，该属性适用于所有应用组件，包括 Activity。只有在 \<application\>和\<activity\>属性都为“true”（因为它们都默认使用该值）时，系统才能将 Activity 实例化。如果其中一个属性是“false”，则无法实例化 Activity。|
|android:excludeFromRecents|是否应从最近使用的应用列表（即概览屏幕）中排除该 Activity 启动的任务。换言之，当该 Activity 是新任务的根 Activity 时，此属性确定最近使用的应用列表中是否应出现该任务。如果应从列表中排除任务，请设置“true”；如果应将其包括在内，则设置“false”。默认值为“false”。
|android:exported|此元素设置 Activity 是否可由其他应用的组件启动 —“true”表示可以，“false”表示不可以。若为“false”，则 Activity 只能由同一应用的组件或使用同一用户 ID 的不同应用启动。如果您使用的是 Intent 过滤器，则不应将此元素设置为“false”。否则，在应用尝试调用 Activity 时，系统会抛出 ActivityNotFoundException 异常。相反，您不应为其设置 Intent 过滤器，以免其他应用调用 Activity。</br>如果没有 Intent 过滤器，则此元素的默认值为“false”。如果您将元素设置为“true”，则任何知道其确切类名的应用均可访问 Activity，但在系统尝试匹配隐式 Intent 时，该 Activity 无法解析。</br>此属性并非是限制 Activity 向其他应用公开的唯一方式。您还可使用权限来限制哪些外部实体能够调用 Activity（请参阅 permission 属性）。|
|android:finishOnTaskLaunch|每当用户再次启动 Activity 的任务（在主屏幕上选择任务）时，是否应关闭（完成）现有的 Activity 实例 —“true”表示应关闭，“false”表示不应关闭。默认值为“false”。如果此属性和 allowTaskReparenting 均为“true”，则优先使用此属性。系统会忽略 Activity 的相似性。系统不会更改 Activity 的父项，而是将其销毁。</br>
|android:hardwareAccelerated|是否应为此 Activity 启用硬件加速渲染 —“true”表示应启用，“false”表示不应启用。默认值为“false”。</br>自 Android 3.0 开始，应用可使用经硬件加速的 OpenGL 渲染器，从而提高许多常见 2D 图形运算的性能。启用硬件加速渲染器后，Canvas、Paint、Xfermode、ColorFilter、Shader 和 Camera 中的大多数运算都会获得加速。这可以提高动画及滚动的流畅度并改善整体响应，即便是未显式利用框架 OpenGL 库的应用也会从中受益。由于启用硬件加速会增加资源消耗，因此您的应用将占用更多内存。</br>请注意，并非所有 OpenGL 2D 运算都会获得加速。如果您启用硬件加速渲染器，请对应用进行测试，确保其在利用渲染器时不会出错。|
|android:icon|表示 Activity 的图标。当需要在屏幕上呈现 Activity 时，系统会向用户显示图标。例如，启动器窗口中会显示启动任务的 Activity 所用图标。该图标通常附带标签（请参阅 android:label 属性）。必须将该属性设置为对包含图像定义的可绘制资源的引用。如果未设置该属性，则转而使用为应用整体指定的图标（请参阅 <application> 元素的 icon 属性）。</br>Activity 的图标（无论是在此处设置，还是由 <application> 元素设置）同时也是 Activity 所有 Intent 过滤器的默认图标（请参阅 <intent-filter> 元素的 icon 属性）。|
|android:immersive|为当前 Activity 进行沉浸模式设置。如果在应用清单文件条目中为此 Activity 将 android:immersive 属性设置为 true，则 ActivityInfo.flags 成员会始终设置其 FLAG_IMMERSIVE 位（即便在运行时使用 setImmersive() 方法更改沉浸模式）。|
|android:label|一种可由用户读取的 Activity 标签。在必须向用户呈现 Activity 时，屏幕上会显示此标签。此标签通常与 Activity 图标一并显示。如果未设置该属性，则转而使用为应用整体设置的标签（请参阅 <application> 元素的 label 属性）。</br>Activity 的标签（无论是在此处设置，还是由 <application> 元素设置）同时也是 Activity 所有 Intent 过滤器的默认标签（请参阅 <intent-filter> 元素的 label 属性）。</br>您应将此标签设置为对字符串资源的引用，以便可以像界面中的其他字符串那样对其进行本地化。不过，为便于开发应用，您也可将其设置为原始字符串。|
|android:launchMode|有关应如何启动 Activity 的指令。共有四种模式可与 Intent 对象中的 Activity 标记（FLAG_ACTIVITY_* 常量）协同工作，以确定在调用 Activity 处理 Intent 时应执行的操作。这些模式是：“standard” “singleTop” “singleTask” “singleInstance”|
|android:lockTaskMode|确定当设备在锁定任务模式下运行时，系统如何显示此 Activity。Android 可以类似于 Kiosk 的沉浸式方式（称为锁定任务模式）运行任务。当系统在锁定任务模式下运行时，设备用户通常无法查看通知、访问非白名单应用或返回主屏幕（除非主页应用已列入白名单）。只有经设备政策控制器 (DPC) 列入白名单后，应用才能在系统处于锁定任务模式时运行。但是，系统和特权应用无需列入白名单便可在锁定任务模式下运行。|
|android:maxRecents|概览屏幕中位于此 Activity 根位置处的最大任务数。达到该条目数时，系统会从概览屏幕中移除近期最少使用的实例。有效值为 1 至 50（内存较小的设备使用 25）；0 为无效值。该值必须是整数，例如 50。默认值为 16。|
|android:maxAspectRatio|Activity 支持的最大纵横比。如果应用在设备上以较宽的纵横比运行，则系统会自动为其添加黑边，未使用的屏幕部分不添加黑边，以便应用可按其指定的最大纵横比运行。最大纵横比表示为设备长边除以短边的商（小数形式）。例如，如果最大纵横比为 7:3，则此属性的值应设为 2.33。在非穿戴式设备上，此属性的值需设为大于或等于 1.33。在穿戴式设备上，该值必须大于或等于 1.0。否则，系统将忽略此设定值。|
|android:noHistory|当用户离开 Activity 且屏幕上不再显示该 Activity 时，是否应从 Activity 堆栈中将其移除并完成（调用其 finish() 方法）—“true”表示应将其完成，“false”表示不应将其完成。默认值为“false”。</br>“true”一值表示 Activity 不会留下历史跟踪记录。它不会留在任务的 Activity 堆栈内，因此用户将无法返回 Activity。在此情况下，如果您通过启动另一个 Activity 来获取该 Activity 的结果，系统永远不会调用 onActivityResult()。|
|android:parentActivityName|Activity 逻辑父项的类名称。此处的名称必须与为相应 <activity> 元素的 android:name 属性所指定的类名称一致。</br>系统会读取该属性，以确定当用户按下操作栏中的“向上”按钮时应该启动哪一个 Activity。系统还可利用这些信息，通过 TaskStackBuilder 合成 Activity 的返回栈。|
|android:permission|启动 Activity 或以其他方式使 Activity 响应 Intent 时，客户端必须具备的权限的名称。如果系统尚未向 startActivity() 或 startActivityForResult() 的调用方授予指定权限，则其 Intent 将不会传递给 Activity。</br>如果未设置该属性，则对 Activity 应用由 <application> 元素的 permission 属性所设置的权限。如果二者均未设置，则 Activity 不受权限保护。|
|android:process|应在其中运行 Activity 的进程的名称。正常情况下，应用的所有组件均以为应用创建的默认进程名称运行，您无需使用该属性。但如有必要，您可以使用该属性替换默认进程名称，以便将应用组件散布到多个进程中。|
|android:relinquishTaskIdentity|Activity 是否会将其任务标识符交给任务栈中在其之上的 Activity。如果任务的根 Activity 将该属性设置为“true”，则该任务会用其下一个 Activity 的 Intent 替换基本 Intent。如果下一个 Activity 也将该属性设置为“true”，则该 Activity 会将基本 Intent 让给其在同一任务中启动的其他 Activity。系统会继续为每个 Activity 执行此过程，直至遇到某个 Activity 将该属性设置为“false”为止。默认值为“false”。如果将该属性设置为“true”，则 Activity 还可利用 ActivityManager.TaskDescription 来更改概览屏幕中的标签、颜色和图标。|
|resizeableActivity|指定应用是否支持多窗口显示。您可以在 <activity> 或 <application> 元素中设置该属性。如果您将该属性设置为 true，则用户可以在分屏和自由窗口模式下启动 Activity。如果您将该属性设置为 false，则 Activity 不支持多窗口模式。如果该值为 false，且用户尝试在多窗口模式下启动 Activity，则该 Activity 将全屏显示。如果应用面向 API 级别 24 或更高级别，但您未指定该属性的值，则该属性的值默认设为 true。|
|android:screenOrientation|Activity 在设备上的显示方向。如果 Activity 是在多窗口模式下运行，则系统会忽略该属性。|
|android:showForAllUsers|当设备的当前用户不是启动 Activity 的用户时，是否要显示 Activity。您可将此属性设置为字面量值（"true" 或 "false"），或包含布尔值的资源或主题属性。|
|android:stateNotNeeded|在不保存 Activity 状态的情况下，能否终止并成功重启该 Activity —“true”表示可在不考虑其之前状态的情况下重启，“false”表示需要之前的状态。默认值为“false”。</br>正常情况下，为保存资源而暂时关闭 Activity 前，系统会调用其 onSaveInstanceState() 方法。该方法会将 Activity 的当前状态存储在一个 Bundle 对象中，然后在 Activity 重启时将其传递给 onCreate()。如果将该属性设置为“true”，则系统可能不会调用 onSaveInstanceState()，并且会向 onCreate() 传递 null（而非 Bundle）— 这与 Activity 首次启动时的情况完全相同。</br>“true”设置可确保 Activity 能够在未保留状态时重启。例如，显示主屏幕的 Activity 可以使用该设置，确保系统不会在该 Activity 因某种原因而崩溃时将其移除。|
|supportsPictureInPicture|指定 Activity 是否支持画中画显示。如果 android:resizeableActivity 是 false，则系统会忽略该属性。|
|android:windowSoftInputMode|Activity 的主窗口与包含屏幕软键盘的窗口之间的交互方式。该属性的设置会影响两点内容：</br>当 Activity 成为用户注意的焦点时，软键盘的状态为隐藏还是可见。对 Activity 主窗口所做的调整 — 是否将其尺寸调小，为软键盘腾出空间；或当软键盘遮盖部分窗口时，是否平移其内容以使当前焦点可见。|

**<application>**
https://developer.android.google.cn/guide/topics/manifest/application-element

