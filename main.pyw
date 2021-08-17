'''
Description: 
Author: hecai
Date: 2021-08-07 12:50:27
LastEditTime: 2021-08-17 21:58:19
FilePath: \checkAi\main.pyw
'''
from time import sleep
import gui
from multiprocessing import Process,Queue
import config
#pip freeze > requirements.txt
#pip install -r requirements.txt

class MainProc:
    def __init__(self):
        self.q=Queue()
        self.conf=config.Config()
        self.createView()
    
    def createView(self):
        uiProc=Process(target=self.service,args=()) #创建服务子进程
        uiProc.start()
        gui.Gui(self)
        uiProc.terminate()

    def SendUiMsg(self,msg:gui.HandleMsg):
        self.q.put(msg)

    def loadConfig(self):
        msg=gui.HandleMsg('SetConfig',{})
        msg.args['list']=self.conf.apiList
        self.SendUiMsg(msg)

    def insertRecMsg(self,recArr):
        msg=gui.HandleMsg('insertRecMsg',{})
        info=""
        for i in recArr:
            info+='%02x ' % (i)
        msg.args['info']=info
        self.SendUiMsg(msg)

    def alarmMsg(self):
        msg=gui.HandleMsg('alarm',{})
        self.SendUiMsg(msg)

    def UartCb(self,recArr):
        cmd=recArr[2]
        data=recArr[3:recArr[1]-1]
        print("cmd:",cmd)
        print("data:",data)
        self.insertRecMsg(recArr)
        if cmd==0xaa:
            self.alarmMsg()

    def service(self):
        self.loadConfig()
        # msg=gui.HandleMsg()
        # x=1
        # while x<10000000:
        #     x=x+1
        #     msg.name=str(x)
        #     print(msg.name)
        #     self.SendUiMsg(msg)
        #     sleep(1)

if __name__ == "__main__":
    app=MainProc();


