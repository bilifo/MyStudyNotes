可以在html中的<script>标签下直接编写js脚本,或者使用<script>标签的src引入外部脚本



基本语法:大致和Java一样

    1.每个语句以;结束，语句块用{...},//注释
    2.let 只在自身所在的{}花括号内起作用,且let不允许在相同作用域内，重复声明同一个变量，否则报错,即一个花括号里let只能声明一次.
      var声明函数内的局部变量.
      const 表常量
      变量前什么都不加,表全局变量
      不区分整数和浮点数，统一用Number表示
    3.JavaScript允许对任意数据类型做比较.==比较，它会自动转换数据类型再比较，很多时候，不同类型见比较会得到非常诡异的结果；===比较，它不会自动转换数据类型，如果数据类型不一致，返回false，如果一致，再比较
    4.[]数组,可以包括任意数据类型.也可以通过Array()函数实现数组.索引的起始值为0.字符串也是数组(不可变数组)
    5.JavaScript的对象是一组由键-值组成的无序集合.eg:var person={name:'Bob',age:20}
    JavaScript对象的所有属性都是字符串，不过属性对应的值可以是任意数据类型。访问属性是通过.操作符完成,也可以通过用['xxx']来访问
    6.function abs(x),function来定义函数,允许传入任意个参数而不影响调用，因此传入的参数比定义的参数多也没有问题.
    关键字arguments，它只在函数内部起作用，并且永远指向当前函数的调用者传入的所有参数。
    关键字rest参数只能写在最后，前面用...标识,表示可变参数数组
    7.lambda表达式 var fn = x => x * x ,fn为返回值,x为参数,x*x是返回表达式
    8.js允许先使用,后声明,即声明可以在任何地方.但在js文件开头写"use strict",启动严格模式,不允许使用未定义的变量
    9.方法名或变量名前加下划线 _ 不是js的要求,只是约定俗成的表示这是应该私有的变量或方法
    10.在方法或变量名前加 exports.XXX 或者 使用 module.exports=XXX,来暴露这个方法或变量为全局可用.要使用时,为了便于区分全局和本地,js中需要使用 require('全局变量或方法所在文件.js')来引进这个js文件.或者是html中使用script标签引入那个js文件.有点像java的import,就是写着有些别扭.
    11.js是支持函数式编程的,即 var 变量=function(),变量就绑定这个函数方法,而且传递这个绑定变量时,可以不需要传入参数.如:
      var aaa=function(a,b){console.log("a:"+a);console.log("b:"+b);}
      var bbb=function(a){console.log("a:"+a);a(1,2);console.log("a:"+a(3,4));}
      bbb(aaa);

数据类型:

6 种不同的数据类型：string,number,boolean,object(Object,Date,Array),function,symbol. 2 种空类型:null(对象或值为空) 和 undefind(类或方法未定义,没声明)
    Number() 转换为数字， String() 转换为字符串， Boolean() 转化为布尔值。
    typeof 获得 JavaScript 变量的数据类型 eg:typeof "mimu" 结果:string
    instanceof 判断 JavaScript 变量的数据类型是否和某种类型相同.但是对于对象是(Array,Date)的比较,会不唯一,即和Array比较会返回true,和Object比较也会返回true.建议还是使用constructor eg:"mimu" instanceof string 结果:true
    constructor 属性返回所有 JavaScript 变量的构造函数。

字符串:
    可以像数组一样通过下标查询单独字符,但无法修改,所有的字符串操作,不会改变原有字符串的内容，而是返回一个新字符串

    var lower = "Hello".toLowerCase()//字符串全部变为小写
    var uper = "hello".toUpperCase()//字符串全部变为大写
    indexOf()//会搜索指定字符串出现的位置
    substring()//返回指定索引区间的子串
    正则表达式通常用于两个字符串方法 : search() 和 replace()。

数组:[]
    直接给Array的length赋一个新的值会导致Array大小的变化.
    Array可以通过索引把对应的元素修改为新的值.如果通过索引赋值时，索引超过了范围，同样会引起Array大小的变化.

    indexOf()//来搜索一个指定的元素的位置
    slice()//截取Array的部分元素，然后返回一个新的Array
    push()//向Array的末尾添加若干元素
    pop()//则把Array的最后一个元素删除掉
    unshift()//往Array的头部添加若干元素
    shift()//把Array的第一个元素删掉
    sort()//对当前Array进行排序
    reverse()//反转数组
    splice()//从指定的索引开始删除若干元素，然后再从该位置添加若干元素 eg:arr.splice(2, 3, 'Google', 'Facebook');//从索引2开始删3个数,并添加'Google', 'Facebook'
    concat()//把当前的Array和另一个Array连接起来，并返回一个新的Array.(注意,该方法自动将多维降为一维)
    join()//把当前Array的每个元素都用指定的字符串连接起来,返回一个字符串 eg:['A', 'B', 'C', 1, 2, 3].join('-'); // 'A-B-C-1-2-3'

