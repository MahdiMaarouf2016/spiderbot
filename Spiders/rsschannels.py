import json
import scrapy
import traceback
import email.utils
from time import sleep
from collections import Iterable
from DataBase import SQLite, MySQL, datetime
from items import RssChannel, RssFeed
import DataBase.items
from .urlparser import *


class RssChannelsSpider(scrapy.Spider):
    name = "rsschannels_spider"
    start_urls = []
    allowed_domains = []

    localdb = SQLite()
    total_channels_feeds = []
    total_feeds_externalLinks = []
    start_rss_channels = []

    def __init__(self, start_rss_channels,total_feeds_externalLinks):
        self.total_feeds_externalLinks = total_feeds_externalLinks
        self.setup_start_urls(start_rss_channels)
        self.setup_allowed_domains()

    def start_requests(self):
        try:
            print("START RSS CHANNELS SCRAPING urls : ", self.start_urls)
            self.setup_allowed_domains()
            for rss_channel in self.start_rss_channels:
                print("REQUESTING TO CAHHENL URL : ", rss_channel.url ," .........")
                yield scrapy.Request(url=rss_channel.url, callback=self.parse_rss_channel,
                                     meta={"domain": rss_channel.domain},encoding="UTF-8")
        except Exception:
            traceback.print_exc()

    def parse_rss_channel(self, response):
        try:
            print("EXTRACTING CHANNEL INFO FOR ",response.url ," .......")
            self.register_name_spaces(response=response)
            channel = self.get_channel(response)
            channel_feeds_items_nodes = response.css("channel item")
            channel_feeds = []
            for channel_feed_item_node in channel_feeds_items_nodes: channel_feeds.append(
                self.get_feed(channel_feed_item_node, channel=channel.url))
            self.total_channels_feeds.append(channel_feeds)
            # ___________________________________________________
            mySql = MySQL()
            mySql.insert_rss_channels([channel])
            mySql.insert_rss_feeds(channel_feeds)
            print("-- SAVING CHANNEL INFO for ",response.url ," .....")
            # ___________________________________________________
            print("FETCHING EXTERNAL FEEDS LINKS ....")
            for feed in channel_feeds:
                if self.allowed_domains.count(getDomaine(feed.link)) == 0: self.allowed_domains.append(
                    getDomaine(feed.link))
                yield scrapy.Request(feed.link, callback=self.parse_websitepage_feed, dont_filter=True,encoding="UTF-8")
                sleep(2)

        except Exception:
            traceback.print_exc()

    def parse_websitepage_feed(self, response):
        print("FETCHING AND SAVING FEED LINK DATA ....")
        feeds_externalLinks = []
        try:
            links_nodes = response.css("body *[href^='https']::attr('href')")
            for link_node in links_nodes:
                link = link_node.extract()
                if self.allowed_domains.count(getDomaine(link)) == 0 and feeds_externalLinks.count(
                        getBaseUrl(link)) == 0 and self.total_feeds_externalLinks.count(getBaseUrl(link)) == 0:
                    feeds_externalLinks.append(getBaseUrl(link))
                    self.total_feeds_externalLinks.append(getBaseUrl(link))
            self.save_sqlite_external_links(feeds_externalLinks)

        except Exception:
            traceback.print_exc()
            self.save_sqlite_external_links(feeds_externalLinks)

    def save_sqlite_external_links(self, external_links):
        if external_links == []: return
        collected_domains = []
        for external_link in external_links:
            collected_domains.append(DataBase.items.Domain(external_link))
        self.localdb.open()
        self.localdb.insert_collected_domains(collected_domains)
        self.localdb.close()

    # ______________________________ HELPERS ________________________________
    def get_feed(self, selector, channel):
        feed_title = self.select_css(selector, "title::text")
        feed_link = self.select_css(selector, "link::text")
        feed_description = self.select_css(selector, "description::text")
        feed_author = self.select_css(selector, "author::text")
        feed_comments = self.select_css(selector, "comments::text")
        feed_slash_comments = self.select_css(selector, "slash|comments::text", expectedtype=int)
        # ERROR IS HERE print("feed_slash_comments",selector.css("slash|comments").extract_first())
        feed_creativeCommons_nodes = selector.css("creativeCommons|license")
        feed_creativeCommons = []

        if feed_creativeCommons_nodes:
            for feed_creativeCommon_node in feed_creativeCommons_nodes:
                feed_creativeCommons.append(self.select_css(feed_creativeCommon_node, "::text"))
        feed_pubdate = self.select_css(selector, "pubDate::text")
        if feed_pubdate == "":
            feed_pubdate = datetime.datetime.today()
        else:
            feed_pubdate = email.utils.parsedate_to_datetime(feed_pubdate)
        feed_guid_node = selector.css("guid")
        feed_guid = {}
        if feed_guid_node: feed_guid = {"guid": self.select_css(feed_guid_node, "::text"),
                                        "isPermaLink": self.select_css(feed_guid_node, "::attr('isPermaLink')")}
        feed_source_node = selector.css("source")
        feed_source = {}
        if feed_source_node: feed_source = {"url": self.select_css(feed_source_node, "::attr('url')"),
                                            "source": self.select_css(feed_source_node, "::text")}
        feed_enclosure_node = selector.css("enclosure")
        feed_enclosure = {"length": self.select_css(feed_enclosure_node, "::attr('length')"),
                          "type": self.select_css(selector, "::attr('type')"),
                          "url": self.select_css(selector, "::attr('url')")}
        feed_categories_nodes = selector.css("category")
        feed_categories = []
        for feed_categorie_node in feed_categories_nodes: feed_categories.append(
            {"categorie": self.select_css(feed_categorie_node, "::text"),
             "domain": self.select_css(feed_categorie_node, "::attr('domain')")})
        feed_atome = {}
        feed_atome_node = selector.css("atome|link")
        if feed_atome_node: feed_atome = {"href": self.select_css(feed_atome_node, "::attr('href')"),
                                          "type": self.select_css(feed_atome_node, "::attr('type ')"),
                                          "title": self.select_css(feed_atome_node, "::attr('title')"),
                                          "hreflang": self.select_css(feed_atome_node, "::attr('hreflang')"),
                                          "length": self.select_css(feed_atome_node, "::attr('length')"),
                                          "rel": self.select_css(feed_atome_node, "::attr('rel')")}
        dc_creators_nodes = selector.css("dc|creator")
        dc_creators = []
        for dc_creator_node in dc_creators_nodes:
            dc_creators.append(dc_creator_node.css("::text").extract_first())
        media_content_node = selector.css("media|content")
        media_content = {}
        if media_content_node: media_content = {"url": self.select_css(media_content_node, "::attr('url')"),
                                                "fileSize": self.select_css(media_content_node, "::attr('fileSize')",
                                                                            expectedtype=int),
                                                "type": self.select_css(media_content_node, "::attr('type')"),
                                                "medium": self.select_css(media_content_node, "::attr('medium')"),
                                                "isDefault": self.select_css(media_content_node, "::attr('isDefault')",
                                                                             expectedtype=bool),
                                                "expression": self.select_css(media_content_node,
                                                                              "::attr('expression')"),
                                                "bitrate": self.select_css(media_content_node, "::attr('bitrate')",
                                                                           expectedtype=int),
                                                "framerate": self.select_css(media_content_node, "::attr('framerate')",
                                                                             expectedtype=int),
                                                "samplingrate": self.select_css(media_content_node,
                                                                                "::attr('samplingrate')",
                                                                                expectedtype=float),
                                                "channels": self.select_css(media_content_node, "::attr('channels')",
                                                                            expectedtype=int),
                                                "duration": self.select_css(media_content_node, "::attr('duration')",
                                                                            expectedtype=int),
                                                "height": self.select_css(media_content_node, "::attr('height')",
                                                                          expectedtype=int),
                                                "width": self.select_css(media_content_node, "::attr('width')",
                                                                         expectedtype=int),
                                                "lang": self.select_css(media_content_node, "::attr('lang')")
                                                }

        media_rating_nodes, media_title_node, media_description_node, media_keywords_node, media_thumbnails_node, media_category_node, \
        media_hash_node, media_player_node, media_credit_node, media_copyright_node, media_text_node, media_restriction_node, \
        media_community_node, media_comments_node, media_embed_node, media_responses_node, media_backLinks_node, media_status_node, \
        media_price_node, media_license_node, media_subTitle_node, media_peerLink_node, media_rights_node, media_scenes_node = \
            selector.css("media|rating"), selector.css("media|title"), selector.css("media|description"), \
            selector.css("media|keywords"), selector.css("media|thumbnail"), selector.css("media|category"), \
            selector.css("media|hash"), selector.css("media|player"), selector.css("media|credit"), \
            selector.css("media|copyright"), selector.css("media|text"), selector.css("media|restriction"), \
            selector.css("media|community"), selector.css("media|comments"), selector.css("media|embed"), \
            selector.css("media|responses"), selector.css("media|backLinks"), selector.css("media|status"), \
            selector.css("media|price"), selector.css("media|license"), selector.css("media|subTitle"), \
            selector.css("media|peerLink"), selector.css("media|rights"), selector.css("media|scenes")
        media_rating, media_title, media_description, media_keywords, media_thumbnails, media_category, media_hash, media_player, media_credit, media_copyright, media_text, media_restriction, media_community, media_comments, media_embed, media_responses, media_backLinks, media_status, media_price, media_license, media_subTitle, media_peerLink, media_rights, media_scenes = [], {}, {}, [], {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, [], [], {}, {}, {}, {}, {}, {}, []
        if media_rating_nodes:
            for media_rating_node in media_rating_nodes:
                media_rating.append({"scheme": self.select_css(media_rating_node, "::attr('scheme')"),
                                     "rating": self.select_css(media_rating_node, "::text")})
        if media_title_node: media_title = {"type": self.select_css(media_title_node, "::attr('type')"),
                                            "title": self.select_css(media_title_node, "::text")}
        if media_description_node: media_description = {
            "type": self.select_css(media_description_node, "::attr('type')"),
            "description": self.select_css(media_description_node, "::text")}
        if media_keywords_node: media_keywords = self.select_css(media_keywords_node, "::text").split(",")
        if media_thumbnails_node: media_thumbnails = {"url": self.select_css(media_thumbnails_node, "::attr('url')"),
                                                      "width": self.select_css(media_thumbnails_node, "::attr('width')",
                                                                               expectedtype=int),
                                                      "height": self.select_css(media_thumbnails_node,
                                                                                "::attr('height')", expectedtype=int),
                                                      "time": self.select_css(media_thumbnails_node, "::attr('time')")}
        if media_category_node: media_category = {"scheme": self.select_css(media_category_node, "::attr('scheme')"),
                                                  "label": self.select_css(media_category_node, "::attr('label')"),
                                                  "categorie": self.select_css(media_category_node, "::text")}
        if media_hash_node: media_hash = {"hash": self.select_css(media_hash_node, "::text"),
                                          "algo": self.select_css(media_hash_node, "::attr('algo')")}
        if media_player_node: media_player = {"url": self.select_css(media_player_node, "::attr('url')"),
                                              "width": self.select_css(media_player_node, "::attr('width')",
                                                                       expectedtype=int),
                                              "height": self.select_css(media_player_node, "::attr('height')",
                                                                        expectedtype=int)}
        if media_credit_node: media_credit = {"scheme": self.select_css(media_credit_node, "::attr('scheme')"),
                                              "role": self.select_css(media_credit_node, "::attr('role')")}
        if media_copyright_node: media_copyright = {"url": self.select_css(media_copyright_node, "::attr('url')"),
                                                    "copyright": self.select_css(media_copyright_node, "::text")}
        if media_text_node: media_text = {"type": self.select_css(media_text_node, "::attr('type')"),
                                          "lang": self.select_css(media_text_node, "::attr('lang')"),
                                          "start": self.select_css(media_text_node, "::attr('start')"),
                                          "end": self.select_css(media_text_node, "::attr('end')"),
                                          "text": self.select_css(media_text_node, "::text")}
        if media_restriction_node: media_restriction = {
            "restriction": self.select_css(media_restriction_node, "::text"),
            "relationship": self.select_css(media_restriction_node, "::attr('relationship')"),
            "type": self.select_css(media_restriction_node, "::attr('type')")}
        if media_status_node: media_status = {"state": self.select_css(media_status_node, "::attr('state')"),
                                              "reason": self.select_css(media_status_node, "::attr('reason')")}
        media_comments = []
        if media_comments_node:
            media_comments_nodes = media_comments_node.css("media|comment")
            for media_comment_node in media_comments_nodes:
                media_comments.append(media_comment_node.css("::text").extract_first())
        if media_price_node: media_price = {"type": self.select_css(media_price_node, "::attr('type')"),
                                            "price": float(self.select_css(media_price_node, "::attr('price')")),
                                            "currency": self.select_css(media_price_node, "::attr('currency')")}
        if media_embed_node:
            media_embed_params = []
            for paramnode in media_embed_node.css("media|param"):
                media_embed_params.append({"name": self.select_css(paramnode, "::attr('name')"),
                                           "value": self.select_css(paramnode, "::text")})

            media_embed = {"url": self.select_css(media_embed_node, "::attr('url')"),
                           "width": self.select_css(media_embed_node, "::attr('width')"),
                           "height": self.select_css(media_embed_node, "::attr('height')"),
                           "params": str(media_embed_params)}
        if media_license_node: media_license = {"type": self.select_css(media_license_node, "::attr('type')"),
                                                "href": self.select_css(media_license_node, "::attr('href')"),
                                                "license ": self.select_css(media_license_node, "::text")}
        if media_subTitle_node: media_subTitle = {"type": self.select_css(media_subTitle_node, "::attr('type')"),
                                                  "lang": self.select_css(media_subTitle_node, "::attr('lang')"),
                                                  "href": self.select_css(media_subTitle_node, "::attr('href')")}
        if media_peerLink_node: media_peerLink = {"type": self.select_css(media_peerLink_node, "::attr('type')"),
                                                  "href": self.select_css(media_peerLink_node, "::attr('href')")}
        # media:location
        if media_rights_node: media_rights = self.select_css(media_rights_node, "::attr('status')")
        if media_scenes_node:
            media_scenes_nodes = media_scenes_node.css("media|scene")
            for media_scene_node in media_scenes_nodes:
                media_scenes.append({"title": self.select_css(media_scene_node, "sceneTitle::text"),
                                     "description": self.select_css(media_scene_node, "sceneDescription::text"),
                                     "starttime": self.select_css(media_scene_node, "sceneStartTime::text"),
                                     "endtime": self.select_css(media_scene_node, "sceneEndTime::text")})
        feed_contentencoded = {}  # feed_contentencoded_node = selector.css("content|encoded")#if feed_contentencoded_node:feed_contentencoded = {}
        if media_responses_node:
            media_responses_nodes = media_responses_node.css("media|response")
            for media_response_node in media_responses_nodes:
                media_responses.append(self.select_css(media_response_node, "::text"))
        if media_backLinks_node:
            media_backLinks_nodes = media_backLinks_node.css("media|backLink")
            for media_backLink_node in media_backLinks_nodes:
                media_backLinks.append(self.select_css(media_backLink_node, "::text"))
        if media_community_node: media_community = {
            "starRating": {"average": self.select_css(media_community_node, "media|starRating::attr('average')", float),
                           "count": self.select_css(media_community_node, "media|starRating::attr('count')", int),
                           "min": self.select_css(media_community_node, "media|starRating::attr('min')", int),
                           "max": self.select_css(media_community_node, "media|starRating::attr('max')", int)},
            "statistics": {"views": self.select_css(media_community_node, "media|statistics ::attr('views')", int),
                           "favorites": self.select_css(media_community_node, "media|statistics ::attr('favorites')",
                                                        int)},
            "tags": self.select_css(media_community_node, "media|tags::text").split(',')}
        return RssFeed(channel=str(channel), title=str(feed_title), link=str(feed_link), mediatitle=json.dumps(media_title),
                       author=str(feed_author), description=str(feed_description),
                       categories=json.dumps(feed_categories), comments=str(feed_comments), enclosure=json.dumps(feed_enclosure),
                       guid=json.dumps(feed_guid),
                       pubDate=feed_pubdate, source=json.dumps(feed_source), atomelink=json.dumps(feed_atome),
                       contentencoded=json.dumps(feed_contentencoded), dccreator=str(dc_creators),
                       slashcomments=int(feed_slash_comments),
                       creativeCommonslicense=str(feed_creativeCommons), mediacontent=json.dumps(media_content),
                       mediaratings=json.dumps(media_rating), mediasubTitle=json.dumps(media_subTitle),
                       mediapeerLink=json.dumps(media_peerLink),
                       mediarights=str(media_rights), mediascenes=json.dumps(media_scenes),
                       mediadescription=json.dumps(media_description), mediakeywords=json.dumps(media_keywords),
                       mediathumbnails=json.dumps(media_thumbnails), mediacategory=json.dumps(media_category),
                       mediahash=json.dumps(media_hash), mediaplayer=json.dumps(media_player), mediacredit=json.dumps(media_credit),
                       mediacopyright=json.dumps(media_copyright), mediatext=json.dumps(media_text),
                       mediarestriction=json.dumps(media_restriction), mediacommunities=json.dumps(media_community),
                       mediacomments=json.dumps(media_comments), mediaembed=json.dumps(media_embed),
                       mediaresponses=json.dumps(media_responses), mediabackLinks=json.dumps(media_backLinks),
                       mediastatus=json.dumps(media_status), mediaprice=json.dumps(media_price), medialicense=json.dumps(media_license),
                       dctermsvalid=json.dumps("{}"))

    def get_channel(self, response):
        # __________ FOR UNIT ONLY
        channel_domain = "nytimes.com"
        # channel_domain = response.meta.get("domain")
        channel_title = self.select_css(response, "channel > title::text")
        channel_link = self.select_css(response, "channel > link::text")
        channel_description = self.select_css(response, "channel > description::text")
        channel_language = self.select_css(response, "channel > language::text")
        channel_copyright = self.select_css(response, "channel > copyright::text")
        channel_lastBuild_date = self.select_css(response, "channel > lastBuildDate::text")
        if channel_lastBuild_date == "":
            channel_lastBuild_date = datetime.datetime.today()
        else:
            channel_lastBuild_date = datetime.datetime.strptime(channel_lastBuild_date, "%a, %d %b %Y %H:%M:%S %z")
        channel_pub_date = self.select_css(response, "channel > pubDate::text")
        if channel_pub_date == "":
            channel_pub_date = datetime.datetime.today()
        else:
            channel_pub_date = email.utils.parsedate_to_datetime(channel_pub_date)

        channel_docs = self.select_css(response, "channel > docs::text")
        channel_generator = self.select_css(response, "channel > generator::text")
        channel_managing_editor = self.select_css(response, "channel > managingEditor::text")
        channel_rating = self.select_css(response, "channel > rating::text")
        channel_ttl = self.select_css(response, "channel > ttl::text")
        channel_web_master = self.select_css(response, "channel > webMaster::text")
        channel_skip_days = []
        channel_skip_days_node = response.css("channel > skipDays > day")
        if channel_skip_days_node:
            for channel_skip_day_node in channel_skip_days_node: channel_skip_days.append(
                channel_skip_day_node.css("::text").extract_first())
        channel_skip_hours = []
        channel_skip_hours_node = response.css("channel > skipHours > hour")
        if channel_skip_hours_node:
            for channel_skip_hour_node in channel_skip_hours_node: channel_skip_hours.append(
                int(channel_skip_hour_node.css("::text").extract_first()))

        channel_image_node = response.css("channel > image")
        channel_image = {"link":"","title":"","url":"","description":"","width":0,"height":0}
        channel_image_width = self.select_css(channel_image_node, "width::text")
        if channel_image_width == "":
            channel_image_width = 0
        else:
            channel_image_width = int(channel_image_width)
        channel_image_height = self.select_css(channel_image_node, "height::text")
        if channel_image_height == "":
            channel_image_height = 0
        else:
            channel_image_height = int(channel_image_height)
        if channel_image_node: channel_image = {"link": self.select_css(channel_image_node, "link::text"),
                                                "title": self.select_css(channel_image_node, "title::text"),
                                                "url": self.select_css(channel_image_node, "url::text"),
                                                "description": self.select_css(channel_image_node, "description::text"),
                                                "width": channel_image_width,
                                                "height": channel_image_height}

        channel_cloud_node = response.css("channel > cloud")
        channel_cloud = {}
        if channel_cloud_node:
            channel_cloud = {"domain": self.select_css(channel_cloud_node, "::attr('domain')"),
                             "path ": self.select_css(channel_cloud_node, "::attr('path')"),
                             "port": self.select_css(channel_cloud_node, "::attr('port')"),
                             "protocol": self.select_css(channel_cloud_node, "::attr('protocol')"),
                             "procedure": self.select_css(channel_cloud_node, "::attr('registerProcedure')")}

        channel_categories_nodes = response.css("channel > category")
        channel_categories = []
        if channel_categories_nodes:
            for channel_categorie_node in channel_categories_nodes:
                channel_categories.append({"categorie": self.select_css(channel_categorie_node, "::text"),
                                           "domain": self.select_css(channel_categorie_node, "::attr('domain')")})
        channel_feed_input_node = response.css("channel > textInput")
        channel_feed_input = {"description": "", "title": "", "link": "", "name": ""}
        if channel_feed_input_node:
            channel_feed_input = {
                "description": self.select_css(channel_feed_input_node, "description::text"),
                "title": self.select_css(channel_feed_input_node, "title::text"),
                "link": self.select_css(channel_feed_input_node, "link::text"),
                "name": self.select_css(channel_feed_input_node, "name::text")
            }

        return RssChannel(url=response.url, domain=channel_domain, link=channel_link, title=channel_title,
                          categories=str(channel_categories), cloud=json.dumps(channel_cloud), copyright=channel_copyright,
                          docs=channel_docs, generator=channel_generator, imagelink=channel_image["link"],
                          imagetitle=channel_image["title"], imageurl=channel_image["url"],
                          imagedescription=channel_image["description"], imageheight=channel_image["height"],
                          imagewidth=channel_image["width"], language=channel_language,
                          lastBuildDate=channel_lastBuild_date, managingEditor=channel_managing_editor,
                          pubDate=channel_pub_date, rating=channel_rating, skipDays=json.dumps(channel_skip_days),
                          skipHours=json.dumps(channel_skip_hours), textInputdescription=channel_feed_input["description"],
                          textInputlink=channel_feed_input["link"], textInputname=channel_feed_input["name"],
                          textInputtitle=channel_feed_input["title"], ttl=channel_ttl, webmaster=channel_web_master,
                          description=channel_description)

    def register_name_spaces(self, response):
        response.selector.register_namespace("media", "http://search.yahoo.com/mrss/")
        response.selector.register_namespace("atome", "http://www.w3.org/2005/Atom")
        response.selector.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
        response.selector.register_namespace("slash", "http://purl.org/rss/1.0/modules/slash/")
        response.selector.register_namespace("content", "http://purl.org/rss/1.0/modules/content/")
        response.selector.register_namespace("creativeCommons", "http://backend.userland.com/creativeCommonsRssModule")
        return response

    def select_css(self, selector, css, expectedtype: type = str):
        if selector:
            node = selector.css(css)
            if node:
                try:
                    value = expectedtype(node.extract_first())
                    return value
                except ValueError as error:
                    print("WARNING :", error)
                    return expectedtype()
            else:
                return expectedtype()
        else:
            return expectedtype()

    def setup_allowed_domains(self, urls: Iterable = None):
        if urls is None: urls = self.start_urls
        self.allowed_domains.clear()
        for url in urls:
            self.allowed_domains.append(getDomaine(url))

    def setup_start_urls(self, rss_channels: Iterable = None):
        if rss_channels is None:
            rss_channels = self.start_rss_channels
        else:
            self.start_rss_channels = rss_channels
        for rss_channel in rss_channels:
            self.start_urls.append(rss_channel.url)

    """ ITEMS https://www.rssboard.org/rss-specification
    author	Email address of the author of the item. More.	
    category	Includes the item in one or more categories. More.	
    comments	URL of a page for comments relating to the item. More.	
    enclosure	Describes a media object that is attached to the item. More.	
    guid	A string that uniquely identifies the item. More.	
    pubDate	Indicates when the item was published. More.	
    source	The RSS channel that the item came from. More.
    """

    """
    self.localdb.open()
    self.localdb.addRssChannels([response.url])
    self.localdb.close()
    """
    """
    self.localdb.open()
    self.localdb.addWebSites(feeds_externalLinks)
    self.localdb.close()
    """
