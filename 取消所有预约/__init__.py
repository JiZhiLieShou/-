import requests
import random
from time import sleep

def get_seat_id_from_txt(keyword):
    # 打开文件
    with open('../预约座位【带验证码】/seat.txt', 'r') as f:
        # 读取文件内容
        content = f.read()
        # 解析为字典对象
        data_dict = eval(content)

    # 获取指定键对应的列表
    if keyword in data_dict:
        value_list = data_dict[keyword][0]
        print(value_list)
        return value_list
    else:
        print(f"The keyword '{keyword}' does not exist in the dictionary.")


def main():
    libiary_username = input('请输入图书馆用户名：')
    libiary_password = input('请输入图书馆密码：')
    session = requests.Session()
    params = {
        "libid": "ayit",
        "username": libiary_username,
        "password": libiary_password
    }
    headers = {
        'authority': 'zwqd.ayit.edu.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://zwqd.ayit.edu.cn/',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'
    }
    response = session.get("https://zwqd.ayit.edu.cn/interface/ayit/user_login.asp", params=params, headers=headers)
    userid = str(response.json()['userid'])
    # print(response.text)
    url = "https://zwqd.ayit.edu.cn/Seatresv/GetMyOrder.asp?userid=" + userid + "&number=" + str(round(random.uniform(0, 1), 17))
    payload = {}
    response = session.request("GET", url, headers=headers, data=payload)
    print(response.text)
    i = 0
    for item in response.json()["seatorder"]:
        if item.get('cancancel') == 1:
            i = 1
            print("存在未取消座位：" + str(item.get('seatinfo')) + "]")
            url = "https://zwqd.ayit.edu.cn/Seatresv/CancelOrder.asp"
            params = {
                'libid': 'ayit',
                'seatorderid': str(item.get('seatorderid')),
                'userid': userid,
                'number': str(round(random.uniform(0, 1), 17))
            }
            print(params)
            response = session.get(url, headers=headers, params=params)
            print(response.text)
    if i == 0:
        print("没有正在预约的座位")
    input("输入任意字符退出...")


if __name__ == '__main__':
    if input('你真的要取消所有的预约吗？(y/n)').lower() == 'y':
        main()
    else:
        sleep(3)
        pass
