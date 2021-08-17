'''
Description: 
Author: hecai
Date: 2021-08-07 12:50:27
LastEditTime: 2021-08-17 22:26:57
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
        self.createView()
    
    def createView(self):
        uiProc=Process(target=self.service,args=()) #创建服务子进程
        uiProc.start()
        gui.Gui(self)
        uiProc.terminate()

    def SendUiMsg(self,msg:gui.HandleMsg):
        self.q.put(msg)

    # def loadConfig(self):
    #     msg=gui.HandleMsg('SetConfig',{})
    #     msg.args['list']=self.conf.apiList
    #     self.SendUiMsg(msg)


    def service(self):
        pass
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


