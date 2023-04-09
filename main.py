# -*- coding: utf-8 -*-
import random
import json
import time
import requests
import os
import datetime


def get_headers() -> dict:
    return {'User-Agent': get_user_agent()}


def get_user_agent() -> str:
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    operation_system_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    user_agent = ' '.join(['Mozilla/5.0', random.choice(operation_system_type), 'AppleWebKit/537.36',
                           '(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])
    return user_agent


def get_data(url) -> str:
    data = requests.get(url=url, headers=get_headers()).text
    return data


def get_container_id(url) -> str:
    data = get_data(url)
    content = json.loads(data).get('data')
    for tab in content.get('tabsInfo').get('tabs'):
        if tab.get('tab_type') == 'weibo':
            container_id = tab.get('containerid')
    return container_id


def get_user_info(user_id) -> dict:
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id
    data = get_data(url)
    user_info = json.loads(data).get('data').get('userInfo')
    user_info = {'screen_name': user_info.get('screen_name'),
                 'profile_url': user_info.get('profile_url'),
                 'verified_reason': user_info.get('verified_reason'),
                 'description': user_info.get('description'),
                 'follow_count': user_info.get('follow_count'),
                 'followers_count': user_info.get('followers_count')}
    return user_info


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
                        markdown(file_path,
                                 '# ' + img_time + '\n'
                                                   '![](' + './' + img_name + ')'+'\n'
                                 )
            else:
                break
        except BaseException as e:
            log(file_path, '\n'+'***error***: ' + str(e) +  '\n')
            pass


def markdown(file_path, str=""):
    with open(file_path + "weibo.md", 'a', encoding='utf-8') as f:
        f.write(str)


def log(file_path, str=""):
    with open(file_path + "log.txt", 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')
        f.write(str)


if __name__ == "__main__":

    id = '2019071187'
    user_info = get_user_info(id)
    file_path = ".\\" + user_info["screen_name"] + "\\"
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    log(file_path, str(user_info))
    get_picture(id, file_path)

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
