import scrapy
from scrapy.selector import Selector

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['https://www.immowelt.de/']
    start_urls = ['https://www.immowelt.de/']

    def parse(self, response):
        url = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=price'
        
        #insert your driver path
        self.driver = webdriver.Chrome('/Users/maxl/chromedriver/chromedriver')
        #self.driver = webdriver.Safari()
        #
        #
        #
        self.driver.get(url)
        sleep(3)

        counter = 0

        def waiting_func(by_variable, attribute):
            try:
                WebDriverWait(self.driver, 20).until(lambda x: x.find_element(by=by_variable,  value=attribute))
            except (NoSuchElementException, TimeoutException):
                print('{} {} not found'.format(by_variable, attribute))
                exit()

        def has_arrow(xpath):
            try:
                self.driver.find_element_by_xpath(xpath)
                return True
            except:
                return False

        #liste aller Ergebnisse auf der Seite
        #items = sel.xpath('//*[@class="listitem clear relative js-listitem "]/a')
        #items = sel.xpath('//*[@class="js-object   listitem_wrap "]')
        #items = sel.xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div')
        x = True
        while x == True:

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            #self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div[1]/div/a').click()
            sel = Selector(text=self.driver.page_source)
            items = sel.xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div')

            for i in range(len(items)):
                self.driver.find_element_by_xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div/a').click()
                sleep(2)
                title = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/h1/text()').extract()
                loc = sel.xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/span/text()').extract()
                price_k = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/app-price/div/div/div/div[1]/div[2]/div/div[1]/div[2]/strong/text()').extract()
                try:
                    price_w = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/app-price/div/div/div/div[1]/div[2]/div/div[2]/div[2]/text()').extract()
                except:
                   price_w = null
                area = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[2]/text()').extract()
                rooms = sel.xpath('//*[@id="expose"]/div[2]/div[1]/div/div[1]/div[6]/div[3]/text()').extract()
                ID = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/div[2]/app-estate-object-informations/div/div/div[1]/div[1]/div[2]/p/text()').extract()
                try:
                    merkmale = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/app-objectmeta/div/div/div[1]/div[2]/div[2]/text()').extract()
                except:
                    merkmale = null
                try:
                    features = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/div[2]/app-estate-object-informations/div/div/div[1]/div[2]/div[2]/ul/li').extract()
                except:
                    features = null
                try:
                    baujahr = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/div[2]/app-estate-object-informations/div/div/div[1]/div[3]/div[2]/ul/li[1]/text()').extract()
                except:
                    baujahr = null
                try:
                    descr = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/div[2]/app-texts/div/div/div/div/div[2]/p/text()').extract()
                except:
                    descr = null
                try:
                    lage = sel.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div/div[3]/app-map/div/div[2]/div/div/div/div[2]/p/text()').extract()
                except:
                    lage = null

                yield {'Count': counter,'ID': ID ,'Name': title, 'Standort': loc, 'Kaltmiete': price_k, 'Warmmiete': price_w, 'Wohnfläche': area, 'Zimmer': rooms, 'Baujahr': baujahr, 'Merkmale': merkmale, 'Features': features, 'Beschreibung': descr, 'Lage': lage}
                counter = counter + 1
                self.driver.back()
                sleep(2)

            if has_arrow('//*[@id="nlbPlus"]'):
                self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[5]/div/div/div/a[last()]').click()
            else:
                x = False
            sleep(2)
        

        self.driver.close()
