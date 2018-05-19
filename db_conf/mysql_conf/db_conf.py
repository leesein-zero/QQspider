# author_li
# create time :2018/5/3

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer,VARCHAR


sql_setting={'user':'xxxxxxxxx',
             'password':'xxxxxxxxx',
             'host':'127.0.0.1:3306',
             'db':'qq_spider'}


engine=sqlalchemy.create_engine('mysql+pymysql://%s:%s@%s/%s?charset=utf8'%(sql_setting['user'],
                                                               sql_setting['password'],
                                                               sql_setting['host'],
                                                               sql_setting['db']))

Model=declarative_base()

class User(Model):
    __tablename__='user'
    id = Column(Integer,primary_key=True)
    qq_number = Column(VARCHAR(45))
    nick_name = Column(VARCHAR(45))
    shuoshuo_number = Column(VARCHAR(45))


class ShuoShuo(Model):
    __tablename__ = 'shuoshuo'
    id = Column(Integer, primary_key=True)
    content = Column(VARCHAR(200))
    time = Column(VARCHAR(45))
    visitor_number = Column(VARCHAR(45))
    comment_number = Column(VARCHAR(45))
    like_number = Column(VARCHAR(45))
    user_id = Column(Integer)