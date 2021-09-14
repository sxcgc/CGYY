import os
import re
import requests
import json
import datetime
import login
import numpy as np
requests.packages.urllib3.disable_warnings()

{
	"gymnasiumId": "1",
	"dateStr": "2021-09-13",
	"timeQuantumId": 3
}

def get_vaild(proxies):
    home_message_url = "https://cgyy.ustc.edu.cn/api/app/config/getConfig/home_message"
    get_config_url = "https://cgyy.ustc.edu.cn/api/app/appointment/time/quantum/get/1"
    update_url = "https://cgyy.ustc.edu.cn/api/app/sport/place/getAppointmentInfo"

    order_json = {}

    s = requests.Session()
    s.headers["content-type"] = "application/json"
    s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
    


def submit(userdef,time_priority,place_priority,proxies):
    order_json = {}

    authority={
        "wxId":userdef["wxId"],
        "ticket":"",
    }

    submit_json = {
    	"gymnasiumId": 1,
    	"sportPlaceId": 4,
    	"timeQuantum": "08:00-09:30",
    	"timeQuantumId": 3,
    	"appointmentUserName": userdef["ChinessName"],
    	"appointmentPeopleNumber": 1,
    	"appointmentDay": "2021-09-15",
    	"phone": userdef["Phone"]
    }
    now_p_3 = (datetime.datetime.now()+datetime.timedelta(days=2)).strftime("%Y-%m-%d")# T+3
    print("appointmentDay:\t",now_p_3)
    #proxies = {}
    s = requests.Session()
    s.headers["authority"]="cgyy.ustc.edu.cn"
    s.headers["scheme"]="https"
    s.headers["content-type"] = "application/json"
    s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
    #s.headers["referer"]="https://servicewechat.com/wxf0984b113dd8ac45/15/page-frame.html"

    login_url = "https://cgyy.ustc.edu.cn/api/user/login"
    home_message_url = "https://cgyy.ustc.edu.cn/api/app/config/getConfig/home_message"
    get_config_url = "https://cgyy.ustc.edu.cn/api/app/appointment/time/quantum/get/1"
    update_url = "https://cgyy.ustc.edu.cn/api/app/sport/place/getAppointmentInfo"
    sub_url = "https://cgyy.ustc.edu.cn/api/app/appointment/record/submit"

# 获取时间段等配置信息
    d = s.post(get_config_url,proxies=proxies,verify = False, data = json.dumps(order_json))
    config_h = json.loads(d.text)
# 获取空闲场地
    timestr = ["","","","08:00-09:30","09:30-11:00","11:00-12:30","12:30-14:00","14:00-15:30",
    "15:30-17:00","17:00-18:30","18:30-20:00","20:00-21:30"]
    for ii,t in enumerate(time_priority):
        submit_flag = False
        order_json["gymnasiumId"]= "1"
        order_json["dateStr"]= now_p_3
        order_json["timeQuantumId"] = t
        d = s.post(update_url,proxies=proxies,verify=False,data = json.dumps(order_json))
        sportPlace = json.loads(d.text)["data"]
        placeID = np.zeros((15))
        for sp in sportPlace:
            if sp["useType"] == 0:
                placeID[sp["id"]] = 1
        for p in place_priority:
            if placeID[p] == 1:

                submit_json["sportPlaceId"] = p
                submit_json["timeQuantumId"] = t
                submit_json["timeQuantum"] = timestr[t]
                submit_json["appointmentDay"]= now_p_3
                submit_flag = True
                break
        if submit_flag == True:
        # 获取校园统一认证身份牌
            authority["ticket"]=login.login(userdef["number"],userdef["passwd"],proxies)
        # 去cgyy.ustc.edu.cn 认证并获取 token 
            d = s.post(login_url,proxies=proxies,verify = False, data = json.dumps(authority))
            token = json.loads(d.text)["data"]["token"]       
        # 交钥匙和订单，进行预约
            s.headers["token"] = token
            d = s.post(sub_url,proxies=proxies,verify = False, data = json.dumps(submit_json))
            msg = json.loads(d.text)
            status={}
            status["msg"]=msg["msg"]
            status["code"] = msg["data"]["code"]
            return status
    return False
            