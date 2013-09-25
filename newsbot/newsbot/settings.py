# Scrapy settings for newsbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'newsbot'

SPIDER_MODULES = ['newsbot.spiders']
NEWSPIDER_MODULE = 'newsbot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'newsbot (+http://www.meetup.com/python-charlotte/)'

# Run every item through these pipelines
ITEM_PIPELINES = [
    'newsbot.pipelines.MissingFieldsPipeline',
]

# Crawl politely
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 2.0
RANDOMIZE_DOWNLOAD_DELAY = True
