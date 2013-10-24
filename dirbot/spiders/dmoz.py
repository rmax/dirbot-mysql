from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from dirbot.items import WebsiteLoader


class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul[@class="directory-url"]/li')

        for site in sites:
            il = WebsiteLoader(response=response, selector=site)
            il.add_xpath('name', 'a/text()')
            il.add_xpath('url', 'a/@href')
            il.add_xpath('description', 'text()', re='-\s([^\n]*?)\\n')
            yield il.load_item()
