import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome("chromedriver")
driver = webdriver.Chrome(
    'D:\seeds\SWEVER\CRAWLING-test\chromedriver_win32\chromedriver.exe')
URL = "https://www.burgerkingevent.com/"

resp = requests.get(URL)
time.sleep(5)
btn = driver.find_element(By.XPATH, '//*[@id="main_btn_touch"]')
btn.click()
time.sleep(3)
inputword = driver.find_element(
    By.XPATH, '//*[@id="input_typing"]')
inputword.send_keys("콰트로 맥시멈 미트 포커스드 어메이징 얼티밋 그릴드 패티 오브 더 비기스트 포 슈퍼 미트 프릭")
inputword.send_keys(Keys.RETURN)
