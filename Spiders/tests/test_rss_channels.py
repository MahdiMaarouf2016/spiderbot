import ipdb
import unittest
import scrapy
from DataBase import SQLite, MySQL
from DataBase.items import RssChannel
from Spiders import RssChannelsSpider, getDomaine, getBaseUrl


class rss_channel_spiderTest(unittest.TestCase):
    def test_spider_init(self):
        rsch = RssChannel("https://www.nytimes.com/HomePage.xml","nytimes.com")
        spider = RssChannelsSpider([rsch])
        self.assertEqual([rsch],spider.start_rss_channels,"START CHANNELS NOT INITIALIZED FOR THE SPIDER")
        self.assertEqual(["nytimes.com"],spider.allowed_domains,"DOMAINS NOT INTISIALIZED FOR THE SPIDER")
        self.assertEqual(["https://www.nytimes.com/HomePage.xml"],spider.start_urls,"START URLS NOT INITIALISED FOR THE SPIDER")
    def test_spider_parse_channel(self):
        rsch = RssChannel("https://www.nytimes.com/HomePage.xml","nytimes.com")
        spider = RssChannelsSpider([rsch])

        with open("./test_storage/rsscases.xml","r",encoding="UTF-8",errors="igniore") as file:
            xml = file.read()
            response = scrapy.http.XmlResponse(url="https://www.nytimes.com/HomePage.xml",body=xml,status=200,encoding="UTF-8")
            spider.register_name_spaces(response=response)
            channel = spider.get_channel(response)
            channel_feeds_items_nodes = response.css("channel item")
            channel_feeds = []
            for channel_feed_item_node in channel_feeds_items_nodes: channel_feeds.append(
                spider.get_feed(channel_feed_item_node, channel=channel.url))
            spider.total_channels_feeds.append(channel_feeds)
            # ___________________________________________________
            mySql = MySQL()
            #mySql.insert_rss_channels([channel])
            mySql.insert_rss_feeds(channel_feeds)
#__________________ END ORIGINAL CODE _______________________
            print("CHANNEL : ",channel._object())
            for feed in channel_feeds:
                print("\n==>",feed._object())

    def test_external_feed_link(self):
        rsch = RssChannel("https://www.nytimes.com/HomePage.xml","nytimes.com")
        s = SQLite("../../Storage/localdb.db")
        spider = RssChannelsSpider([rsch])
        spider.localdb = s
        spider.allowed_domains = ["nytimes.com","facebook.com","nytco.com","nytmediakit.com","twitter.com"]
        with open("./test_storage/external.html","r",encoding="UTF-8",errors="igniore") as file:
            html = file.read()
            response = scrapy.http.XmlResponse(url="https://www.nytimes.com/2020/04/29/opinion/coronavirus-vaccine.html",body=html,status=200,encoding="UTF-8")
            links_nodes = response.css("body *[href^='https']::attr('href')")
            feeds_externalLinks = []
            for link_node in links_nodes:
                link = link_node.extract()
                if spider.allowed_domains.count(getDomaine(link)) == 0 and feeds_externalLinks.count(
                        getBaseUrl(link)) == 0 and spider.total_feeds_externalLinks.count(getBaseUrl(link)) == 0:
                    feeds_externalLinks.append(getBaseUrl(link))
                    spider.total_feeds_externalLinks.append(getBaseUrl(link))
            print(feeds_externalLinks)
        spider.save_sqlite_external_links(feeds_externalLinks)


if __name__ == "__main__":
    unittest.main()