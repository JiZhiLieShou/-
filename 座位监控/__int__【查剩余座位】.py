import requests
import random
import os
from datetime import datetime
from time import sleep


def get_free_seat(userid, mapid, start_time, end_time):
    headers = {
        'authority': "zwqd.ayit.edu.cn",
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        "Cache-Control": "no-cache",
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
    session = requests.Session()
    response = session.get('https://zwqd.ayit.edu.cn/Seatresv/GetTableList.asp?', headers=headers, params={'libid': 'ayit',
                                                                                                           'userid': userid,
                                                                                                           'mapid': mapid,
                                                                                                           'starttime': start_time,
                                                                                                           'endtime': end_time,
                                                                                                           'number': '0.9311735784410118'})

    # print("所有的桌子", response.json()['seattables'])
    for item in response.json()['seattables']:
        if item['isbusy'] == 'false':
            # print("\t空闲桌子号：", item['seattableid'])
            response = session.get('https://zwqd.ayit.edu.cn/Seatresv/GetTableInfo.asp', headers=headers, params={'tableid': item['seattableid'],
                                                                                                                  'number': '0.21017312650888753',
                                                                                                                  'mapid': mapid,
                                                                                                                  'starttime': start_time,
                                                                                                                  'endtime': end_time, })
            # print(response.json()['seats'])
            for item2 in response.json()['seats']:
                if item2['state'] == '空闲':
                    print(response.json()['location'])
                    print('', 'seatnum:' + item2['seatnum'].replace("\n", ""), 'seatid:' + item2['seatid'])
                else:
                    pass


def all_free_seat(userid, start_time, end_time):
    headers = {
        'authority': "zwqd.ayit.edu.cn",
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        "Cache-Control": "no-cache",
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
    while True:
        try:
            print('全体座位开始显示时间:', datetime.now())
            session = requests.Session()
            response = session.get("https://zwqd.ayit.edu.cn/seatresv/Getseatcount.asp", headers=headers,
                                   params={'libid': 'ayit',
                                           'userid': userid,
                                           'starttime': start_time,
                                           'endtime': end_time,
                                           'number': str(round(random.uniform(0, 1), 17))})
            for item in response.json()['maparea']:
                print(item['name'])
            print('全体座位显示完毕时间:', datetime.now())
            print("----------------------------------------------------------")
            get_free_seat(userid=userid, mapid='830', start_time=start_time, end_time=end_time)
            print('830一楼座位输出完毕时间:', datetime.now())
            get_free_seat(userid=userid, mapid='834', start_time=start_time, end_time=end_time)
            print('834五楼座位输出完毕时间:', datetime.now())
            session.close()
            sleep(1)
            # 清屏代码
            os.system('cls')
        except:
            pass


# start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
# end_time = datetime.now().strftime("%Y-%m-%d ") + '22:30'
start_time = '2023-10-20 07:00'
end_time = '2023-10-20 22:30'
all_free_seat('200000', start_time, end_time)
