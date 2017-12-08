import requests
from Crawler.parser import *
from ProxyPool.Manager.ProxyManager import ProxyManager

def get_proxy():
    try:
        proxy = requests.get("http://127.0.0.1:5010/get/").content
        return ProxyManager.get()
    except:
        return None

def delete_proxy(proxy):
    try:
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    except:
        return


def get_web_content(url = 'https://www.amazon.com/dp/B003AI2VGA'):

    headers = {
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }

    retry_count = 5
    proxy = get_proxy()
    while retry_count > 0:
        try:
            response = requests.get(url, headers = headers, proxies={"http": "http://{}".format(proxy)})
            return parser(response.content)
        except Exception:
            retry_count -= 1
    delete_proxy(proxy)
    return None