# author_li
# create time :2018/5/3
from db_conf.mysql_conf.db_conf import *
from sqlalchemy.orm import sessionmaker

Model.metadata.create_all(engine)

Session_class = sessionmaker(bind=engine)
Session = Session_class()

def into_user(qq_number,nick_name,shuoshuo_number):
    user = User(qq_number=qq_number,nick_name=nick_name,shuoshuo_number=shuoshuo_number)
    Session.add(user)
    Session.commit()

def into_shuoshuo(content,time,visitor_number,comment_number,like_number,user_id):
    try:
        shuoshuo = ShuoShuo(content=content, time=time, visitor_number=visitor_number, comment_number=comment_number,
                            like_number=like_number, user_id=user_id)
        Session.add(shuoshuo)
        Session.commit()
    except:
        Session.rollback()
    # finally:
    #     shuoshuo = ShuoShuo(content='wrong content', time=time, visitor_number=visitor_number,
    #                         comment_number=comment_number,
    #                         like_number=like_number, user_id=user_id)
    #     Session.add(shuoshuo)
    #     Session.commit()




