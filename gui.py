'''
Description: 
Author: hecai
Date: 2021-08-07 23:08:32
LastEditTime: 2021-08-24 15:05:47
FilePath: \checkAi\gui.py
'''
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import winreg
import json
from PIL import Image
from PIL import ImageTk
import windnd
import ai
import numpy as np
import config

 

 
class Gui:
    w_box = 480  
    h_box = 480  
    def __init__(self,owner):
        self.owner=owner
        self.ai=ai.Ai()
        self.picPath=""
        self.conf=config.Config()
        
 
    def loadConfig(self):
        self.comboApi['value']=self.conf.apiList
        if len(self.conf.apiList)>0:
            self.comboApi.current(0)
        else:
            self.comboApi.set('')

    def signAiResult(self):
        self.openPic(self.picPath)
        data = json.loads(self.text_Re.get("0.0","end"))
        goods={}
        self.ai.IdentifyBeanFiliter(data,float(self.conf.dedup_th1))
        pixelMatrix=np.ones((960,960))*0
        for bean in data["results"]:
            x1=bean["location"]["left"]/2
            x2=(bean["location"]["left"]+bean["location"]["width"])/2
            y1=bean["location"]["top"]/2
            y2=(bean["location"]["top"]+bean["location"]["height"])/2
            if bean["score"]!=0 and self.ai.checkAvailable(pixelMatrix,bean["location"],float(self.conf.dedup_th2)):
                name=bean["name"]
                if name in goods:
                    goods[name]=goods[name]+1
                else:
                    goods[name]=1
                self.canvas.create_rectangle(x1,y1,x2,y2,outline='blue')
            else:
                self.canvas.create_rectangle(x1,y1,x2,y2,outline='red')
            
        
        self.text_count.delete("0.0","end")
        for v,k in goods.items():
            name=v
            if v in self.conf.goods:
                name=self.conf.goods[v]
            self.text_count.insert("end",name+":"+str(k)+"\n")

    def resize(self,w, h, w_box, h_box, pil_image):  
        f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
        f2 = 1.0*h_box/h  
        factor = min([f1, f2])  
        #print(f1, f2, factor) # test  
        # use best down-sizing filter  
        width = int(w*factor)  
        height = int(h*factor)  
        return pil_image.resize((width, height), Image.ANTIALIAS)  

    def get_desktop(self):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]

    def openPic(self,file_path):
        global image
        global im
        print(file_path)
        image = Image.open(file_path)  
        w,h=image.size
        image = self.resize(w, h, self.w_box, self.h_box, image) 
        im = ImageTk.PhotoImage(image)  
        self.canvas.create_image(0,0,anchor='nw',image = im)  
        self.picPath=file_path

    def openPicDialog(self):    
        path=self.get_desktop()
        file_path = filedialog.askopenfilename(title='请选择一个图片', 
            initialdir=path, 
            filetypes=[("图片", ".jpg .png"), ('All Files', ' *')], 
            defaultextension='.jpg')
        
        if len(file_path)>0:
            self.openPic(file_path)

    def Identify(self):
        if self.picPath!="":
            result=self.ai.Identify(self.picPath,self.comboApi.get(),self.text_th.get())
            self.text_Re.delete("0.0","end")            
            self.text_Re.insert("end",result.replace("{\"loca","\n{\"loca"))
            self.signAiResult()

    def dragged_files(self,files):
        try:
            if len(files)==1:
                filename=files[0].decode('gbk')
                if filename.endswith(".jpg"):
                    self.openPic(filename)
        except:
            print("dragged error")
        
    def create(self):
        
        self.root = tk.Tk()

        self.root.geometry('880x520')  # 这里的乘是小x
 
        labelPort = tk.Label(self.root,text = "API:")
        labelPort.grid(column=0, row=0,padx=5, pady=5)

        self.comboApi = ttk.Combobox(self.root,state="readonly",width=60)
        self.comboApi.grid(column=1, row=0, padx=5)

        self.bt_OpenPic = tk.Button(self.root, text="打开图片", command=self.openPicDialog)
        self.bt_OpenPic.grid(column=2, row=0)
        self.bt_Identify = tk.Button(self.root, text="识别", command=self.Identify)
        self.bt_Identify.grid(column=3, row=0)
        self.text_th = tk.Entry(self.root,width=6)
        self.text_th.grid(column=4, row=0)
        self.text_th.insert(0,self.conf.threshold)
        self.bt_Sign = tk.Button(self.root, text="标记", command=self.signAiResult)
        self.bt_Sign.grid(column=5, row=0)
        

        self.canvas = tk.Canvas(self.root, bg='white', height=480, width=500)
        self.canvas.grid(column=0, row=2,columnspan=2,rowspan=2)
        
        self.text_Re = tk.Text(self.root,width=50, height=27)
        self.text_Re.grid(column=2, row=2,columnspan=4)
        
        self.text_count = tk.Text(self.root,width=50, height=10)
        self.text_count.grid(column=2, row=3,columnspan=4)

        self.loadConfig()
        
        #self.root.after(10, self.loop)
        windnd.hook_dropfiles(self.root , func=self.dragged_files)
        self.root.mainloop()
        
 
