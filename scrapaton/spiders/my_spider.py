

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapaton.items import ScrapatonUrl, Event
from scrapy.http import Request

from scrapy import log

import urlparse


class MySpider(BaseSpider):
    name = "my_spider"
    allowed_domains = ['es.wikipedia.org']
    start_urls = ['http://es.wikipedia.org/wiki/Presidente_de_Chile']

    def parse(self, response):

	self.log('parse url: <%s>' % response.url)
        hxs = HtmlXPathSelector(response)

        #foto = hxs.select('/html/body//table[@class="infobox_v2"]//tr/td/a/img/@src').extract()
        #nombre = hxs.select('/html/body//table[@class="infobox_v2"]//tr[1]/th').extract()
        #yield Presidente(nombre=nombre, foto=foto)

        #result = []


        #urls = hxs.select('/html/body//table[@class="wikitable"]//tr/td[1]//a/@href').extract()
        #start = hxs.select('/html/body//table[@class="wikitable"]//tr/td[2]/b/a').extract()
        #self.log(start)

        rows = hxs.select('/html/body//table[@class="wikitable"]//tr')

        for row in rows:



            links = row.select('td[1]//a/@href').extract()

            for link in links:
                #event = Event()
                #event['start'] = '1900'
                link = 'http://es.wikipedia.org' + link

                #event['link'] = link
                request = Request(link, callback=self.parse_url)
                #request =  Request('http://es.wikipedia.org/%s' % link[1:], callback=self.parse_url)
                #yield request

                #self.log("                <%s>" % request)

                #request.meta['event'] = event
                yield request
                #result.append(request)

                #request.meta['event'] = event 
        
    def parse_url(self, response):
        self.log('parse_presidente url: <%s>' % response.url)
        hxs = HtmlXPathSelector(response)
        
	foto = hxs.select('/html/body//table[@class="infobox_v2"]//tr/td/a/img/@src').extract()#.re('//(.*)')
        nombre = hxs.select('/html/body//table[@class="infobox_v2"]//tr[1]/th/span/text()').extract()

        desc = hxs.select('/html/body//table[@class="infobox_v2"]//tr/th/div[@style="background-color:lavender"]/a/@title').extract()
        #nacimiento .hxs.select('/html/body//table[@class="infobox_v2"]//tr').re("th")

        #/html/body//table[@class="infobox_v2"]//tr[contains(td, 'Nacimiento')]/td[2]
        #nac = hxs.select('/html/body//table[@class="infobox_v2"]//tr')
        nac = hxs.select('/html/body//table[@class="infobox_v2"]//tr[contains(td, "Nacimiento")]/td[2]/a/text()').re('1[0-9][0-9][0-9]')
        fac = hxs.select('/html/body//table[@class="infobox_v2"]//tr[contains(td, "Fallecimiento")]/td[2]/a/text()').re('1[0-9][0-9][0-9]')

        self.log(foto)
        self.log(nombre)

        if ''.join(fac) != "" and ''.join(nac) != "" and foto:

            result = Event()
            result['title'] = ''.join(nombre)
            result['image'] = foto.pop()
            result['description'] = ''.join(desc)
            result['link'] = response.url
            result['start'] = ''.join(nac)
            result['end'] = ''.join(fac)


        return result

        #print event
        #return Presidente(nombre = nombre, foto = foto)

        #presi = Presidente()
        #presi['foto'] = [foto for foto in hxs.select('/html/body//table[@class="infobox_v2"]//tr/td/a/img/@src').re('//(.*)')]
        #presi['nombre'] = hxs.select('/html/body//table[@class="infobox_v2"]//tr[1]/th/span/text()')
        #nom_text = nom.extract()[0]
        #self.log('sin utf-8 %s' % nom_text)
        #self.log('utf-8 %s' % nom_text.encode('utf-8'))
        #presi['nombre'] = nom_text.encode('utf-8')
        #return presi

        
        
