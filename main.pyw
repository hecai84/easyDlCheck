'''
Description: 
Author: hecai
Date: 2021-08-07 12:50:27
LastEditTime: 2021-08-19 16:24:58
FilePath: \checkAi\main.pyw
'''
from time import sleep
import gui
from multiprocessing import Process,Queue
import threading
import config
#pip freeze > requirements.txt
#pip install -r requirements.txt

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


