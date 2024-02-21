import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


def get_cookie():
    driver = Chrome(service=Service("./chromedriver.exe"))
    driver.get('https://webvpn.ayit.edu.cn/')
    driver.maximize_window()
    driver.find_element(By.XPATH, '//*[@id="loginNew"]/div[2]/div[2]/div[2]/div[2]/button').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="credentials"]/ul/li[2]/input').send_keys('20136610115')
    driver.find_element(By.XPATH, '//*[@id="credentials"]/ul/li[3]/input').send_keys('20021112Aa~')
    driver.find_element(By.XPATH, '//*[@id="credentials"]/ul/li[5]/input[3]').click()
    diccookie = driver.get_cookie("my_client_ticket")
    cookie = str(diccookie["value"])
    driver.quit()
    print(cookie)
    time.sleep(1)
    return cookie


if __name__ == '__main__':
    cookie = get_cookie()
    session = requests.session()
    session.cookies.update({'my_client_ticket': cookie})
    print(session.get("https://zwqd.ayit.edu.cn/GetLibinfo/?libid=ayit&subsystemid=").text)
