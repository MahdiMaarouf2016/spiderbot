import unittest
import scrapy


from DataBase import SQLite,items
from Spiders import WebSitesSpider, getDomaine, getBaseUrl
from items import Domaine


class websites_spider_test(unittest.TestCase):
    def test_openlocaldb(self):
        s = SQLite("../../Storage/localdb.db")
        self.assertNotEqual(s.connexion,None,"FAILED OPEN DB")

    def test_init_spider(self):
        s = WebSitesSpider(start_urls=["https://test.com"],total_external_links=["https://test.com"])
        self.assertEqual(s.allowed_domains,["test.com"])
    def test_parsewebsite(self):
        with open("./test_storage/domain.html","r",encoding="UTF-8" ,errors="igniore") as html:
            db = SQLite("../../Storage/localdb.db")
            html = html.read()
            response = scrapy.http.HtmlResponse(url="https://nytimes.com",status=200,body=html,encoding="UTF-8")
            s = WebSitesSpider(start_urls=["https://nytimes.com"],total_external_links=["https://nytimes.com"])
            s.localdb = db

            website_domaine = getDomaine(response.url)
            domain = s.get_domain(response)
            website_rss_links = s.getWebSiteRssChannelsLinks(response)
            links = s.getWebSiteLinks(response)
            externalLinks = s.getExtrernalLinks(domaine=website_domaine,total_links=links)
            internalLinks = s.getWebSiteInternalLinks(domaine=website_domaine,total_links=links)
            #_________________
            #s.save_mysql_domains([domain])
            s.update_collected_domains([getBaseUrl(response.url)])
            #s.save_sqlite_external_links(externalLinks)
            #s.save_sqlite_rss_channels(website_domaine,website_rss_links)

            #print("DOMAIN SCRAPED DATA : ",{"infos":domain._object(),"rsslinks":website_rss_links,"internalLinks":internalLinks,"externalLinks":externalLinks})
            #_________________
            print("info", {"infos":domain._object(),"rsslinks":website_rss_links,"internalLinks":internalLinks,"externalLinks":externalLinks})


    def test_parse_internalwebsite(self):
        with open("./test_storage/internal.html","r",encoding="UTF-8" ,errors="igniore") as html:
            db = SQLite("../../Storage/localdb.db")
            html = html.read()
            response = scrapy.http.HtmlResponse(url="https://www.nytimes.com/section/politics",status=200,body=html,encoding="UTF-8")
            s = WebSitesSpider(start_urls=["https://nytimes.com"],total_external_links=["https://nytimes.com"])
            s.localdb = db

            domain = "nytimes.com"
            website_domaine = getDomaine(response.url)
            rss_channels_links = s.getWebSiteRssChannelsLinks(response)
            links = s.getWebSiteLinks(response)
            extrernalLinks = s.getExtrernalLinks(website_domaine,links)
            #________________
            s.save_sqlite_external_links(extrernalLinks)
            s.save_sqlite_rss_channels(domain,rss_channels_links)
            print("INERNAL WEBISTE SCRAPE DATA : ",{"domaine":website_domaine,"url":response.url,"rsschannelslinks":rss_channels_links,"externalLinks":extrernalLinks,"containerwebsiteinfoDOAMIN":domain})
            #________________


if __name__ == "__main__":
    unittest.main()