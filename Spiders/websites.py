import datetime
import traceback
import ipdb
from collections import Iterable
from time import sleep
from urllib import parse

import scrapy
from scrapy import Request

import DataBase
from DataBase import items
from .urlparser import *
from DataBase import SQLite, MySQL
from items import Domaine

class WebSitesSpider(scrapy.Spider):
    name = "websites_spider"
    start_urls = []
    allowed_domains = []
    handle_httpstatus_list = [404,500]
    localdb = SQLite()
    total_rss_channels_links = []
    total_external_links = []

    def __init__(self,start_urls,total_external_links):
        self.start_urls = start_urls
        self.total_external_links = total_external_links
        self.setup_allowed_domains()
    def start_requests(self):
        try:
            print("START SCRAPING WEBSITES urls : ",self.start_urls)
            self.setup_allowed_domains()
            for url in self.start_urls:
                print("REQUESTING TO DOMAIN URL : ", url ," .........")
                yield scrapy.Request(url=url, callback=self.parse_website,dont_filter=True,encoding="UTF-8")
                sleep(5)
        except Exception :
            traceback.print_exc()

    def parse_website(self, response):
        website_domaine = getDomaine(response.url)
        websiteurl = getBaseUrl(response.url)
        if response.status in (404,500):
            self.update_collected_domains([websiteurl],status=4)
            print("---- DOMAIN NOT FOUND -> ",websiteurl)
            return None
        try:
            print("EXTRACTING DOMAIN INFO ....")

            domain = self.get_domain(response)
            website_rss_links = self.getWebSiteRssChannelsLinks(response)
            links = self.getWebSiteLinks(response)
            externalLinks = self.getExtrernalLinks(domaine=website_domaine,total_links=links)
            internalLinks = self.getWebSiteInternalLinks(domaine=website_domaine,total_links=links)
            #_________________
            print("-- SAVING EXTRACTED DOMAIN DATA ....")
            self.save_mysql_domains([domain])
            self.update_collected_domains([websiteurl],status=1)
            self.save_sqlite_external_links(externalLinks)
            self.save_sqlite_rss_channels(getBaseUrl(response.url),website_rss_links)
            #_________________
            if internalLinks == [] and externalLinks == [] and website_rss_links == []:
                self.update_collected_domains([websiteurl],status=3)
                return
            else:
                print("FETCHUING DOMAIN INTERNAL LINKS....")
                for internalLink in internalLinks:
                    if self.allowed_domains.count(getDomaine(internalLink)) == 0 :self.allowed_domains.append(getDomaine(internalLink))
                    yield Request(internalLink, callback=self.parse_internalwebsite, dont_filter=True,meta={"domain":domain},encoding="UTF-8")
                    sleep(2)
            self.update_collected_domains([websiteurl],status=2)
        except Exception :
            traceback.print_exc()

    def parse_internalwebsite(self,response):
        print("-- FETCHING AND SAVING DATA FOR INTERNAL LINK  ",response.url + " ......")
        try:
            domain = response.meta.get("domain")
            website_domaine = getDomaine(response.url)
            rss_channels_links = self.getWebSiteRssChannelsLinks(response)
            links = self.getWebSiteLinks(response)
            extrernalLinks = self.getExtrernalLinks(website_domaine,links)
            #________________
            self.save_sqlite_external_links(extrernalLinks)
            self.save_sqlite_rss_channels(domain.url,rss_channels_links)
            #________________
        except Exception :
            traceback.print_exc()


    def save_mysql_domains(self,domains):
        mysql = MySQL()
        mysql.insert_domains(domains)
        mysql.close()

    def save_sqlite_external_links(self, external_links):
        if external_links == []: return
        collected_domains = []
        for external_link in external_links:
            collected_domains.append(items.Domain(external_link))
        self.localdb.open()
        self.localdb.insert_collected_domains(collected_domains)
        self.localdb.close()

    def save_sqlite_rss_channels(self, domain,rss_channels_links:Iterable=[],):
        if rss_channels_links == []:return None
        rss_channels = []
        for rss_channel_link in rss_channels_links:
            rss_channels.append(items.RssChannel(rss_channel_link,domain))
        self.localdb.open()
        self.localdb.insert_rss_channels(rss_channels)
        self.localdb.close()
    def update_collected_domains(self, domainslinks,status:int=1,last_update:datetime=datetime.datetime.today()):
        args = []
        for domain in domainslinks:
            args.append(DataBase.items.Domain(domain=domain,last_update=last_update,state=status))
        self.localdb.open()
        self.localdb.update_collected_domains(args)
        self.localdb.close()


