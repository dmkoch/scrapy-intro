from scrapy.spider import BaseSpider

class CnnSpider(BaseSpider):
    name = 'cnn'
    allowed_domains = ['www.cnn.com']
    start_urls = [
        'http://www.cnn.com/',
    ]

    def parse(self, response):
        open('homepage.html', 'wb').write(response.body)
