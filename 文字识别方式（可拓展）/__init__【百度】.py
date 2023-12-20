import base64
import urllib
import requests

API_KEY = ""
SECRET_KEY = ""


def main():
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=" + get_access_token()

    # 要求：
    #   base64编码和urlencode后大小不超过10M，最短边至少15px，最长边最大8192px
    payload = (
        #  图片的base64编码（base64编码后进行urlencode）
        'image='
        # 图片完整url，url长度不超过1024字节
        '&url='
        # 优先级：image > url > pdf_file，当image、url字段存在时，pdf_file字段失效 (文件数据base64编码)
        '&pdf_file='
        # 【需要识别的PDF文件的对应页码】当 pdf_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页
        '&pdf_file_num='
        # OFD文件：优先级：image > url > pdf_file > ofd_file，当image、url、pdf_file字段存在时，ofd_file字段失效
        '&ofd_file='
        # 【需要识别的OFD文件的对应页码】当 ofd_file 参数有效时，识别传入页码的对应页面内容，若不传入，则默认识别第 1 页
        '&ofd_file_num='
        # 识别语言类型，默认为CHN_ENG 可选值包括： 
            # - auto_detect：自动检测语言，并识别 
            # - CHN_ENG：中英文混合 
            # - ENG：英文 - JAP：日语 - KOR：韩语 - FRE：法语 - SPA：西班牙语 - POR：葡萄牙语 - GER：德语 - ITA：意大利语 - RUS：俄语 - DAN：丹麦语 - DUT：荷兰语 -  MAL：马来语 - SWE：瑞典语 - IND：印尼语 - POL：波兰语 - ROM：罗马尼亚语 - TUR：土耳其语 - GRE：希腊语 - HUN：匈牙利语 - THA：泰语 - VIE：越南语 - ARA：阿拉伯语 - HIN：印地语 
        '&language_type=auto_detect'
        # 表示识别语言类型为「中英文（CHN_ENG）」的情况下，英文的单字符结果是按照单词（word）维度输出还是字母（letter）维度输出。(当 recognize_granularity=small 时生效)
        '&eng_granularity=word'
        # 是否定位单字符位置
            # big：不定位单字符位置，默认值；
            # small：定位单字符位置
        '&recognize_granularity=big'
        # 是否检测图像朝向，默认不检测，即：false。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括: - true：检测朝向； - false：不检测朝向
        '&detect_direction=true'
        # 是否返回文字外接多边形顶点位置，不支持单字位置。默认为false
        '&vertexes_location=true'
        # 是否输出段落信息
        '&paragraph=true'
        # 是否返回识别结果中每一行的置信度
        '&probability=true')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
