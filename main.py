from Spiders import WebSitesSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

settings1 = Settings()
settings1.set("USER_AGENT","Chrome/43.0.2357.134 Safari/537.36")
settings1.set("LOG_ENABLED",False)
settings1.set("ROBOTSTXT_OBEY",True)
settings2 = Settings()
settings2.set("USER_AGENT","Chrome/43.0.2357.134 Safari/537.36")
settings2.set("LOG_ENABLED",True)
settings2.set("ROBOTSTXT_OBEY",True)

url = "http://127.0.0.1:8000/nytimes.htm"

def run_spider(spider,settings):
    crawlProcess = CrawlerProcess(settings)
    crawlProcess.crawl(spider,spider.start_urls)
    return crawlProcess.start(stop_after_crawl=True)

print("START PROCSS")
spider = WebSitesSpider(start_urls=[],total_external_links=[""])
run_spider(spider,settings2)
print("END PROCESS")





"""
settings.set("SPIDER_MIDDLEWARES", {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware':True,
    'scrapy.extensions.closespider.CloseSpider':True
})
"""
"""
print("**1")
websiteCrawlerProcess = CrawlerProcess(settings1)
webSitesSpider = WebSitesSpider(start_urls=[url],onrssfound=rssFound)
websiteCrawlerProcess.crawl(webSitesSpider,webSitesSpider.start_urls)
websiteCrawlerProcess.start()
websiteCrawlerProcess.stop()
print("**2")
print("resularts from object",webSitesSpider.rss_found)
print("**3")
exit(1)
rssCrawlerProcess = Crawler(settings2)
rssCrawlerProcess.crawlers = []
rsspider = RssSpider(start_urls=webSitesSpider.rss_found)
rssCrawlerProcess.crawl(rsspider,rsspider.start_urls)
rssCrawlerProcess.start()
print("**4")

"""
"""
prcess = CrawlerProcess(settings2)
webSitesSpider = WebSitesSpider(start_urls=[url])
rsspider = RssSpider(start_urls=["http://127.0.0.1:8000/HomePage.xml"])

prcess.crawl(webSitesSpider)
prcess.crawl(rsspider)
prcess.start()
"""
"""

#url = "https://nytimes.com"
print("START")
runner = CrawlerRunner(settings2)
webSitesSpider = WebSitesSpider(start_urls=[url])
runner.crawl(webSitesSpider)
runner.join()
reactor.run()
"""

"""
https://www.programcreek.com/python/example/86476/scrapy.crawler.CrawlerProcess
"""

#["https://nytimes.com/"]
#USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4)","AppleWebKit/537.36 (KHTML, like Gecko)"," Chrome/43.0.2357.134 Safari/537.36"
#settings.set("DOWNLOAD_TIMEOUT",1000)
#settings.set("DOWNLOAD_DELAY",0.25)
#settings.set("HTTPCACHE_ENABLED",False)
#settings.set("REDIRECT_ENABLED",False)
#https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
#rss_found("http://127.0.0.1:8000/HomePage.xml")
