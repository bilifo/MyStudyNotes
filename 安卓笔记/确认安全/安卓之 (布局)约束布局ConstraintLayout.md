约束布局ConstraintLayout 是一个ViewGroup，可以在Api9以上的Android系统使用

ConstraintLayout使用起来比RelativeLayout更灵活，性能更出色！还有一点就是ConstraintLayout可以按照比例约束控件位置和尺寸，能够更好地适配屏幕大小不同的机型。

添加依赖:

    implementation 'com.android.support.constraint:constraint-layout:1.1.3'

相对定位:

<img alt="安卓之 (布局)约束布局ConstraintLayout-2787721-ff2d4c4b39b9e98b.png" src="assets/安卓之 (布局)约束布局ConstraintLayout-2787721-ff2d4c4b39b9e98b.png" width="" height="" >

    <TextView
    android:id="@+id/TextView1"
    ...
    android:text="TextView1" />

    <TextView
    android:id="@+id/TextView2"
    ...
    app:layout_constraintLeft_toRightOf="@+id/TextView1" />

    <TextView
    android:id="@+id/TextView3"
    ...
    app:layout_constraintTop_toBottomOf="@+id/TextView1" />
常用属性：

    layout_constraintLeft_toLeftOf//当前控件的左边,位于指定控件的左边(左对齐)
    layout_constraintLeft_toRightOf//当前控件的左边,位于指定控件的右边(右衔接)
    layout_constraintRight_toLeftOf//当前控件的右边,位于指定控件的左边(左衔接)
    layout_constraintRight_toRightOf//当前控件的右边,位于指定控件的右边(右对齐)
    layout_constraintTop_toTopOf//当前控件的上边,位于指定控的上边(顶对齐)
    layout_constraintTop_toBottomOf//当前控件的上边,位于指定控件的低边(下衔接)
    layout_constraintBottom_toTopOf//当前控件的低边,位于指定控件的顶边(上衔接)
    layout_constraintBottom_toBottomOf//当前控件的低边,位于指定控件的低边(低对齐)
    layout_constraintBaseline_toBaselineOf//当前控件的中线,位于指定控件的中线(中间对齐)
    layout_constraintStart_toEndOf
    layout_constraintStart_toStartOf
    layout_constraintEnd_toStartOf
    layout_constraintEnd_toEndOf

    android:layout_marginStart//相对于指定控件开始的距离
    android:layout_marginEnd
    android:layout_marginLeft
    android:layout_marginTop
    android:layout_marginRight
    android:layout_marginBottom
    /**
    android:layout_marginRight="10dp"配合 app:layout_goneMarginRight="110dp"一起使用,在约束的布局gone时,起用goneMargin,但是一定要预先设置对应方向上的margin
    **/
    layout_goneMarginStart
    layout_goneMarginEnd
    layout_goneMarginLeft
    layout_goneMarginTop
    layout_goneMarginRight
    layout_goneMarginBottom

    /**
    设置横向偏差.能使约束偏向某一边，默认是0.5,有以下属性:
    layout_constraintHorizontal_bias (0最左边 1最右边)
    layout_constraintVertical_bias (0最上边 1 最底边)
    **/
    app:layout_constraintHorizontal_bias="0.2"

    //圆形定位3要素,就是几点钟方向,Angle 角度,Radius 半径
    app:layout_constraintCircle="@id/btnA"
    app:layout_constraintCircleAngle="135"
    app:layout_constraintCircleRadius="100dp"

    /**
    比例.可以在比率值的前面添加 W 或者 H 来分别约束宽度或者高度。这里用“H”表示以高度为约束，高度的最大尺寸就是父控件的高度，“2:1”表示高：宽 = 2 : 1. 则宽度为高度的一半：
    **/
    app:layout_constraintDimensionRatio="H,2:1"

    //使用 0dp (MATCH_CONSTRAINT)来代表填充,官方不推荐在ConstraintLayout中使用match_parent

    /**
    如果两个或以上控件通过下图的方式约束在一起，就可以认为是他们是一条链（图为横向的链，纵向同理）。
    **/
<img alt="安卓之 (布局)约束布局ConstraintLayout-2787721-b3b5a73715891a53.png" src="assets/安卓之 (布局)约束布局ConstraintLayout-2787721-b3b5a73715891a53.png" width="" height="" >

3个TextView相互约束，两端两个TextView分别与parent约束，成为一条链.
一条链的第一个控件是这条链的链头，我们可以在链头中设置 layout_constraintHorizontal_chainStyle来改变整条链的样式。chains提供了3种样式，分别是：

    CHAIN_SPREAD —— 展开元素 (默认)；
    CHAIN_SPREAD_INSIDE —— 展开元素，但链的两端贴近parent；
    CHAIN_PACKED —— 链的元素将被打包在一起。
<img alt="安卓之 (布局)约束布局ConstraintLayout-2787721-6d3fd9ce0f0cfd75.png" src="assets/安卓之 (布局)约束布局ConstraintLayout-2787721-6d3fd9ce0f0cfd75.png" width="" height="" >    


注意:约束和依赖一样是线性的,即所依赖的控件,也依赖着某种约束条件,最后追踪到所有节点,会发现某个最初控件有如下形式的依赖:

    app:layout_constraintStart_toStartOf="parent"
    app:layout_constraintTop_toTopOf="parent"
