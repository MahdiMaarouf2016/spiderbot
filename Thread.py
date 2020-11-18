"""
import requests
from Spiders import urlparser
from DataBase import SQLite
tab = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print(tab[0:30])
exit(1)
websies = ["nytimes.com","facebook.com","feedpier.com"]
sqlite = SQLite()
sqlite.open()
#sqlite.addWebSites(websies)
sqlite.deleteWebsites(websies)
sqlite.close()
exit(1)


url =  "https://saverestaurants.us19.list-manage.com/track/click?u=ac1f1b55c391bdcb421965ac2&id=f4a9c4a508&e=96529e08c6"
print(urlparser.getDomaine(url))

exit(1)
res = requests.get("https://www.nytimes.com/2020/04/29/us/coronavirus-usa-cases-deaths.html")
with open("./tarsh.html","w",encoding="UTF-8",errors="ingiore" ) as file:
    file.write(res.text)


"""

import threading

from scrapy.crawler import CrawlerProcess

from Spiders import WebSitesSpider


class SpiderRunner(threading.Thread):
    spider = None

    def __init__(self, spider):
        self.spider = spider
        threading.Thread.__init__(self)

    def run(self):
        print("START THREAD")
        crawlProcess = CrawlerProcess()
        crawlProcess.crawl(self.spider, self.spider.start_urls)
        # self.spider.start_requests()
        crawlProcess.start(stop_after_crawl=True)
        print("END TRHEAD", self.spider.total_rss_channels_links, self.spider.total_external_links)


url = ""
print("START")
spider = WebSitesSpider(start_urls=[],total_external_links=[])
sr = SpiderRunner(spider)
sr.start()
print("END", spider.total_rss_channels_links, spider.total_external_links)
