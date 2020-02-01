import subprocess
import time
import asyncio

def cmd1():
    # 启动桌面上的config.xlaunch应用,直接使用subprocess,没有使用asyncio
    p = subprocess.Popen("start C:/Users/panjunlong/Desktop/config.xlaunch", stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE,shell=True, close_fds=True)
    print("启动桌面上的config.xlaunch应用")

async def cmd2():
    ###asyncio.create_subprocess_shell必须重复,只想重复p.communicate是不行的,还是会阻塞
    # p = await asyncio.create_subprocess_shell("ubuntu1804", stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True, close_fds=True)
    #使用asyncio.gather来同步运行
    await asyncio.gather(commun_cmd(cmd2_str1()),commun_cmd(cmd2_str2()),commun_cmd(cmd2_str3()))

async def commun_cmd(cmd_str):
    #注意 asyncio.subprocess.PIPE ,和subprocess.PIPE不一样
    p = await asyncio.create_subprocess_shell("ubuntu1804", stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True, close_fds=True)
    task=asyncio.create_task(p.communicate(bytes(cmd_str,encoding='utf-8')))
    (out,err)=await task
    print("out:"+str(out,encoding="utf-8")+"**\r\n")
    print("err:"+str(err,encoding="utf-8")+"**\r\n")

def cmd2_str1():#赋权执行compiz
    print("赋权执行compiz")
    return "echo wode110 | sudo -S compiz"

def cmd2_str2():#启动软件
    time.sleep(3)
    print("启动软件")
    return "/mnt/e/kaios软件/kaiosrt-v2.5-ubuntu-20190925163557-n378/kaiosrt/kaiosrt"
    
def cmd2_str3():#挂载远程映射盘到pjl_tmp下
    time.sleep(3)
    print("挂载远程映射盘到pjl_tmp下")
    return "echo wode110 | sudo -S mount -t drvfs Z: /pjl_tmp"

def cmd3():
    # 执行adb root 和adb remount
    p = subprocess.Popen("adb root", stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE,shell=True, close_fds=True)
    print("adb root")
    p = subprocess.Popen("adb remount", stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE,shell=True, close_fds=True)
    print("adb remount")

cmd1()
cmd3()
time.sleep(2)
asyncio.run(cmd2())


