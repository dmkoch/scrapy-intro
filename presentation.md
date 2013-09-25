title: "Introduction to Scrapy"
author:
    name: "Dan Koch"
    url: "https://github.com/dmkoch/scrapy-intro"
    twitter: "@dkoch"
output: build/presentation.html

--

# Scrapy 101
## Crawling the web for fun and profit

--

### Obligatory meme

![Spider cat](spidercat.jpg)


--

### Crawling the web

*Not so hard, right?*

    curl http://www.cnn.com/


--

### Crawling with Python

    #!/usr/bin/env python
    import requests

    r = requests.get('http://www.cnn.com/')
    print r.content

*Then what?*

--

### Crawling is *Hard*

* Inconsistent markup
* Unstructured data
* Error handling
* Selecting URLs to crawl
* Content freshness
* Duplicate content
* URL normalization
* Politeness
* Parallelization / distributed crawling

--

### What is Scrapy?
* http://scrapy.org/
* Framework for building web crawlers
* Extracts structured data from unstructured web pages
* Inspired by Django
* Enables developers to focus on the rules to extract the data they want
* Does the hard parts of crawling
* Fast event-driven code based on Twisted

--

### Features and benefits

* Selecting and extracting data from HTML
* Reusable filters for cleaning and sanitizing
* Export formats: JSON, CSV, XML
* Automatic image downloading
* Pluggable extension API
* Text encoding auto-detection
* Template system from creating spiders
* Statistics and spider performance monitoring

--

### Features and benefits

* Interactive console for testing scrapers
* Production-quality service daemon for spider deployment
* Web service for controlling your bots
* Telnet console for live debugging
* Logging
* Sitemap URL discovery
* DNS caching

--

### Middleware

* Cookies and sessions
* HTTP compression
* HTTP authentication
* HTTP cache
* User-agent spoofing
* robots.txt handling
* Crawl depth control

--
### Installation

    pip install Scrapy

--

### Project scaffolding

Create a project called *newsbot*:

    scrapy startproject newsbot


--

### Project layout

    newsbot/
        scrapy.cfg
        newsbot/
            __init__.py
            items.py
            pipelines.py
            settings.py
            spiders/
                __init__.py


--

### Define what to scrape

    # items.py
    from scrapy.item import Item, Field

    class ArticleItem(Item):
        url = Field()
        source = Field()
        headline = Field()
        byline = Field()
        article = Field()

--

### Create a spider for each site

Download the CNN homepage:

    # spiders/cnn_spider.py
    from scrapy.spider import BaseSpider

    class CnnHomepageSpider(BaseSpider):
        name = 'cnn_homepage'
        allowed_domains = ['www.cnn.com']
        start_urls = ['http://www.cnn.com/',]

        def parse(self, response):
            open('homepage.html', 'wb').write(response.body)

--

### Run a spider

    cd newsbot
    scrapy crawl cnn_homepage


    2013-09-24 18:40:01-0700 [scrapy] INFO: Scrapy 0.18.2 started (bot: newsbot)
        ...
    2013-09-24 18:40:01-0700 [cnn] DEBUG: Crawled (200) <GET http://www.cnn.com/> (referer: None)
    2013-09-24 18:40:01-0700 [cnn] INFO: Closing spider (finished)
    2013-09-24 18:40:01-0700 [cnn] INFO: Dumping Scrapy stats:
        {'downloader/request_bytes': 217,
         'downloader/request_count': 1,
         'downloader/request_method_count/GET': 1,
         'downloader/response_bytes': 28916,
         'downloader/response_count': 1,
         'downloader/response_status_count/200': 1,
         'finish_reason': 'finished',
        ...

--

### More useful spider that crawls

    from scrapy.contrib.spiders import CrawlSpider, Rule
    from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
    from scrapy.selector import HtmlXPathSelector
    from ..items import ArticleItem

    class CnnSpider(CrawlSpider):
        ...
        start_urls = ['http://www.cnn.com/',]

        rules = [
            Rule(SgmlLinkExtractor(
                    allow=[r'/\d{4}/\d{2}/\d{2}/[^/]+/[^/]+/index.html']),
                    callback='parse_item'),
        ]

        def parse_item(self, response):
            ...

--

### Parsing items (articles)

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

--

### Pipelines

Shared across all spiders, processes each item after it is parsed from web page

    from scrapy.exceptions import DropItem

    class MissingFieldsPipeline(object):
        def process_item(self, item, spider):
            for field in ('headline', 'url', 'article'):
                print field
                if not item.get(field, False):
                    raise DropItem("Missing '%s' in %s" % (field, item))

            return item

--

### Settings

    # Crawl responsibly by identifying yourself (and your website)
    # on the user-agent
    USER_AGENT = 'newsbot (+http://www.meetup.com/python-charlotte/)'

    # Run every item through these pipelines
    ITEM_PIPELINES = [
        'newsbot.pipelines.MissingFieldsPipeline',
    ]

    # Crawl politely
    CONCURRENT_REQUESTS_PER_DOMAIN = 2
    DOWNLOAD_DELAY = 2.0
    RANDOMIZE_DOWNLOAD_DELAY = True

--

### Saving items

    scrapy crawl cnn -o articles.json


--

### Related projects

#### scrapyd
[https://github.com/scrapy/scrapyd](https://github.com/scrapy/scrapyd)

* Daemon for running spiders in production
* Web service interface for scheduling crawls

--

### Related projects

#### scrapely
[https://github.com/scrapy/scrapely](https://github.com/scrapy/scrapely)

* Screen scraping library
* Train a scraper once, automatically extracts same data from similar pages
* No hand-written XPath

--

### Scrapely example

    from scrapely import Scraper
    scraper = Scraper()

    # Train scraper with an article
    url1 = ('http://www.cnn.com/2013/09/06/us/nsa-surveillance-encryption'
            '/index.html')
    data = {'headline': 'Reports: NSA has cracked much online encryption',
            'byline': 'Peter Wilkinson and Laura Smith-Spark'}
    scraper.train(url1, data)

    # Use it to extract same fields from another article
    url2 = ('http://www.cnn.com/2013/09/25/world/asia/pakistan-earthquake'
            '/index.html')
    scraper.scrape(url2)


--

### Related projects

#### Beautiful Soup
[http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/)

* Alternative to Scrapy's XPath selector
* More "Pythonic"

--

### Related projects

#### slybot
[https://github.com/scrapy/slybot](https://github.com/scrapy/slybot)

* Complete web crawler written on top of scrapy and scrapely
