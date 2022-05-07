'''
Description: 
Author: hecai
Date: 2021-08-07 12:50:27
LastEditTime: 2022-05-07 10:43:26
FilePath: \checkAi\main.py
'''
from time import sleep
import gui
from multiprocessing import Process,Queue
import threading
import config
import os
#pip freeze > requirements.txt
#pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

#将工作目录设置成当前脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MainProc:
    def __init__(self):
        self.q=Queue()
        self.ui=gui.Gui(self)
        self.createView()
    
    def createView(self):
        mainThread = threading.Thread(target = self.service,args =())   
        mainThread.start()
        self.ui.create()


    # def loadConfig(self):
    #     msg=gui.HandleMsg('SetConfig',{})
    #     msg.args['list']=self.conf.apiList
    #     self.SendUiMsg(msg)


    def service(self):
        pass

if __name__ == "__main__":
    app=MainProc();


