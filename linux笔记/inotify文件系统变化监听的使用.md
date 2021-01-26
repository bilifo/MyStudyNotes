## inotify功能
**它是一个内核用于通知用户空间程序文件系统变化的机制**
为了及时让用户得知内核或底层硬件设备发生了什么改变，从而能够更好地管理设备,linux使用*hotplug*、*udev* 和 *inotify*.
* Hotplug 是一种内核向用户态应用通报关于热插拔设备一些事件发生的机制，桌面系统能够利用它对设备进行有效的管理，
* udev 动态地维护 /dev 下的设备文件，
* inotify 是一种文件系统的变化通知机制，如文件增加、删除等事件可以立刻让用户态得知

## 使用
1. 导入头文件 

    #include  <sys/inotify.h>

2. 初始化实例  
每一个 inotify 实例对应一个独立的排序的队列。
    
    int inotify_fd = inotify_init();

3. 添加/删除一个监听watch  
文件系统的变化事件被称做 watches 的一个对象管理，每一个 watch 是一个二元组（目标，事件类型掩码），目标可以是文件或目录，事件掩码表示应用希望关注的 inotify 事件，每一个位对应一个 inotify 事件。
    
    /**
     fd 是 inotify_init() 返回的文件描述符
     path 是被监视的目标的路径名（即文件名或目录名）
     mask 是事件类型掩码, 在头文件 linux/inotify.h 中定义了每一位代表的事件。一般是读写类型
     wd : Wd 是 watch 描述符
    */
    int wd = inotify_add_watch (fd, path, mask);//增加监听
    int ret = inotify_rm_watch (fd, wd);//删除监听

4. 监听信息读取  
对于instance_fd调用read进行读取即可。注意，read读出的数据只是一些字符序列，你要通过强制转换才能获得inotify_event

    size_t len = read(instance_fd, buf, BUF_LEN);

注意:其中buf是一个指向struct inotify_event数组的指针。

由于struct inotify_event长度是可变的，因此在读取inotify_event数组内容的时候需要动态计算一下时间数据的偏移量。index += sizeof(struct inotify_event)+event->len，len即name成员的长度。

inotify_event结构体:

    struct inotify_event {
    int wd;//监听文件描述
    uint32_t mask;//事件类型掩码, 在头文件 linux/inotify.h 中定义了每一位代表的事件。一般是读写类型
    uint32_t cookie;//关联事件的
    uint32_t len;//name的大小
    char name[];//名称,以空格结尾
    };

示例:

    #include <stdio.h>   
    #include <unistd.h>   
    #include <sys/select.h>   
    #include <errno.h>   
    #include <sys/inotify.h>   
    
    static void   _inotify_event_handler(struct inotify_event *event)      //从buf中取出一个事件。  
    {   
            printf("event->mask: 0x%08x\n", event->mask);   
            printf("event->name: %s\n", event->name);   
    }   
    
    int  main(int argc, char **argv)   
    {   
        if (argc != 2) {   
            printf("Usage: %s <file/dir>\n", argv[0]);   
            return -1;   
        }   
    
        unsigned char buf[1024] = {0};   
        struct inotify_event *event = NULL;              

        //初始化
        int fd = inotify_init();
        //监控指定文件的ALL_EVENTS。
        int wd = inotify_add_watch(fd, argv[1], IN_ALL_EVENTS);
    
        for (;;) {   
            fd_set fds;   
            FD_ZERO(&fds);                
            FD_SET(fd, &fds);   
            //监控fd的事件。当有事件发生时，返回值>0
            if (select(fd + 1, &fds, NULL, NULL, NULL) > 0){   
                int len, index = 0;   
                while (((len = read(fd, &buf, sizeof(buf))) < 0) && (errno == EINTR)); //没有读取到事件。循环等待
                while (index < len) 
                {   
                    event = (struct inotify_event *)(buf + index); 
                    //获取事件。                    
                    _inotify_event_handler(event);                                      
                    //移动index指向下一个事件。
                    index += sizeof(struct inotify_event) + event->len;  
                }   
            }   
        }   
        //删除对指定文件的监控。
        inotify_rm_watch(fd, wd);              
        return 0;   
    }