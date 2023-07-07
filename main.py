# -*- coding: utf-8 -*-
import random
import json
import sys
import time
import requests
import os
import datetime


def get_headers()->dict:
    first_num = random.randint(63, 69)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    operation_system_type = [
        '(Windows NT 10.0; Win64; x64)', '(Windows NT 10.0; WOW64)', '(Windows NT 6.1; WOW64)',
        '(X11; Linux x86_64)', '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)
    
    pc_user_agent = ' '.join(
        ['Mozilla/5.0', random.choice(operation_system_type), 'AppleWebKit/537.36',
         '(KHTML, like Gecko)', chrome_version, 'Safari/537.36'])

    ipad_mini_user_agent = ' '.join(
        ['Mozilla/5.0', '(iPad; CPU OS 13_3 like Mac OS X)', 'AppleWebKit/605.1.15',
         '(KHTML, like Gecko)', 'CriOS/87.0.4280.77', 'Mobile/15E148', 'Safari/604.1',
         'Edg/114.0.0.0'])

    iphone_12pro_user_agent = ' '.join(
        ['Mozilla/5.0', '(iPhone; CPU iPhone OS 13_2_3 like Mac OS X)', 'AppleWebKit/605.1.15',
         '(KHTML, like Gecko)', 'Version/13.0.3', 'Mobile/15E148', 'Safari/604.1',
         'Edg/114.0.0.0'])

    samsung_s20u_user_agent = ' '.join(
        ['Mozilla/5.0', '(Linux; Android 10; SM-G981B)', 'AppleWebKit/537.36',
         '(KHTML, like Gecko)', 'Chrome/80.0.3987.162', 'Mobile', 'Safari/537.36',
         'Edg/114.0.0.0'])

    user_agent_list = [pc_user_agent,ipad_mini_user_agent,iphone_12pro_user_agent,samsung_s20u_user_agent]

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
    except requests.exceptions.RequestException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return {}


def get_mblog_data(card):
    try:
        mblog = card.get('mblog')
        pics = [pic['large']['url'] for pic in mblog.get('pics', [])]
        return {
            'created_at': mblog.get('created_at', ''),
            'text': mblog.get('text', ''),
            'reposts_count': mblog.get('reposts_count', 0),
            'comments_count': mblog.get('comments_count', 0),
            'attitudes_count': mblog.get('attitudes_count', 0),
            'pics': pics
        }
    except BaseException as e:
        log(file_path, '******' + str(e) + '******' + '\n')
        return {}


def get_picture(user_id, file_path):
    page_num = 0
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + user_id
    weibo_url_prefix = url + '&containerid=' + get_container_id(url) + '&page='
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

                        if mblog_data['pics'] != None:
                            for i in range(len(mblog_data['pics'])):
                                print(mblog_data['pics'][i])
                                img_url = mblog_data['pics'][i]
                                img = requests.get(img_url)
                                img_time = datetime.datetime.strptime(str(mblog_data['created_at']),
                                                                      "%a %b %d %H:%M:%S %z %Y").strftime(
                                    "%Y-%m-%d-%H-%M-%S")
                                # if img_time == latest_img_time:
                                #     print('图片已经下载')
                                #     sys.exit()
                                img_name = img_time + '-' + str(i).zfill(3) + ".jpg"
                                with open(file_path + img_name, 'ab') as f:
                                    f.write(img.content)
                        # log(file_path,
                        #     "----第" + str(page_num) + "页，第" + str(card) + "条微博----" + "\n" +
                        #     "微博地址：" + str(scheme) + "\n" +
                        #     "发布时间：" + str(created_at) + "\n" +
                        #     "微博内容：" + text + "\n" +
                        #     "点赞数：" + str(attitudes_count) + "\n" +
                        #     "评论数：" + str(comments_count) + "\n" +
                        #     "转发数：" + str(reposts_count) + "\n")
                        # markdown(file_path,
                        #          '# ' + img_time + '\n'
                        #                            '![](' + './' + img_name + ')'+'\n'
                        #          )
            else:
                break
        except BaseException as e:
            log(file_path, '\n' + '***error***: ' + str(e) + '\n')
            pass


def markdown(file_path, str=""):
    with open(file_path + "weibo.md", 'a', encoding='utf-8') as f:
        f.write(str)


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
    id = '2019071187'
    user_info = get_user_info(id)
    file_path = ".\\" + user_info["screen_name"] + "\\"
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    log(file_path, str(user_info))
    get_picture(id, file_path)
