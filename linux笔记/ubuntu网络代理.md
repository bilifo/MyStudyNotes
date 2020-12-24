网络代理和路由的区别:  
网络代理,电脑非直接访问网络,而是借助代理的服务器的网络ip去访问,代理服务器再将网络转发  
路由则是本机的ip去访问网络

ubuntu设置网络代理的3种方式:
1. 临时的手段
如暂时需要通过http代理使用apt-get，您可以使用这种方式。在使用apt-get之前，在终端中输入以下命令（根据您的实际情况替换ourproxyaddress和proxyport）。 

    export http_proxy="http://用户名:密码@代理IP:代理端口"

2. 永久设置
在 /etc/apt/apt.conf 中配置  

    Acquire::http::Proxy "http://yourproxyaddress:proxyport/";

(这一行输入的时候注意，Proxy这个词和后面的“有空格，并且端口后面应该有/，并且注意如果直接把这句话拷贝过去，一定要把引号换成英文的。还有末尾的分号不要忘记。根据你的实际情况替换yourproxyaddress和proxyport)  
保存apt.conf文件。  

3. 在您的home用户目录下(或其他目录)的.bashrc文件中添加两行  

    http_proxy=http://yourproxyaddress:proxyport
    export http_proxy

保存后执行 source ~/.bashrc

