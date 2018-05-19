# author_li
# create time :2018/4/30
from shuoshuo import deal_one
from db_conf.redis_conf.db_conf import *
import threading
from login import write_into


start_setting={
    'qq_number':'xxxxxxxxx',
    'password':'xxxxxxxxx'
}


def mian():
    write_into()
    deal_one(start_setting['qq_number'])
    t1 = threading.Thread(target=do_one())
    t2 = threading.Thread(target=do_one())
    t3 = threading.Thread(target=do_one())
    t4 = threading.Thread(target=do_one())
    t5 = threading.Thread(target=do_one())
    t6 = threading.Thread(target=do_one())
    t7 = threading.Thread(target=do_one())
    t8 = threading.Thread(target=do_one())
    t_list = [t1,t2,t3,t4,t5,t6,t7,t8]
    for i in t_list:
        i.start()



def do_one():
    while True:
        number = conn.spop('wait_queue').decode('utf8')
        deal_one(number)



if __name__ == '__main__':
    mian()