# -*- coding: utf-8 -*-
import datetime
import json
import math
import os
import random
import requests
import sys
import time


class WeiboSpider(object):
    def __init__(self, user_id: str):
        self.user_id: str = user_id
        self.user_info: dict = {}
        self.weibo_count: int = 0
        self.page_count: int = 0
        self.weibo_container_id: str = ''


    def get_data(self,url:str):
        data = requests.get(url=url).text
        return data
    def get_container_id(self, info):
        data = self.get_data(url)
        content = json.loads(data).get('data')
        for tab in content.get('tabsInfo').get('tabs'):
            if tab.get('tab_type') == 'weibo':
                self.weibo_container_id = tab.get('containerid')

    def get_weibo_and_page_count(self):
        weibo_count = self.user['statuses_count']
        self.page_count = int(math.ceil(weibo_count / 10.0))

    def get_user_info(self):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + self.user_id
        data = self.get_data(url)
        user_info = json.loads(data).get('data').get('userInfo')
        self.user_info = {'screen_name': user_info.get('screen_name'),
                          'profile_url': user_info.get('profile_url'),
                          'statuses_count': user_info.get('statuses_count'),
                          'verified_reason': user_info.get('verified_reason'),
                          'description': user_info.get('description'),
                          'follow_count': user_info.get('follow_count'),
                          'followers_count_str': user_info.get('followers_count_str')}
        self.get_page_count()
        self.get_container_id()




    # def get_weibo:


    def get_picture_info(self):
        weibo_url_prefix = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + self.user_id + '&containerid=' + self.weibo_container_id + '&page='
        for i in range(0, self.page_count):
            weibo_url = weibo_url_prefix + str(i)
            try:
                data = self.get_data(weibo_url)
                content = json.loads(data).get('data')
                cards = content.get('cards')
                cards = content.get('cards')
                if len(cards) > 0:
                    for card in range(len(cards)):
                        print("-----正在爬取第" + str(page_num) + "页，第" + str(card) + "条微博------")
                        card_type = cards[card].get('card_type')
                        if card_type == 9:
                            try:
                                mblog = cards[card].get('mblog')
                                scheme = cards[card].get('scheme')
                                created_at = mblog.get('created_at')
                                text = mblog.get('text')
                                reposts_count = mblog.get('reposts_count')
                                comments_count = mblog.get('comments_count')
                                attitudes_count = mblog.get('attitudes_count')
                            except BaseException as e:
                                log(file_path, '******' + str(e) + '******' + '\n')
                            if mblog.get('pics') != None:
                                pics = mblog.get('pics')
                                for i in range(len(pics)):
                                    print(pics[i]['large']['url'])
                                    img_url = pics[i]['large']['url']
                                    img = requests.get(img_url)
                                    img_time = datetime.datetime.strptime(str(created_at),
                                                                      "%a %b %d %H:%M:%S %z %Y").strftime(
                                    "%Y-%m-%d-%H-%M-%S")
                                # if img_time == latest_img_time:
                                #     print('图片已经下载')
                                #     sys.exit()
                                    img_name = img_time + '-' + str(i).zfill(3) + ".jpg"
                                    with open(file_path + img_name, 'ab') as f:
                                        f.write(img.content)



    def download_picture(self, url, file_path='./img'):
        if not os.path.isdir(file_path):
            os.makedirs(file_path)
        try:

        except Exception as e:


    def markdown(self):

    def run(self):
        self.get_user_info()






def get_container_id(url) -> str:
    data = get_data(url)
    content = json.loads(data).get('data')
    for tab in content.get('tabsInfo').get('tabs'):
        if tab.get('tab_type') == 'weibo':
            container_id = tab.get('containerid')
    return container_id


