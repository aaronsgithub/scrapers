import hashlib
import pathlib
import sys

import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors import LinkExtractor
from scrapers.items import Webpage
from scrapers.settings import DATA_DIR


class IndexWebsiteSpider(Spider):
    """Basic indexing of a website.

    It will visit all internal urls it can find and download http response body of each page.
    (Usually this is the website html, but depends on the response content-type.)
    It will also store some data about that page in a jsonlines log file.

    Usage:
    scrapy crawl indexwebsite -a url <root-url-of-website>

    It is important to give the spider the root url as opposed to any subdomain
    as this spider will use the root url to determine what internal urls it can visit.

    See the spider README.md for full details.
    """

    name = "indexer"
    version = "0.1"

    # this is a hack, see:
    # https://github.com/scrapy/scrapy/issues/3663
    for arg in sys.argv:
        if "url=" in arg:
            url = arg.strip("url=")
            custom_settings = {
                "FEEDS": {
                    pathlib.Path(DATA_DIR)
                    / f"{url}"
                    / f"{url}.jsonl": {"format": "jsonlines"}
                }
            }

    def __init__(self, url=None, *args, **kwargs):
        super(IndexWebsiteSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.start_urls = [f"https://{url}"]
        self.allowed_domains = [f"{url}"]
        self.url_data_directory = pathlib.Path(DATA_DIR) / url
        self.url_data_directory.mkdir(parents=True, exist_ok=True)

    def parse(self, response):
        # gather data
        w = Webpage()
        w["spider_name"] = self.name
        w["spider_version"] = self.version
        w["timestamp"] = response.request.timestamp.isoformat()
        w["url"] = response.url
        w["url_hash"] = hashlib.md5(bytes(response.url, "ascii")).hexdigest()
        w["page_title"] = response.css("title::text").get()
        w["html_hash"] = hashlib.md5(response.body).hexdigest()
        internal_urls = LinkExtractor(allow_domains=self.allowed_domains).extract_links(
            response
        )
        w["internal_urls"] = [link.url for link in internal_urls]
        external_urls = LinkExtractor(deny_domains=self.allowed_domains).extract_links(
            response
        )
        w["external_urls"] = [link.url for link in external_urls]
        w["request_headers"] = response.request.headers.to_unicode_dict()
        w["response_headers"] = response.headers.to_unicode_dict()

        # save data log file defined by FEEDs in custom_settings
        yield w

        # save html response body
        page_data_directory = self.url_data_directory / f"{w['url_hash']}"
        page_data_directory.mkdir(parents=True, exist_ok=True)
        html_output_file = page_data_directory / f'{w["html_hash"]}.html'

        with open(html_output_file, "wb") as f:
            f.write(response.body)

        # crawl internal links
        for link in internal_urls:
            yield scrapy.Request(url=link.url)
