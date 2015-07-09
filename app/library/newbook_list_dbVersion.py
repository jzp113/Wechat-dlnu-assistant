# -*- coding: utf-8 -*-
import sys, os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from sqlalchemy import create_engine
#from config import SQLALCHEMY_BINDS

class newbook_list:
    
    def __init__(self, username):
        self.username = username
        self.link = SQLALCHEMY_BINDS['Library']
        
        
    def get_data(self):
        book =[]
        engine = create_engine(self.link)
        booklist = engine.execute('''SELECT M_TITLE, NORM_RET_DATE 
                                     FROM LEND_LST, ITEM, MARC 
                                     WHERE LEND_LST.PROP_NO =        ITEM.PROP_NO AND ITEM.MARC_REC_NO = MARC.MARC_REC_NO AND LEND_LST.CERT_ID = :id''', id = self.username).fetchall()

        if booklist == []:
            return u'无借阅信息'
        else:
            for item in booklist:
                row = u'\n%s  到期时间: %s'% (item[0], item[1])
                book.append(row)
            book = ''.join(book)
            return book
        
   

        
        
