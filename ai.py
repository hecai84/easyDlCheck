'''
Description: 
Author: hecai
Date: 2021-08-17 16:32:13
LastEditTime: 2022-03-08 10:49:54
FilePath: \checkAi\ai.py
'''
import requests
import json
import config
import base64

class Ai:
    def __init__(self) -> None:
        self.token=""
        conf=config.Config()
        self.getToken(conf.baidu_ak,conf.baidu_sk)

    def getToken(self,ak,sk):
        #获取token地址
        authHost = "https://aip.baidubce.com/oauth/2.0/token?"
        getAccessTokenUrl = authHost + "grant_type=client_credentials"+ "&client_id=" + ak+ "&client_secret=" + sk

        r = requests.get(getAccessTokenUrl)

        if r.status_code == 200:
            self.token=r.json()["access_token"]
   
                
       
    def IdentifyBeanFiliter(self,result,threshold):
        for i in range(1,len(result["results"])):
            for j in range(i):
                beforeRe=result["results"][j]
                curRe=result["results"][i]
                if beforeRe["name"]==curRe["name"]:
                    if self.checkCover(beforeRe["location"],curRe["location"],threshold):
                        result["results"][i]["score"]=0

    def checkCover(self,before,after,threshold):
        left=before["left"] if before["left"]>after["left"] else after["left"]
        right=before["left"]+before["width"] if before["left"]+before["width"]<after["left"]+after["width"] else after["left"]+after["width"]
        top=before["top"] if before["top"]>after["top"] else after["top"]
        bottom=before["top"]+before["height"] if before["top"]+before["height"]<after["top"]+after["height"] else after["top"]+after["height"]
        if left<right and top<bottom:
            coverArea=(right-left) * (bottom-top)
            beforeArea=before["width"]*before["width"]
            if coverArea>beforeArea*threshold:
                return True
        return False

    def checkAvailable(self,pixelMatrix,location,threshold):
        count=0
        for x in range(location["left"],location["left"]+location["width"]):
            for y in range(location["top"],location["top"]+location["height"]):
                if pixelMatrix[x,y]==0:                    
                    count+=1
                    pixelMatrix[x,y]=1
        return count > location["width"] * location["height"] * threshold;


    def base64Img(self,path):
        with open(path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode()  # base64编码
            return base64_data

    def Identify(self,filepath,url,threshold):
        if url.find('192.168') != -1:
            with open(filepath, 'rb') as f:
                img = f.read()
            r = requests.post(url, params={'threshold': 0.1},data=img).json()
            print(r)
            return json.dumps(r)
        else:
            param={}
            param["image"]=self.base64Img(filepath)
            if threshold!="":
                param["threshold"]=threshold
            content=json.dumps(param)
            r=requests.post(url+"?access_token=" + self.token, data=content)
            if r.status_code == 200:
                print(r.text)
                return r.text

