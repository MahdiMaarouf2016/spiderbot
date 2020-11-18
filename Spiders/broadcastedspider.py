import scrapy
from .websites import WebSitesSpider
from .rsschannels import RssChannelsSpider


class BroadCastedSpider(WebSitesSpider, RssChannelsSpider):
    name = "broadcast_spider"

    def __init__(self):
        WebSitesSpider.__init__(self)

    def start_requests(self):
        WebSitesSpider.start_requests(self)
        RssChannelsSpider.__init__(WebSitesSpider.total_rss_channels_links)
        RssChannelsSpider.start_requests(self)
