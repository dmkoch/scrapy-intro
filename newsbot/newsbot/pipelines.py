# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class MissingFieldsPipeline(object):
    def process_item(self, item, spider):
        for field in ('headline', 'url', 'article'):
            print field
            if not item.get(field, False):
                raise DropItem("Missing '%s' in %s" % (field, item))

        return item
