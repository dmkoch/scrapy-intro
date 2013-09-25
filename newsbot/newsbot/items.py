# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    url = Field()
    source = Field()
    headline = Field()
    byline = Field()
    article = Field()
