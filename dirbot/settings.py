# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = [
    'dirbot.pipelines.RequiredFieldsPipeline',
    'dirbot.pipelines.FilterWordsPipeline',
    'dirbot.pipelines.MySQLStorePipeline',
]

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'dirbot'
MYSQL_USER = 'dirbot'
MYSQL_PASSWD = ''