def get_picture(user_id, file_path):
    page_num = 0
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id
    weibo_url_prefix = url + '&containerid=' + get_container_id(url) + '&page='
    while True:
        weibo_url = weibo_url_prefix + str(page_num)
        log(file_path, weibo_url)
        try:
            page_num += 1
            data = get_data(weibo_url)
            content = json.loads(data).get('data')
            cards = content.get('cards')
            if len(cards) > 0:
                for card in range(len(cards)):
                    print("-----正在爬取第" + str(page_num) + "页，第" + str(card) + "条微博------")
                    card_type = cards[card].get('card_type')
                    if card_type == 9:
                        try:
                            mblog = cards[card].get('mblog')
                            scheme = cards[card].get('scheme')
                            created_at = mblog.get('created_at')
                            text = mblog.get('text')
                            reposts_count = mblog.get('reposts_count')
                            comments_count = mblog.get('comments_count')
                            attitudes_count = mblog.get('attitudes_count')
                        except BaseException as e:
                            log(file_path, '******' + str(e) + '******' + '\n')
                        if mblog.get('pics') != None:
                            pics = mblog.get('pics')
                            for i in range(len(pics)):
                                print(pics[i]['large']['url'])
                                img_url = pics[i]['large']['url']
                                img = requests.get(img_url)
                                img_time = datetime.datetime.strptime(str(created_at),
                                                                      "%a %b %d %H:%M:%S %z %Y").strftime(
                                    "%Y-%m-%d-%H-%M-%S")
                                # if img_time == latest_img_time:
                                #     print('图片已经下载')
                                #     sys.exit()
                                img_name = img_time + '-' + str(i).zfill(3) + ".jpg"
                                with open(file_path + img_name, 'ab') as f:
                                    f.write(img.content)
                        log(file_path,
                            "----第" + str(page_num) + "页，第" + str(card) + "条微博----" + "\n" +
                            "微博地址：" + str(scheme) + "\n" +
                            "发布时间：" + str(created_at) + "\n" +
                            "微博内容：" + text + "\n" +
                            "点赞数：" + str(attitudes_count) + "\n" +
                            "评论数：" + str(comments_count) + "\n" +
                            "转发数：" + str(reposts_count) + "\n")
            else:
                break
        except BaseException as e:
            log(file_path, '\n' + '***error***: ' + str(e) + '\n')
            pass



def log(file_path, str=""):
    with open(file_path + "log.txt", 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')
        f.write(str)


def get_latest_file(directory):
    latest_file = None
    latest_date = datetime.datetime.min
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            try:
                file_date = datetime.datetime.strptime(filename[:19], "%Y-%m-%d-%H-%M-%S")
                if file_date > latest_date:
                    latest_file = filename
                    latest_date = file_date
            except ValueError:
                pass
    return latest_file


if __name__ == "__main__":
    wb = WeiboSpider('2019071187')
    wb.run()

    # id = '2019071187'
    # user_info = get_user_info(id)
    # file_path = ".\\" + user_info["screen_name"] + "\\"
    # if not os.path.isdir(file_path):
    #     os.mkdir(file_path)
    # log(file_path, str(user_info))
    # get_picture(id, file_path)







# def get_headers() -> dict:
#     return {'User-Agent': get_user_agent()}
#

# def get_user_agent() -> str:
#     first_num = random.randint(55, 76)
#     third_num = random.randint(0, 3800)
#     fourth_num = random.randint(0, 140)
#     operation_system_type = [
#         '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
#         '(Macintosh; Intel Mac OS X 10_14_5)'
#     ]
#     chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
#
#     user_agent = ' '.join(['Mozilla/5.0', random.choice(operation_system_type), 'AppleWebKit/537.36',
#                            '(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])
#     return user_agent


# def get_proxy_ip_list() -> list[dict[str, str]]:
#     proxy_ip_list: list[dict[str, str]] = []
#     url = r"https://www.kuaidaili.com/free/inha/{}".format(1)
#     headers = {'User-Agent': get_user_agent()}
#     web_data = requests.get(url=url, headers=headers)
#     html = etree.HTML(web_data.text, etree.HTMLParser())
#     for n in range(1, 15):
#         temporary_proxy_ip_dictionary = {
#             html.xpath("//td[@data-title=\"类型\"]/text()")[n]:
#                 html.xpath("//td[@data-title=\"IP\"]/text()")[n] + ":" +
#                 html.xpath("//td[@data-title=\"PORT\"]/text()")[n]}
#         proxy_ip_list.append(temporary_proxy_ip_dictionary)
#     return proxy_ip_list
#
#
# def test_proxy_ip(proxy_ip_list) -> list[dict[str, str]]:
#     valid_proxy_ip_list = []
#     url = "http://icanhazip.com/"
#     for proxy_ip in proxy_ip_list:
#         res = requests.get(url=url, proxies=proxy_ip)
#         if res.text == proxy_ip["http"]:
#             valid_proxy_ip_list.append(proxy_ip)
#     return valid_proxy_ip_list
