# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Webpage(scrapy.Item):
    spider_name = scrapy.Field()
    spider_version = scrapy.Field()
    timestamp = scrapy.Field()
    url = scrapy.Field()
    url_hash = scrapy.Field()
    page_title = scrapy.Field()
    html_output_path = scrapy.Field()
    html_hash = scrapy.Field()
    internal_urls = scrapy.Field()
    external_urls = scrapy.Field()
    request_headers = scrapy.Field()
    response_headers = scrapy.Field()