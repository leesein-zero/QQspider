# author_li
# create time :2018/4/30
import requests
from tools import config
import login
from db_conf.mysql_conf.into_db_api import *
from db_conf.redis_conf.db_conf import *
import redis
import re
import sys
sys.setrecursionlimit(1000000) #例如这里设置为一百万

def read_key():
    with open('cookie.ini','r') as f:
        cookie , g_tk = f.read().split('liyang')
    return cookie , g_tk


cookie , g_tk = read_key()
headers={'user-agent' : config.UserAgents[24]}
cookies={
    'cookie':cookie
}



def get_shuoshuo_index(qq_number):

    req=requests.get('https://mobile.qzone.qq.com/combo?g_tk={}'
                 '&hostuin={}&action=1&g_f=&refresh_type=1&res_type=2&format=json'.format(g_tk,qq_number),
                 headers=headers,
                 cookies=cookies)
    print(req.json())
    get_friends(str(req.json()))
    if 'data' in req.json():
        if 'vFeeds' in req.json()['data']['feeds']:
            conn.sadd('worked_queue',qq_number)


            for index, value in enumerate(req.json()['data']['feeds']['vFeeds']):
                deal_item(value)

            basetime = req.json()['data']['feeds']['vFeeds'][-1]['comm']['time']
            return basetime

        else:
            conn.sadd('unwork_queue',qq_number)
            return False
    else:
        return False





def get_shuoshuo_next(basetime,qq_number,id):
    '''

    :param basetime: 时间戳
    '''
    req = requests.get('https://mobile.qzone.qq.com/get_feeds?g_tk={}&hostuin={}&res_type=2&res_attach'
                    '=att%3Dback%255Fserver%255Finfo%253Doffset%25253D{}6%252526total%25253D8%252526basetime'
                    '%25253D{}%252526feedsource%25253D0%2526lastrefreshtime%253D1525242289'
                    '%2526lastseparatortime%253D0%2526loadcount%253D3%26tl%3D{}&refresh_type=2&format=json'
                    ''.format(g_tk,qq_number,id,basetime,basetime),headers=headers,cookies=cookies)
    # print(req.json())
    get_friends(str(req.json()))
    if 'data' in req.json():
        if 'vFeeds' in req.json()['data']:
            for index , value in enumerate(req.json()['data']['vFeeds']):
                deal_item(value)

            basetime = req.json()['data']['vFeeds'][-1]['comm']['time']
            # print(basetime)
            id += 1
            get_shuoshuo_next(basetime,qq_number,id)

    else:
        return -1


def deal_item(item):
    '''
    处理单条说说，并入库
    :return:
    '''
    if 'summary' in item:
        content = item['summary']['summary']
    else:
        content=' '
    # print(content)
    time = item['comm']['time']
    if 'visitor' in item:
        visitor_number = item['visitor']['view_count']
    else:
        visitor_number = '0'
    if 'comment' in item:
        comment_number = item['comment']['num']
    else:
        comment_number = '0'
    if 'like' in item:
        like_number = item['like']['num']
    else:
        like_number = '0'
    user_id = '0'

    into_shuoshuo(content, time, visitor_number, comment_number, like_number, user_id)



def deal_one(qq_number):
    try:
        id = 0
        basetime = get_shuoshuo_index(qq_number)
        if basetime != False:
            get_shuoshuo_next(basetime,qq_number,id)
    except:
        global cookies,cookie,g_tk
        login.write_into()
        cookie, g_tk = read_key()
        cookies = {
            'cookie': cookie
        }
        basetime = get_shuoshuo_index(qq_number)
        get_shuoshuo_next(basetime,qq_number,id)




def get_friends(source_code):
    number_list = set(re.compile(r'\'uin\': \'(.*?)\',').findall(source_code))
    for i in number_list:
        conn.sadd('wait_queue',i)



if __name__ == '__main__':
    x=conn.spop('wait_queue').decode('utf8')
    print(x)
    deal_one(x)
    deal_one('1810824959')