#___________________________ HELPERS ___________________________________________
    def getWebSiteRssChannelsLinks(self,response):
        rssChannelsLinksNodes = response.css("link[type='application/rss+xml']::attr('href')")
        filtratedRssChannelsLinks = []
        for rssChannelLinkNode in rssChannelsLinksNodes:
            rssChannelLink = rssChannelLinkNode.extract()
            if self.total_rss_channels_links.count(rssChannelLink) == 0 and getDomaine(response.url) == getDomaine(rssChannelLink):
                filtratedRssChannelsLinks.append(rssChannelLink)
                self.total_rss_channels_links.append(rssChannelLink)
        return filtratedRssChannelsLinks

    def getWebSiteLinks(self,response):
        linksNodes = response.css("body *[href^='https']::attr('href')")
        links = []
        for linkNode in linksNodes:
            link = linkNode.extract()
            if links.count(link) == 0: links.append(link)
        return links
    def getWebSiteInternalLinks(self,domaine,total_links:Iterable=[],response:None=None):
        if total_links is None:total_links = self.getWebSiteLinks(response)
        internal_links = []
        for link in total_links:
            if internal_links.count(link) == 0 and getDomaine(link) == domaine and domaine != link:internal_links.append(link)
        return internal_links[0:10]
    def getExtrernalLinks(self,domaine,total_links:Iterable=[],response:None=None):
        if total_links is None:total_links = self.getWebSiteLinks(response)
        external_links = []
        for link in total_links:
            if external_links.count(getBaseUrl(link)) == 0 and self.total_external_links.count(getBaseUrl(link)) == 0 and getDomaine(link) != domaine:
                external_links.append(getBaseUrl(link))
                self.total_external_links.append(getBaseUrl(link))
        return external_links
    def get_domain(self, response):
        websiteName = self.select_css(response,"meta[name='application-name']::attr('content')")
        websiteType = self.select_css(response,"meta[property='og:type']::attr('content')")
        websiteImage = self.select_css(response,"meta[property='og:image']::attr('content')")
        websiteKeyWords = self.select_css(response,"meta[name='keywords']::attr('content')")
        websiteIconUrl = self.select_css(response,"link[rel='shortcut icon']::attr('href')")
        websiteLanguage = self.select_css(response,"meta[itemprop='inLanguage']::attr('content')")
        websiteRobots = self.select_css(response,"meta[name='robots']::attr('content')")
        websiteStartUrl = self.select_css(response,"meta[name='msapplication-starturl']::attr('content')")



        websiteDescription = self.select_css(response,"meta[name='description']::attr('content')")
        if websiteDescription == "":websiteDescription =self.select_css(response,"meta[property='og:description']::attr('content')")

        websiteTitle = self.select_css(response,"meta[property='og:title']::attr('content')")
        if websiteTitle == "":websiteTitle = self.select_css(response,"title::text")

        return Domaine(url=getBaseUrl(response.url),name=websiteName,description=websiteDescription,roletype=websiteType,title=websiteTitle,image=websiteImage,keywords=websiteKeyWords,language=websiteLanguage,robots=websiteRobots,icon=websiteIconUrl,starturl=websiteStartUrl)
    def select_css(self, selector, css):
        node = selector.css(css)
        if node:
            return node.extract_first()
        else:
            return ""

    def setup_allowed_domains(self,urls:Iterable=None):
        if urls is None:urls = self.start_urls
        self.allowed_domains.clear()
        for url in urls:
            self.allowed_domains.append(str(parse.urlparse(url).hostname))

