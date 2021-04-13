import scrapy


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['https://www.immowelt.de/']
    start_urls = ['http://https://www.immowelt.de//']

    def parse(self, response):
        pass
