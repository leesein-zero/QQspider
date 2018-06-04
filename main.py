# author_li
# create time :2018/4/30
from concurrent.futures import ThreadPoolExecutor

from db_conf.redis_conf.db_conf import *
from login import write_into, start_setting
from shuoshuo import deal_one


def mian():
    write_into()
    deal_one(start_setting['qq_number'])
    with ThreadPoolExecutor(max_workers=12) as e:
        k=0
        while(k<13):
            e.submit(do_one)
            k+=1


def do_one():
    while True:
        number = conn.spop('wait_queue').decode('utf8')
        deal_one(number)



if __name__ == '__main__':
    mian()