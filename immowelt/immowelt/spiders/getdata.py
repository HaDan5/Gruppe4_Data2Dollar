import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from time import sleep


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['https://www.immowelt.de/']
    start_urls = ['https://www.immowelt.de/']

    def parse(self, response):
        url = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=price'
        
        #insert your driver path
        self.driver = webdriver.Chrome('/Users/maxl/chromedriver/chromedriver')
        #
        #
        #
        self.driver.get(url)
        #create Selector
        sel = Selector(text=self.driver.page_source)
        #liste aller Ergebnisse auf der Seite
        #items = sel.xpath('//*[@class="listitem clear relative js-listitem "]/a')
        items = sel.xpath('//*[@class="js-object   listitem_wrap "]')
        for i in range(len(items)):
        	#Ergebnis i anklicken
        	self.driver.find_elements_by_xpath('//*[@class="listitem clear relative js-listitem "]/a')[i].click()
        	#Daten zu Ergebniss i extrahieren
        	sel = Selector(text=self.driver.page_source)
        	title = sel.xpath('//*[@class="quickfacts iw_left"]/h1').extract()
        	loc = sel.xpath('//*[@class="no_s"').extract()
        	price = sel.xpath('//*[@class="hardfact"][1]/strong').extract()
        	area = sel.xpath('//*[@class="hardfact"][2]').extract()
        	rooms = sel.xpath('//*[@class="hardfact rooms"]').extract()
        	sleep (2)
        	self.driver.back()
        	yield {'Name': title, 'Standort': loc, 'Kaltmiete': price, 'Wohnfläche': area, 'Zimmer': rooms}
        	sleep (2)

        self.driver.close()
