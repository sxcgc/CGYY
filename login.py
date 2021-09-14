import os
import re
import requests
import json
import datetime
from lxml import etree

def login(number,passwd,proxies):
    login_url = "https://passport.ustc.edu.cn/login?service=https://cgyy.ustc.edu.cn/validateLogin.html"
    login_url2 = "https://passport.ustc.edu.cn/login"

    form = {
        "model":"uplogin.jsp",
        "CAS_LT":"",
        "service":"https://cgyy.ustc.edu.cn/validateLogin.html",
        "warn":"",
        "showCode":"",
        "username":number,
        "password":passwd,
        "bottom":"",
    }

    cookies={
        "uc":number
    }
    s = requests.Session()
    s.headers["User-Agent"]="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat"
    s.headers["cookie"] = number

    d = s.get(login_url,proxies = proxies,verify = False)
    get_cookies= requests.utils.dict_from_cookiejar(d.cookies) 
    for k in get_cookies:
        cookies[k] = get_cookies[k]
    s.headers["cookie"]="; ".join([str(x)+"="+str(y) for x,y in cookies.items()])

    start = d.text.find("input type=\"hidden\" id=\"CAS_LT\" name=\"CAS_LT\" value=")
    form["CAS_LT"]=d.text[start+53:start+88]

    d = s.post(login_url2,proxies = proxies,verify = False,data = form)
    url_redirect = d.history[0].headers["Location"]
    id_temp = url_redirect.find("ticket=")
    id1 = url_redirect[id_temp+7:id_temp+42]
    return id1
