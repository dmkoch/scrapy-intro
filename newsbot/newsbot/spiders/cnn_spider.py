from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from ..items import ArticleItem


class CnnSpider(CrawlSpider):
    name = 'cnn'
    allowed_domains = ['www.cnn.com']
    start_urls = [
        'http://www.cnn.com/',
    ]

    rules = [
        Rule(SgmlLinkExtractor(allow=[r'/\d{4}/\d{2}/\d{2}/[^/]+/[^/]+/index.html']),
             callback='parse_item'),
    ]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        article = ArticleItem()
        article['url'] = response.url
        article['source'] = self.name
        article['headline'] = hxs.select(
            '//*[@id="cnnContentContainer"]/h1[1]/text()').extract()
        article['byline'] = hxs.select(
            '//*[@id="cnnContentContainer"]//div[@class="cnnByline"]'
            '//text()').extract()
        article['article'] = hxs.select(
            '//*[@id="cnnContentContainer"]//p//text()').extract()
        return article
