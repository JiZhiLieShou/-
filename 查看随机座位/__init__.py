import requests
import random
from datetime import datetime

def encrypte(e):
    t = ["", "g", "h", "i"]
    i = "wx3cba883abac619bb"
    a = ""
    n = 0
    for s in range(len(e)):
        r = ord(e[s]) + 2
        if n >= len(i):
            n = 0
        r += ord(i[n])
        # o = hex(r)[2:]
        o = format(r, 'x')
        if len(o) < 4:
            h = t[4 - len(o)]
            o = h + o
        a += o.lower()
        n += 1
    return a


headers = {
    'authority': "zwqd.ayit.edu.cn",
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'accept': '*/*',
    'dnt': '1',
    'referer': 'https://zwqd.ayit.edu.cn/',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'
}
mapid = input("输入座位")  # 830 一楼 834 五楼
session = requests.Session()
userid = '20000'
params = encrypte("libid=ayit"
                  "&userid=" + userid +
                  "&mapid=" + mapid +
                  "&starttime=" + datetime.now().strftime("%Y-%m-%d %H:%M") +
                  "&endtime=" + datetime.now().strftime("%Y-%m-%d ") + '22:30' +
                  "&number=" + str(round(random.uniform(0, 1), 17)) +
                  "&time=" + datetime.now().strftime("%Y-%m-%d %H:%M")
                  )
url = "https://zwqd.ayit.edu.cn/Seatresv/RandomSeat.asp"
print(params)
response = session.get(url, headers=headers, params=params)
print(response.json())
