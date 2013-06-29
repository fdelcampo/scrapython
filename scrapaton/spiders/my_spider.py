

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapaton.items import ScrapatonUrl, Presidente
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
        
        urls = hxs.select('/html/body//table[@class="wikitable"]//tr/td[1]//a/@href').extract()
        for i in urls:
            
            #yield ScrapatonUrl(name = "", url = i)
            #i = i.encode('utf-8')
            #self.log('http://es.wikipedia.org/%s' % i[1:])
            yield Request('http://es.wikipedia.org/%s' % i[1:], callback=self.parse_url)
        
        
    def parse_url(self, response):
        self.log('parse_presidente url: <%s>' % response.url)
        hxs = HtmlXPathSelector(response)
        presi = Presidente()
        presi['foto'] = hxs.select('/html/body//table[@class="infobox_v2"]//tr/td/a/img/@src').re('//(.*)')
        nom = hxs.select('/html/body//table[@class="infobox_v2"]//tr[1]/th/span/text()')
        nom_text = nom.extract()
        #self.log('sin utf-8 %s' % nom_text)
        #self.log('utf-8 %s' % nom_text.encode('utf-8'))
        presi['nombre'] = nom_text
        return presi
        
        
        
