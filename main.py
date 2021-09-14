import cgyy
import numpy as np

time_priority=[11,10]# time scale (08:00-09:30 pm) (06:30-08:00 pm)
place_priority=[6,8,11,12,1,2,3,4,5,7,9,10,13,14]
proxies = {
    "http":"http://127.0.0.1:8888",
    "https":"https://127.0.0.1:8888",
}

user1 = {
    "ChinessName":"",
    "Phone": "",
    "number":"",
    "passwd":"",
    "wxId":"",
}

status=cgyy.submit(user1,time_priority,place_priority,proxies)
print(status)
