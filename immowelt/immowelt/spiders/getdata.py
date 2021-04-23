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
        url = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?sort=price&cp=15'
        
        #insert your driver path
        #self.driver = webdriver.Chrome('/Users/maxl/chromedriver/chromedriver')
        self.driver = webdriver.Chrome('/Users/Alex/DRIVERS/chromedriver/chromedriver')
        #self.driver = webdriver.Safari()
        #
        #
        #
        self.driver.get(url)
        sleep(1)

        counter = 0

        #Wartefunktion wartet bis eine bestimmte Variable, z.B. ein xPath, gefunden wird
        def waiting_func(by_variable, attribute):
            try:
                WebDriverWait(self.driver, 20).until(lambda x: x.find_element(by=by_variable,  value=attribute))
            except (NoSuchElementException, TimeoutException):
                print('{} {} not found'.format(by_variable, attribute))
                exit()

        #Funktion gibt zurück, ob auf der Seite ein Element mit dem angegebenen xPath existiert, z.B. ein Pfeil auf die nächste Seite
        def has_arrow(xpath):
            try:
                self.driver.find_element_by_xpath(xpath)
                return True
            except:
                return False

        #Schleife, die so lange läuft, bis die letzte Seite erreicht wird
        x = True
        while x == True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            sel = Selector(text=self.driver.page_source)
            #Liste aller Ergebnisse auf der Seite, fixe und dynamische
            items1 = sel.xpath('//*[@id="listItemWrapperFixed"]/div')
            items2 = sel.xpath('//*[@id="listItemWrapperAsync"]/div')

            sleep(1)

            #Über fixe Einträge iterieren
            for i in range(len(items1)):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #warten bis i-tes Ergebnis gefunden wurde
                waiting_func('xpath', '//html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div/a')
                #anklicken des i-ten Ergebnisses
                self.driver.find_element_by_xpath('/html/body/div/div[2]/div[5]/div[1]/div[2]/div[2]/div[1]/div['+str(i+1)+']/div/a').click()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)

                sel = Selector(text=self.driver.page_source)
                #extrahieren der Features des i-ten Ergebnisses
                title = sel.xpath('/html/head/title/text()').extract()
                loc = sel.xpath('//*[@class="location"]/span/text()').extract()
                price_k = sel.xpath('//*[contains(text(),"Kaltmiete")]/preceding-sibling::strong/text()').extract()
                
                #einige Features werden nicht bei allen Objekten angegeben. Wo sie nicht vorhanden sind soll ein Alternativwert im Datensatz eingetragen werden
                try:
                    price_w = sel.xpath('//*[contains(text(),"Warmmiete")]/following-sibling::div[1]/text()').extract()
                except:
                    price_w = -1

                area = sel.xpath('//*[contains(text(),"Wohnfläche")]/preceding-sibling::span/text()').extract()
                rooms = sel.xpath('//*[@class="hardfact rooms ng-star-inserted"]/span/text()').extract()
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
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

            # Über dynamische Einträge iterieren
            for i in range(len(items2)):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                #warten bis i-tes Ergebnis gefunden wurde
                waiting_func('xpath', '//*[@id="listItemWrapperAsync"]/div['+str(i+1)+']/div/a')
                #anklicken des i-ten Ergebnisses
                self.driver.find_element_by_xpath('//*[@id="listItemWrapperAsync"]/div['+str(i+1)+']/div/a').click()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)

                sel = Selector(text=self.driver.page_source)
                #extrahieren der Features des i-ten Ergebnisses
                title = sel.xpath('/html/head/title/text()').extract()
                loc = sel.xpath('//*[@class="location"]/span/text()').extract()
                price_k = sel.xpath('//*[contains(text(),"Kaltmiete")]/preceding-sibling::strong/text()').extract()
                
                #einige Features werden nicht bei allen Objekten angegeben. Wo sie nicht vorhanden sind soll ein Alternativwert im Datensatz eingetragen werden
                try:
                    price_w = sel.xpath('//*[contains(text(),"Warmmiete")]/following-sibling::div[1]/text()').extract()
                except:
                    price_w = -1

                area = sel.xpath('//*[contains(text(),"Wohnfläche")]/preceding-sibling::span/text()').extract()
                rooms = sel.xpath('//*[@class="hardfact rooms ng-star-inserted"]/span/text()').extract()
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
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

            #prüfen, ob am Ende der Seite ein Pfeil auf die nächste Seite ist
            if has_arrow('//*[@id="nlbPlus"]'):
            	#wenn ja: anklicken
                element = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[5]/div/div/div/a[last()]')
                self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
                self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[5]/div[1]/div[2]/div[5]/div/div/div/a[last()]').click()
            else:
            	#wenn nein: der Crawler hat die Features aller Ergebnisse der letzten Seite extrahiert und ist am Ende angelangt, also wird die Schleife beendet
                x = False
            sleep(1)
        
        #der Crawler ist fertig und wird geschlossen
        self.driver.close()
