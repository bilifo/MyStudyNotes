1. 先使用 ssh localhost来检测下是否安装了ssh,如果没有安装,使用 sudo apt-get install openssh-server 安装
2. 运行ssh.使用 sudo /etc/init.d/ssh start
3. 测试是否能使用ssh, ssh 127.0.0.1 或 ssh localhost
4. 查看ssh连接状态, ps -e | grep ssh
5. 需要连接的电脑的ssh 公钥,放到 authorized_keys 指定文件里
6. 需要连接的电脑,使用 ssh 连接的电脑的用户名@服务器ip地址 ,进行连接

以上是同一个局域网下的ssh连接方法,但在非局域网,如家里面的电脑连接公司电脑.就需要内网穿透了.
内网穿透,网上的文章一般都会使用到某些工具,我暂时不需要,以后再研究吧


问题1:ssh: connect to host localhost port 22: Connection refused
原因:可能是端口没有打开, 本地防火墙拒绝, 本机没有ssh服务,或者根本没生成ssh秘钥;
解决:
生成秘钥:ssh-keygen -t rsa (连按回车，生成秘钥)

问题2:root@127.0.0.1: Permission denied (publickey).
原因:生成的ssh秘钥,分为公钥(~/.ssh/id_rsa.pub)和私钥(~/.ssh/id_rsa),公钥（~/.ssh/id_rsa.pub）应该保存在远程服务端的已认证的秘钥文件内（~/.ssh/authorized_keys）,这个过程是允许特定公钥的设备来连接该机,其他机器要连接服务器,也需要将公钥发给服务器,放到authorized_keys下
解决:使用 cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys 将公钥放到指定文件里