# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ScrapatonItem(Item):
    # define the fields for your item here like:
    # name = Field()
    nombre = Field()
    inicio = Field()
    termino = Field()
    url = Field()
    pass

class ScrapatonUrl(Item):
    name = Field()
    url = Field()
    pass
    
class Presidente(Item):
    nombre = Field()
    foto = Field()
