# !/usr/bin python3                                 
# encoding    : utf-8 -*-                            
# @author     : Erikten                            
# @software   : PyCharm      
# @file       : Xray_m.py
# @Time       : 2021/8/4 21:25

import threading
import os
import re
import queue
import time
import argparse


class UnionXray(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.__url = url

    def run(self):
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        url = self.__url.get()[0]
        filename = re.findall(r'http[s]{0,1}://(.+)', url)
        cmd = f"xray webscan --basic-crawler {url} --html-output {filename[0]}.html"
        print(f'''[INFO] {nowTime} 正在扫描{url}, 导出文件名为: {filename[0]}.html\n''')
        os.system(cmd)


class Xray_m(object):
    def __init__(self):
        self.file = self.Msg()
        self.urls = []
        self.threads = ''

    def getThreadings(self,urls):
        return len(urls)

    def getUrl(self):
        filename = self.file
        print(filename)
        q = queue.Queue()
        threadings = []
        num = []
        with open(filename,'r') as f:
            self.urls = f.read().split('\n')
        for url in self.urls:
            url = re.findall(r'http[s]{0,1}://.+',url)
            if url == []:
                pass
            else:
                num.append(url)
                q.put(url)
        for i in range(self.getThreadings(num)):
            threadings.append(UnionXray(q))
        for thread in threadings:
            if thread != None:
                thread.start()
            else:
                pass

    def Msg(self):
        print('''
 __    __                                                    
/  |  /  |                                                   
$$ |  $$ |  ______   ______   __    __          _____  ____  
$$  \/$$/  /      \ /      \ /  |  /  |        /     \/    \ 
 $$  $$<  /$$$$$$  |$$$$$$  |$$ |  $$ |        $$$$$$ $$$$  |
  $$$$  \ $$ |  $$/ /    $$ |$$ |  $$ |        $$ | $$ | $$ |
 $$ /$$  |$$ |     /$$$$$$$ |$$ \__$$ |        $$ | $$ | $$ |
$$ |  $$ |$$ |     $$    $$ |$$    $$ | ______ $$ | $$ | $$ |
$$/   $$/ $$/       $$$$$$$/  $$$$$$$ |/      |$$/  $$/  $$/ 
                             /  \__$$ |$$$$$$/               
                             $$    $$/                       
                              $$$$$$/                        
        ''')
        parser = argparse.ArgumentParser(usage='python3 Xray_m.py -f url.txt ')
        parser.add_argument('-f', '--file', help='This is file dir')
        args = parser.parse_args()
        if args.file == None:
            print("未指定参数 !")
            exit()
        else:
            return args.file

def main():
    start_time = time.time() # 脚本开始执行的时间
    user = Xray_m()
    user.getUrl()
    end_time = time.time() # 脚本结束执行的时间
    print("[times] %3ss"%(end_time-start_time,))


if __name__ == "__main__":
    try:
        osPath = os.environ
        if 'xray' not in osPath['PATH']:
            chose = input('[!] 未在系统环境变量中检测到Xray, 是否继续执行 ? (y)') or 'y'
            print(chose)
            if chose == 'y':
                main()
            else:
                exit('感谢使用~')
        else:
            main()
    except:
        print("程序运行出错, 请读readme文档 !")