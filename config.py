'''
Description: 
Author: hecai
Date: 2021-08-17 14:58:15
LastEditTime: 2021-08-17 22:51:40
FilePath: \checkAi\config.py
'''
class Config:
    def __init__(self) -> None:
        self.apiList=[
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/beverage_whole",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/beverage_whole_2", 
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/detection/wine_test",           
        ]
        self.threshold="0.6"
        self.baidu_ak="EdkfxjTv0pR8IU2q9AdN6Ntg"
        self.baidu_sk="9ohs6PvxnBNMtFkG9jqpTwFTkiBdd42r"
        self.goods={
            "youyic_mn_6934665087653":"优益C",
            "gonggang_cg_6924686502754":"供港壹号",
        }
        
