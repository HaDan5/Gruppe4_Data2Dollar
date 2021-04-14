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

        def has_arrow(xpath):
            try:
                self.driver.find_element_by_xpath(xpath)
                return True
            except:
                return False

        #create Selector
        #sel = Selector(text=self.driver.page_source)
        #liste aller Ergebnisse auf der Seite
        #items = sel.xpath('//*[@class="listitem clear relative js-listitem "]/a')
        #items = sel.xpath('//*[@class="js-object   listitem_wrap "]')
        #items = sel.xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div')
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div[1]/div/a').click()
        sel = Selector(text=self.driver.page_source)
        title = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/h1/text()').extract()
        loc = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/span/text()').extract()
        price = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[1]/strong/text()').extract()
        area = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[2]/text()').extract()
        rooms = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[3]/text()').extract()
        yield {'Name': title, 'Standort': loc, 'Kaltmiete': price, 'Wohnfläche': area, 'Zimmer': rooms}
        sleep (2)
        self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/a').click()
        #for i in range(len(items)):
        counter = 0
        x = True
        while x == True:
        	#Ergebnis i anklicken
        	#self.driver.find_element_by_xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div/a').click()
        	#Daten zu Ergebniss i extrahieren
            sel = Selector(text=self.driver.page_source)
            title = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/h1/text()').extract()
            loc = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/span/text()').extract()
            price = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[1]/strong/text()').extract()
            area = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[2]/text()').extract()
            rooms = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[3]/text()').extract()
        	#sleep (2)
            #self.driver.back()
            yield {'ID': counter ,'Name': title, 'Standort': loc, 'Kaltmiete': price, 'Wohnfläche': area, 'Zimmer': rooms}
            sleep(3)
            if has_arrow('/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/a[2]') == False:
                break
            counter = counter + 1
            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/a[2]').click()

        self.driver.close()
