# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyfendoItem(scrapy.Item):
    # define the fields for your item here like:
    bookname = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    booktitle = scrapy.Field()
    bookdirnumber = scrapy.Field()
    book_List = scrapy.Field()
    book_list_tag = scrapy.Field()
    imgUrl = scrapy.Field()
    author = scrapy.Field()
