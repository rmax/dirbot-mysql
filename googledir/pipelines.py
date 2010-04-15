from scrapy import log
from scrapy.core.exceptions import DropItem
from twisted.enterprise import adbapi

import time
import MySQLdb.cursors

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, spider, item):
        print spider
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

class MySQLStorePipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db='googledir',
                user='root',
                passwd='',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, spider, item):
        # defered call to check if record already exists
        query = self.dbpool.runQuery(\
                "select * from sites where url = %s", (item['url'][0], ))
        query.addCallback(self.conditional_insert(item))
        query.addErrback(self.handle_error)

        return item

    def conditional_insert(self, item):
        """Returns defered callback to insert item only if record not
        exists"""

        def callback(results):
            if results:
                log.msg("Item already stored in db: %s" % item)
            else:
                now = time.time()
                query = self.dbpool.runQuery(\
                    "insert into sites (name, url, description, created) "
                    "values (%s, %s, %s, %s)",
                    (item['name'][0],
                     item['url'][0],
                     item['description'][0],
                     now)
                )
                query.addCallback(lambda r: log.msg(\
                        "Item stored: %s" % item['name'][0]))
                query.addErrback(self.handle_error)

        return callback

    def handle_error(self, e):
        log.err(e)

    
