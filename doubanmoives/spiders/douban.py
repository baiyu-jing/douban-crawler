import scrapy
from lxml import etree
import re
from scrapy import Request

from doubanmoives.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]

    async def start(self):
        for i in range(0, 251, 25):
            yield Request(url=f"https://movie.douban.com/top250?start={i}&filter=")

    # start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        html = etree.HTML(response.text)
        movies = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

        for movie in movies:
            movie_item=MovieItem()
            movie_item['name'] = movie.xpath('./div/div[2]/div[1]/a/span[1]/text()')
            movie_item['director'] = movie.xpath('./div/div[2]/div[2]/p[1]/text()')[0].split('   ')[0]
            year_str = movie.xpath('./div/div[2]/div[2]/p[1]/text()')[1].split('/')[0]
            movie_item['year'] = int(re.search(r'\d{4}', year_str).group())

            yield movie_item
