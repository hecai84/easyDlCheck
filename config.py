'''
Description: 
Author: hecai
Date: 2021-08-17 14:58:15
LastEditTime: 2021-09-10 16:26:50
FilePath: \checkAi\config.py
'''
import pandas as pd

class Config:
    def __init__(self) -> None:
        self.apiList=[
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/beverage_whole",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/beverage_whole_2", 
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/obj_detection_test",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/wine_test",     
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/obj_detection",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/obj_detection_test"            
        ]
        self.threshold="0.6"
        #同一产品去重
        self.dedup_th1="0.9"
        #所有产品去重
        self.dedup_th2="0.5"
        self.baidu_ak="EdkfxjTv0pR8IU2q9AdN6Ntg"
        self.baidu_sk="9ohs6PvxnBNMtFkG9jqpTwFTkiBdd42r"
        self.goodsfile="./goods.xlsx"
        self.goods={}

    def LoadGoods(self):
        df = pd.read_excel(self.goodsfile, sheet_name='Sheet1')
        print(df)
        print(df.columns)
        # 5.获取列行标题
        print(df.index)
        for index in df.index:
            self.goods[df.loc[index].values[0]]=df.loc[index].values[1]
