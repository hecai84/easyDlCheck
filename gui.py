'''
Description: 
Author: hecai
Date: 2021-08-07 23:08:32
LastEditTime: 2021-08-17 21:51:15
FilePath: \checkAi\gui.py
'''
import tkinter as tk
from tkinter import image_names, messagebox, ttk, filedialog
import winreg
import json
from PIL import Image
from PIL import ImageTk
import ai
import numpy as np

#from mttkinter import mtTkinter as tk
 
class HandleMsg:
    def __init__(self,name="",args={}):
        self.name = name     # 名称
        self.args = args     # 参数 
 
class Gui:
    w_box = 480  
    h_box = 480  
    def __init__(self,owner):
        self.owner=owner
        self.ai=ai.Ai()
        self.picPath=""
        self.create()
 

    def loop(self):
        #读出队列中的信息 
        if(not self.owner.q.empty()): 
            msg=self.owner.q.get() 
            if(msg.name=="SetConfig"):                
                self.comboApi['value']=msg.args['list']
                if len(msg.args['list'])>0:
                    self.comboApi.current(0)
                else:
                    self.comboApi.set('')
            elif msg.name=="insertRecMsg":
                self.text_Rec.insert('end', msg.args['info']+'\n')
            elif msg.name=="alarm":
                self.canvas.create_oval(30, 30, 130, 130, fill='red')
 
        self.root.after(100,self.loop)
 
    def signAiResult(self):
        data = json.loads(self.text_Re.get("0.0","end"))
        goods={}
        self.ai.IdentifyBeanFiliter(data)
        pixelMatrix=np.ones((960,960))*0
        for bean in data["results"]:
            x1=bean["location"]["left"]/2
            x2=(bean["location"]["left"]+bean["location"]["width"])/2
            y1=bean["location"]["top"]/2
            y2=(bean["location"]["top"]+bean["location"]["height"])/2
            if self.ai.checkAvailable(pixelMatrix,bean["location"],0.5):
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
            self.text_count.insert("end",v+":"+str(k)+"\n")

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

    def openPic(self):    
        global image
        global im
        path=self.get_desktop()
        file_path = filedialog.askopenfilename(title='请选择一个图片', initialdir=path, filetypes=[(
    "图片", ".jpg .png"), ('All Files', ' *')], defaultextension='.jpg')
        
        if len(file_path)>0:
            print(file_path)
            image = Image.open(file_path)  
            w,h=image.size
            image = self.resize(w, h, self.w_box, self.h_box, image) 
            im = ImageTk.PhotoImage(image)  
            self.canvas.create_image(0,0,anchor='nw',image = im)  
            self.picPath=file_path

    def Identify(self):
        if self.picPath!="":
            result=self.ai.Identify(self.picPath,self.comboApi.get(),self.text_th.get())
            self.text_Re.delete("0.0","end")            
            self.text_Re.insert("end",result.replace("{\"loca","\n{\"loca"))
            self.signAiResult()
    def create(self):
        
        self.root = tk.Tk()

        self.root.geometry('880x520')  # 这里的乘是小x
 
        labelPort = tk.Label(self.root,text = "API:")
        labelPort.grid(column=0, row=0,padx=5, pady=5)

        self.comboApi = ttk.Combobox(self.root,state="readonly",width=60)
        self.comboApi.grid(column=1, row=0, padx=5)

        self.bt_OpenPic = tk.Button(self.root, text="打开图片", command=self.openPic)
        self.bt_OpenPic.grid(column=2, row=0)
        self.bt_Identify = tk.Button(self.root, text="识别", command=self.Identify)
        self.bt_Identify.grid(column=3, row=0)
        self.text_th = tk.Entry(self.root,width=6)
        self.text_th.grid(column=4, row=0)
        self.bt_Sign = tk.Button(self.root, text="标记", command=self.signAiResult)
        self.bt_Sign.grid(column=5, row=0)
        

        self.canvas = tk.Canvas(self.root, bg='white', height=480, width=500)
        self.canvas.grid(column=0, row=2,columnspan=2,rowspan=2)
        
        self.text_Re = tk.Text(self.root,width=50, height=27)
        self.text_Re.grid(column=2, row=2,columnspan=4)
        
        self.text_count = tk.Text(self.root,width=50, height=10)
        self.text_count.grid(column=2, row=3,columnspan=4)

        self.root.after(10, self.loop)
        self.root.mainloop()
 