set:
    创建:new Set()
    add()//添加
    delete()//删除

Map或Dictionary:{}

    set('键',value)和get('键')来添加和获得
    has('键')//判断存在

对象:
    js对象是键值对的容器.如:var person={name:"蔡徐坤",age:50,like:function(){return "唱,跳,rap,打篮球";}},这样我们能通过person.name得到"蔡徐坤"
    用in判断一个属性存在.
json:
    JSON.stringify(对象);序列化为json
    JSON.parse("...");反序列化,解析为对象

比较运算符:
    ==    等于
    ===   绝对等于(值和类型均相等)
    !=    不等于
    !==   不绝对等于(值或者类型不相等,或者都不相等)

输出打印:
    console.log(XXX) 和安卓的Log.d差不多

弹出警告框:
    alert("XXXX");  和安卓的toast差不多

HTML DOM:
    当网页被加载时，浏览器会创建页面的文档对象模型（Document Object Model）.Document 对象是 HTML 文档的根节点。通过可编程的对象模型，JavaScript 获得了足够的能力来创建动态的 HTML。(请查看"DOM结构图")
    提示：Document 对象是 Window 对象的一部分，可通过 window.document 属性对其进行访问。

    查找HTML元素:
    一/通过id查找: var x=document.getElementById("intro"); //找id为intro的标签
    二/通过标签名查找: var y=x.getElementsByTagName("p");//查找所有 P 标签
    三/通过类名查找: var x=document.getElementsByClassName("intro"); //查找class='intro'的标签

点击事件:
    window.document.getElementById("id名").onclick=function(){ ...... };

define定义一个可被其他js使用的模块:
    define([module-name], [array-of-dependencies], module-factory-or-object);
    第一个参数,模块名称,可省略.如果省略,则文件名就是模块名
    第二个参数,所依赖的模块,可省略.
    第三个参数,模块的实现,或js对象

window.customElements.define自定义标签:
    window.customElements.define("标签名称",标签类或标签的js实现)

js的模块化import和require:
    require/exports 是 CommonJS/AMD 中为了解决模块化语法而引入的
    import/export 是ES6引入的新规范，因为浏览器引擎兼容问题，需要在node中用babel将ES6语法编译成ES5语法

    require 是运行时调用，所以理论上可以运作在代码的任何地方
    import 是编译时调用，所以必须放在文件的开头

    require 是赋值过程，其实require的结果就是对象、数字、字符串、函数等，再把结果赋值给某个变量。它是普通的值拷贝传递。
    import 是解构过程。使用import导入模块的属性或者方法是引用传递。且import是read-only的，值是单向传递的。default是ES6 模块化所独有的关键字，export default {} 输出默认的接口对象，如果没有命名，则在import时可以自定义一个名称用来关联这个对象

    示例:    
    1/require
    ------------------------
    // module.js
    module.exports = {
      a: function() {
        console.log('exports from module');
      }
    }
    -----------------------
    // sample.js
    var obj = require('./module.js');
    obj.a()  // exports from module
    ----------------------
    当我们不需要导出模块中的全部数据时，使用大括号包含所需要的模块内容。
    ----------------------
    // module.js
    function test(str) {
      console.log(str);
    }
    module.exports = {
      test
    }
    --------------------
    // sample.js
    let { test } =  require('./module.js');
    test ('this is a test');
    -----------------

    2/import
    使用import导出的值与模块中的值始终保持一致，即引用拷贝.import必须结合export使用
    ----------------------
    // module.js
    export function test(args) {
      console.log(args);
    }
    // 定义一个默认导出文件, 一个文件只能定义一次
    export default {
      a: function() {
        console.log('export from module');
      }
    }

    export const name = 'gzc'
    -------------------
    // sample.js  使用 _ 导出export default的内容
    import _ , { test, name } from './a.js'
    test("my name is ${name}")  // 模板字符串中使用${}加入变量
