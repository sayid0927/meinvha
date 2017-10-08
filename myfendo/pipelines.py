# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs
from scrapy.conf import settings
import pymysql


class MyfendoPipeline(object):
    def __init__(self):

        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='sayid', passwd='111', db='test', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        booktitle = item['booktitle']
        bookname = item['bookname']
        bookdirnumber = item['bookdirnumber']
        book_list_tag = item['book_list_tag']
        book_List = item['book_List']
        bookname = bookname.replace('<h>', " ").replace('</h>', " ")
        bookname = bookname.strip()
        content = item['content']


        if not os.path.exists(book_List):
            os.makedirs(book_List)
        book_List_Ptah = os.path.abspath(book_List)

        conut = self.cursor.execute("select * from book_list where book_list= '%s'" % book_List)
        self.cursor.fetchall()
        if conut==0:
            sql = "insert into book_list(book_list, book_list_tag) values(%s,%s)"
            params = (book_List, book_list_tag)
            self.cursor.execute(sql, params)
        else:
            pass

        if not os.path.exists(bookname):
            try:
                os.makedirs(book_List_Ptah + "/" + bookname)
            except OSError:
                pass

        conut = self.cursor.execute("select * from book_name where book_name= '%s'" % bookname)
        self.cursor.fetchall()
        if conut == 0:
            self.cursor.execute("select * from book_list where book_list= '%s'" %book_List)
            re = self.cursor.fetchall()
            book_list_id = re[0][0]
            sql = "insert into book_name(book_name, book_list_id) values(%s,%s)"
            params = (bookname, book_list_id)
            self.cursor.execute(sql, params)
        else:
            pass


        ss = os.path.abspath(book_List_Ptah + "/" + bookname)
        filename = codecs.open(ss + "/" + booktitle + '.text', 'wb', encoding="utf-8")
        filename.write(content)
        filePath = os.path.abspath(filename.name)
        url = item['url']

        conut = self.cursor.execute("select * from book where book_title= '%s'" % booktitle)
        self.cursor.fetchall()

        if conut == 0:
            self.cursor.execute("select * from book_name where book_name= '%s'" % bookname)
            re = self.cursor.fetchall()
            book_name_id = re[0][0]
            sql = "insert into book(book_title, book_url,book_path,book_number,book_name_id) values(%s,%s,%s,%s,%s)"
            params = (booktitle, url, filePath, bookdirnumber, book_name_id)
            self.cursor.execute(sql, params)
        else:
            pass
        self.conn.commit()

        return item
