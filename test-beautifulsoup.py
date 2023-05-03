import requests
from bs4 import BeautifulSoup as bs
from lxml.html import fromstring
from openpyxl import Workbook
from itertools import cycle
import time
from random import choice
from fake_useragent import UserAgent
import sys
from requests.exceptions import ProxyError, SSLError, ConnectTimeout


def get_proxies():
    url = 'http://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.content)
    proxies = set()
    for i in parser.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')[:50]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                             i.xpath('.//td[2]/text()')[0]])  # /text빼고도 되는지 확인
            proxies.add(proxy)
    return proxies


headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    'User-Agent': str(UserAgent().chrome)
}
print(headers)

URL = 'https://www.stepstone.de/jobs--IT-system-engineer-m-w-d-Bundesweit-TOI-TOI-DIXI-Group-GmbH--9134347-inline.html?rltr=1_1_25_seorl_m_0_0_0_0_0_0'
res = requests.get(URL)
print(res)

# proxy_server_list = []
# proxy_server_list = list(get_proxies())
# print(proxy_server_list)
# while True:
#     time.sleep(3)
#     proxy = choice(proxy_server_list)
#     print(proxy)
#     proxies = {'http': proxy, 'https': proxy}
#     try:
#         resp = requests.get(URL, headers=headers,
#                             proxies=proxies, verify=False, timeout=3)
#         time.sleep(5)
#         print('try..')
#         print(resp.status_code)
#         if (resp.status_code == "403"):
#             print(resp)
#         elif str(resp.status_code) == "200":
#             print("=====================SUCCESS!==============================")
#             parser = fromstring(resp.content)
#             soup = bs(resp.text, "html.parser")
#             elements = soup.select_one('body>div')
#             print(elements)
#             print("============================================================")
#             break
#     except (ProxyError, SSLError, ConnectTimeout) as e:
#         print('except..')
#         proxy_server_list.remove(proxy)

# print("DONE...")
