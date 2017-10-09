# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myfendo.items import MyfendoItem


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com']
    # rules = (
    #     Rule(LinkExtractor(allow=r'list/\d+.html'), process_links = "deal_links", callback='parse_item'),
    #     # Rule(LinkExtractor(allow=r'\d+')),
    #     # Rule(LinkExtractor(allow=r'book/\d+/\d+/\d+.html'), callback='parse_item'),
    # )
    #
    # def deal_links(self, links):
    #     for each in links:
    #         print(each)
    #         # each.url = each.url.replace("?", "&").replace("Type&", "Type?")
    #     return links

    def parse(self, response):
        links = response.xpath('//ul[@class="channel-nav-list"]//@href').extract()
        book_List = response.xpath('//ul[@class="channel-nav-list"]//a/text()').extract()
        for link in links:
            i = links.index(link)
            yield scrapy.Request(link, meta={'book_List': book_List[i], 'book_list_tag': i}, callback=self.book_list)

    def book_list(self, response):
        links = response.xpath('//em[@class="c999 clearfix"]//@href').extract()
        imgUrl_list = response.xpath('//a[@class ="l mr10"]/img /@src').extract()

        book_List = response.meta['book_List']
        book_list_tag = response.meta['book_list_tag']

        for link in links:
            i = links.index(link)
            yield scrapy.Request(link, meta={'book_List': book_List, 'book_list_tag':book_list_tag, 'imgUrl': imgUrl_list[i]}, callback=self.book_href)

    def book_href(self, response):
        links = response.xpath('//a[@class="reader"]//@href').extract()[0]
        book_List = response.meta['book_List']
        imgUrl = response.meta['imgUrl']
        book_list_tag = response.meta['book_list_tag']
        yield scrapy.Request(links, meta={'imgUrl': imgUrl, 'href_url': links, 'book_List': book_List,'book_list_tag':book_list_tag}, callback = self.book_dir)

    def book_dir(self, response):
        links = response.xpath('//div[@class="clearfix dirconone"]//@href').extract()
        booktitle = response.xpath('//div[@class="clearfix dirconone"]//@title').extract()
        bookname = response.xpath('//div[@class ="chapName"]//strong/text()').extract()[0]
        author = response.xpath('//span[@class ="r"]/text()').extract()

        href_url = response.meta['href_url']
        book_List = response.meta['book_List']
        imgUrl = response.meta['imgUrl']
        book_list_tag = response.meta['book_list_tag']
        for link in links:
            try:
              i = links.index(link)
            except Exception:
              pass
            yield scrapy.Request(href_url + "/" + link, meta={'author': author, 'imgUrl': imgUrl, 'bookname': bookname, 'booktitle': booktitle[i], 'bookdirnumber':i, 'book_List': book_List,'book_list_tag':book_list_tag}, callback=self.process_item)

    def process_item(self, response):
        i = MyfendoItem()
        links = response.xpath('//div[@class="mainContenr"]/text()').extract()
        content = ''.join(links)
        content = content.replace('<p>', "").replace('</p>', "").replace('<br>', "\n").replace(u'\xa0', "")
        bookname = response.meta['bookname']
        booktitle = response.meta['booktitle']
        bookdirnumber =response.meta['bookdirnumber']
        book_list_tag = response.meta['book_list_tag']
        imgUrl = response.meta['imgUrl']
        author = response.meta['author']
        i['bookname'] = bookname
        i['content'] = content
        i['url'] = response.url
        i['booktitle'] = booktitle
        i['bookdirnumber'] = bookdirnumber
        i['book_List'] = response.meta['book_List']
        i['book_list_tag'] = book_list_tag
        i['imgUrl'] = imgUrl
        i['author'] = author

        yield i

