# 报错集锦：
#   [1001]：预约速度过快
#   invid：cookies错误，需要再抓
#   校验码错误：预约实时时间死板了（time变量）
# 注意事项：
#   代码运行时不要开vpn(连美国地址怎么去访问图鉴识别站点)
import requests
import base64
import json
import random
import pygame
from time import sleep
from datetime import datetime


def get_seatid_from_txt(seat_number):
    # 打开文件
    with open('../预约座位【带验证码】/seat.txt', 'r') as f:
        # 读取文件内容
        content = f.read()
        # 解析为字典对象
        data_dict = eval(content)

    # 获取指定键对应的列表
    if seat_number in data_dict:
        value_list = data_dict[seat_number][0]
        # print(value_list)
        return value_list
    else:
        print(f"座位号 '{seat_number}' 不在seat.txt字典里")


def get_userid_from_txt(session, libiary_username, libiary_password):  # 获取user_id（取代 user_id = "181919"  # 使用者id 宝顺才：185469 李国兴：181919）
    userid = str(session.get("https://zwqd.ayit.edu.cn/interface/ayit/user_login.asp", params={
        "libid": "ayit",
        "username": libiary_username,
        "password": libiary_password
    }, headers={
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
    }).json()['userid'])  # 获取userid
    return userid


def base64_api(tujianocr_uname, tujianocr_pwd, base64_data, typeid):
    response = requests.get("http://api.ttshitu.com/queryAccountInfo.json?username=" + tujianocr_uname + "&password=" + tujianocr_pwd).json()['data']['balance']
    print("你的余额剩余：" + str(response) + "元")
    data = {"username": tujianocr_uname,
            "password": tujianocr_pwd,
            "typeid": typeid,
            "image": base64_data}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        # ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]


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


if __name__ == "__main__":
    print("")
    # 打开文件->录入预约人信息
    with open('information.txt', 'r', encoding='utf-8') as file:
        # 读取文件的所有行
        lines = file.readlines()
        # 读取并赋值给变量
        second = lines[2].split('：', 1)[-1].strip()
        # print("停顿时间:", second)
        seat_number = lines[3].split('：', 1)[-1].strip()
        # print("座位号:", seat_number)
        libiary_username = lines[4].split('：', 1)[-1].strip()
        # print("图书馆用户名:", libiary_username)
        libiary_password = lines[5].split('：', 1)[-1].strip()
        # print("图书馆密码:", libiary_password)
        start_time = lines[6].split('：', 1)[-1].strip()
        # print("预约开始时间:", start_time)
        end_time = lines[7].split('：', 1)[-1].strip()
        # print("预约结束时间:", end_time)
        if_chock_time = lines[8].split('：', 1)[-1].strip()
        # print("是否需要阻塞时间", if_chock_time)
        chock_time = lines[9].split('：', 1)[-1].strip()
        # print("阻塞时间:", chock_time)
    # 转换信息文本
    session = requests.Session()  # 创建一个会话对象
    userid = get_userid_from_txt(session=session, libiary_username=libiary_username, libiary_password=libiary_password)
    seatid = str(get_seatid_from_txt(seat_number))  # 将座位号转换为编码形式
    number = str(round(random.uniform(0, 1), 17))  # 0和1之间，精度为17位小数#"0.27832147488845793"  # 一般不用改，对加密后的数值影响不大【小数点后是十七位】

    headers = {
        'authority': 'zwqd.ayit.edu.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
    print("录入信息完成，准备开始预约...")
    # 加入时间阻塞函数
    if int(if_chock_time) == 1:
        while 1:
            print(datetime.now())
            sleep(0.00001)
            if str(datetime.now().strftime("%H:%M:%S")) == chock_time:  # 只有时分秒同时相等时才运行
                print(datetime.now())
                print("开始预约")
                break

    while True:
        try:
            print("1.发送GET请求获取【验证码】BMP文件内容->将BMP文件内容转换为Base64编码->解码为utf-8保存在base64_data变量中")
            bmp_data = session.get(
                ("https://zwqd.ayit.edu.cn/Seatresv/getcode.asp?checkcodename=seatresv_code&libid=ayit"
                 + "&seatid=" + seatid
                 + "&userid=" + userid
                 + "&number=" + number
                 + "/image.bmp"), headers=headers, timeout=28).content
            base64_data = base64.b64encode(bmp_data).decode('utf-8')
            # print("2.验证码识别")
            # code = str(base64_api(tujianocr_uname=tujianocr_uname, tujianocr_pwd=tujianocr_pwd, base64_data=base64_data, typeid=3))  # 验证码
            # print("验证码：" + str(code))
            print("3.加密验证码生成网址")
            before_encrypt = ("libid=ayit"
                              + "&seatid=" + seatid
                              + "&userid=" + userid
                              + "&validtime=" + start_time
                              + "&invalidtime=" + end_time
                              + "&number=" + number
                              + "&time=" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                              + "&code=")
            print("加密前：" + str(before_encrypt))
            After_encrypt = encrypte(before_encrypt)  # 加密信息
            print("加密后：" + str(After_encrypt))
            print("4.请求网址【带着加密的验证码】")
            response = session.get("https://zwqd.ayit.edu.cn/Seatresv/SeatOrder.asp?" + After_encrypt, headers=headers)

            print(str(response.json()))
            if "预约成功" in response.json()['ErrNote']:
                pygame.mixer.init()  # 初始化pygame.mixer模块
                sound = pygame.mixer.Sound('music.mp3')
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000))
                input("输入任意字符退出程序...")
                break
            elif ("您同时只能预约一个座位" in response.json()['ErrNote']) or ("该座位已被他人预约" in response.json()['ErrNote']) or "预约失败！提前预约时间为前一天20:00:00之后" in response.json()['ErrNote']:
                input("输入任意字符退出程序...")
                break
        except:
            print("报错了，等待停顿时间之后重新执行")
            print("当前时间:", datetime.now())
            for i in range(int(second), 0, -1):
                sleep(1)
                print(i)
            print("当前时间：", datetime.now())
            print("重新开始预约...")
