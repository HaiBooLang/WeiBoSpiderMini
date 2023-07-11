# -*- coding: utf-8 -*-
import random
import json
import re
import sys
import time
import requests
import os
import datetime


def get_headers() -> dict:
    first_num = random.randint(63, 69)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    operation_system_type = [
        '(Windows NT 10.0; Win64; x64)', '(Windows NT 10.0; WOW64)', '(Windows NT 6.1; WOW64)',
        '(X11; Linux x86_64)', '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    pc_user_agent = f'Mozilla/5.0 {random.choice(operation_system_type)} AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    f'{chrome_version} Safari/537.36'

    ipad_mini_user_agent = 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                           'CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/114.0.0.0'

    iphone_12pro_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, ' \
                              'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/114.0.0.0'

    samsung_s20u_user_agent = 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                              'Chrome/80.0.3987.162 Mobile Safari/537.36 Edg/114.0.0.0'

    samsung_fold_user_agent = 'Mozilla/5.0 (Linux; Android 9.0; SAMSUNG SM-F900U Build/PPR1.180610.011) ' \
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 ' \
                              'Edg/114.0.1823.67'

    huawei_p30_user_agent = 'Mozilla/5.0 (Linux; Android 9; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (' \
                            'KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile ' \
                            'Safari/537.36 MMWEBID/8968 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools ' \
                            'NetType/4G Language/zh_CN ABI/arm64'

    huawei_mate20_user_agent = 'Mozilla/5.0 (Linux; Android 9; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 ' \
                               '(KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36 ' \
                               'MMWEBID/1247 MicroMessenger/7.0.10.1561(0x27000A41) Process/tools NetType/4G ' \
                               'Language/zh_CN ABI/arm64 GPVersion/1'

    user_agent_list = [pc_user_agent, ipad_mini_user_agent, iphone_12pro_user_agent, samsung_s20u_user_agent,
                       huawei_p30_user_agent, huawei_mate20_user_agent, samsung_fold_user_agent]

    return {'User-Agent': random.choice(user_agent_list)}


def get_data(url) -> str:
    try:
        data = requests.get(url=url, headers=get_headers()).text
        return data
    except requests.exceptions.RequestException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return ''


def get_container_id(url) -> str:
    try:
        data = get_data(url)
        content = json.loads(data).get('data')
        for tab in content.get('tabsInfo').get('tabs'):
            if tab.get('tab_type') == 'weibo':
                container_id = tab.get('containerid')
                return container_id
    except BaseException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return ''


def get_weibo_data(weibo_url):
    try:
        data = get_data(weibo_url)
        cards = json.loads(data).get('data').get('cards')
        return cards
    except BaseException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return []


def get_user_info(user_id) -> dict:
    try:
        data = get_data(f'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}')
        user_info = json.loads(data).get('data').get('userInfo')
        return {key: user_info.get(key, '') for key in
                ['screen_name', 'profile_url', 'statuses_count', 'verified_reason', 'description', 'follow_count',
                 'followers_count']}
    except BaseException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return {}


def get_mblog_data(card):
    try:
        mblog = card.get('mblog')
        return {
            'created_at': mblog.get('created_at', ''),
            'text': mblog.get('text', ''),
            'reposts_count': mblog.get('reposts_count', 0),
            'comments_count': mblog.get('comments_count', 0),
            'attitudes_count': mblog.get('attitudes_count', 0),
            'pics': [pic['large']['url'] for pic in mblog.get('pics', [])]
        }
    except BaseException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return {}


def get_picture(user_id, file_path):
    page_num = 0
    url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}'
    container_id = get_container_id(url)
    weibo_url_prefix = f'{url}&containerid={container_id}&page='
    while True:
        weibo_url = weibo_url_prefix + str(page_num)
        log(file_path, weibo_url)
        try:
            page_num += 1

            cards = get_weibo_data(weibo_url)

            if len(cards) > 0:

                for card in range(len(cards)):
                    print("-----正在爬取第" + str(page_num) + "页，第" + str(card) + "条微博------")
                    card_type = cards[card].get('card_type')
                    if card_type == 9:

                        mblog_data = get_mblog_data(cards[card])

                        pics = mblog_data.get('pics', [])
                        for i, img_url in enumerate(pics):
                            print(img_url)

                            img = requests.get(img_url)
                            created_at = mblog_data['created_at']
                            img_time = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                            img_time_str = img_time.strftime("%Y-%m-%d-%H-%M-%S")

                            if latest_time > img_time.replace(tzinfo=None) > oldest_file:
                                print(f'{img_url}图片已经下载')
                                continue


                            img_name = f'{img_time_str}-{str(i).zfill(2)}.jpg'
                            with open(f'{file_path}{img_name}', 'ab') as f:
                                f.write(img.content)

                        mblog_data.get('scheme', '')

                        weibo_num = f'第{page_num}页，第{card}条微博'
                        weibo_url = f"微博地址：{mblog_data.get('scheme', '')}"
                        created_at = f"发布时间：{mblog_data.get('created_at', '')}"
                        weibo_text = f"微博内容：{mblog_data.get('text', '')}"
                        attitudes_count = f"点赞数：{mblog_data.get('attitudes_count', '')}"
                        comments_count = f"评论数：{mblog_data.get('comments_count', '')}"
                        reposts_count = f"转发数：{mblog_data.get('reposts_count', '')}"

                        log(file_path,
                            f'{weibo_num}\n{weibo_url}\n{created_at}\n{weibo_text}\n{attitudes_count}\n{comments_count}\n{reposts_count}\n')
                        # markdown(file_path,
                        #          '# ' + img_time + '\n'
                        #                            '![](' + './' + img_name + ')'+'\n'
                        #          )
            else:
                break
        except BaseException as e:
            log(file_path, '\n' + '***error***: ' + str(e) + '\n')
            pass


def log(file_path, str=""):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open(f'{file_path}log.txt', 'a', encoding='utf-8') as f:
        f.write(f'{current_time}\n{str}')

def get_latest_file(directory):
    date_format = '%Y-%m-%d-%H-%M-%S'
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".jpg")]
    latest_file = max(files, key=lambda x: datetime.datetime.strptime(x[:19], date_format), default=None)
    oldest_file = min(files, key=lambda x: datetime.datetime.strptime(x[:19], date_format), default=None)
    return latest_file, oldest_file

latest_time = None
oldest_file = None

if __name__ == "__main__":

    latest_file, oldest_file = get_latest_file('.//罗小黑CAT//')
    latest_time = datetime.datetime.strptime(latest_file[:19] ,'%Y-%m-%d-%H-%M-%S')
    oldest_file = datetime.datetime.strptime(oldest_file[:19] ,'%Y-%m-%d-%H-%M-%S')


    user_id = '2019071187'
    user_info = get_user_info(user_id)
    screen_name = user_info['screen_name']
    file_path = f'.\\{screen_name}\\'

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    log(file_path, str(user_info))
    get_picture(user_id, file_path)

# def markdown(file_path, str=""):
#     with open(file_path + "weibo.md", 'a', encoding='utf-8') as f:
#         f.write(str)



