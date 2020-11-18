import datetime
import json

class Object:
    def _keys(self):
        keys = []
        for key in self.__dict__.keys():
            keys.append(key)
        return keys


class RssChannel(Object):
    url = ""
    domain = ""
    link = ""
    title = ""
    categories = ""
    cloud = ""
    copyright = ""
    docs = ""
    generator = ""
    imagelink = ""
    imagetitle = ""
    imageurl = ""
    imagedescription = ""
    imageheight = ""
    imagewidth = ""
    language = ""
    lastBuildDate = ""
    managingEditor = ""
    pubDate = ""
    rating = ""
    skipDays = ""
    skipHours = ""
    textInputdescription = ""
    textInputlink = ""
    textInputname = ""
    textInputtitle = ""
    ttl = ""
    webmaster = ""
    description = ""

    def __init__(self, object: None = None, url: str = "", domain: str = "", link: str = "", title: str = "",
                 categories: str = "", cloud: str = "{}", copyright: str = "", docs: str = "", generator: str = "",
                 imagelink: str = "", imagetitle: str = "", imageurl: str = "", imagedescription: str = "",
                 imageheight: int = 0, imagewidth: int = 0, language: str = "",
                 lastBuildDate: datetime.datetime = datetime.datetime.today(),
                 managingEditor: str = "", pubDate: datetime.datetime = datetime.datetime.today(), rating: str = "",
                 skipDays: str = "", skipHours: str = "",
                 textInputdescription: str = "", textInputlink: str = "", textInputname: str = "",
                 textInputtitle: str = "", ttl: str = "", webmaster: str = "", description: str = ""):
        if object:
            self._fromobject(object)
        else:
            self.url, self.domain, self.link, self.title, self.categories, self.cloud, self.copyright, self.docs, self.generator, self.imagelink, self.imagetitle, self.imageurl, self.imagedescription, self.imageheight, self.imagewidth, self.language, self.lastBuildDate, self.managingEditor, self.pubDate, self.rating, self.skipDays, self.skipHours, self.textInputdescription, self.textInputlink, self.textInputname, self.textInputtitle, self.ttl, self.webmaster, self.description = url, domain, link, title, categories, cloud, copyright, docs, generator, imagelink, imagetitle, imageurl, imagedescription, imageheight, imagewidth, language, lastBuildDate, managingEditor, pubDate, rating, skipDays, skipHours, textInputdescription, textInputlink, textInputname, textInputtitle, ttl, webmaster, description

    def _object(self):
        object = {}
        object["url"], object["domain"], object["link"], object["title"], object["categories"], object["cloud"], \
        object["copyright"], object["docs"], object["generator"], object["imagelink"], object["imagetitle"], \
        object[
            "imageurl"], object["imagedescription"], object["imageheight"], object["imagewidth"], object[
            "language"], object["lastbuilddate"], object["managingeditor"], object["pubdate"], object["rating"], \
        object["skipdays"], object["skiphours"], object["textinputdescription"], object["textinputlink"], \
        object[
            "textinputname"], object["textinputtitle"], object["ttl"], object[
            "webmaster"], object[
            "description"] = self.url, self.domain, self.link, self.title, self.categories, self.cloud, self.copyright, self.docs, self.generator, self.imagelink, self.imagetitle, self.imageurl, self.imagedescription, self.imageheight, self.imagewidth, self.language, self.lastBuildDate, self.managingEditor, self.pubDate, self.rating, self.skipDays, self.skipHours, self.textInputdescription, self.textInputlink, self.textInputname, self.textInputtitle, self.ttl, self.webmaster, self.description
        return object

    def _fromobject(self, object):
        self.url, self.domain, self.link, self.title, self.categories, self.cloud, self.copyright, self.docs, self.generator, self.imagelink, self.imagetitle, self.imageurl, self.imagedescription, self.imageheight, self.imagewidth, self.language, self.lastBuildDate, self.managingEditor, self.pubDate, self.rating, self.skipDays, self.skipHours, self.textInputdescription, self.textInputlink, self.textInputname, self.textInputtitle, self.ttl, self.webmaster, self.description = \
            object["url"], object["domain"], object["link"], object["title"], object["categories"], object["cloud"], \
            object["copyright"], object["docs"], object["generator"], object["imagelink"], object["imagetitle"], \
            object[
                "imageurl"], object["imagedescription"], object["imageheight"], object["imagewidth"], object[
                "language"], object["lastbuilddate"], object["managingeditor"], object["pubdate"], object["rating"], \
            object["skipdays"], object["skiphours"], object["textinputdescription"], object["textinputlink"], \
            object[
                "textinputname"], object["textinputtitle"], object["ttl"], object["webmaster"], object["description"]

    def _array(self):
        return [self.url, self.domain, self.link, self.title, self.categories, self.cloud, self.copyright, self.docs,
                self.generator, self.imagelink, self.imagetitle, self.imageurl, self.imagedescription, self.imageheight,
                self.imagewidth, self.language, self.lastBuildDate, self.managingEditor, self.pubDate, self.rating,
                self.skipDays, self.skipHours, self.textInputdescription, self.textInputlink, self.textInputname,
                self.textInputtitle, self.ttl, self.webmaster, self.description]
    def json(self):
        return json.dumps(self._object())

class Domaine(Object):
    url = ""
    name = ""
    description = ""
    roletype = ""
    title = ""
    image = ""
    keywords: [] = []
    icon = ""
    language = ""
    robots: [] = []
    starturl = ""

    def __init__(self, object: {} = None, url: str = "", name: str = "", description: str = "", roletype: str = "",
                 title: str = "",
                 image: str = "", keywords: str = "", icon: str = "", language: str = "", robots: str = "",
                 starturl: str = ""):
        if object:
            self._fromobject(object)
        else:
            self.url, self.name, self.description, self.roletype, self.title, self.image, self.keywords, self.icon, self.language, self.robots, self.starturl = url, name, description, roletype, title, image, keywords, icon, language, robots, starturl

    def _object(self):
        object = {}
        object['url'], object['name'], object['description'], object['roletype'], object['title'], object['image'], \
        object['keywords'], object['icon'], object['language'], object['robots'], object[
            'starturl'] = self.url, self.name, self.description, self.roletype, self.title, self.image, self.keywords, self.icon, self.language, self.robots, self.starturl
        return object

    def _fromobject(self, object):
        self.url, self.name, self.description, self.roletype, self.title, self.image, self.keywords, self.icon, self.language, self.robots, self.starturl = \
            object['url'], object['name'], object['description'], object['roletype'], object['title'], object['image'], \
            str(object['keywords']), object['icon'], object['language'], str(object['robots']), object['starturl']

    def _array(self):
        return [self.url, self.name, self.description, self.roletype, self.title, self.image, self.keywords, self.icon,
                self.language, self.robots, self.starturl]
    def json(self):
        return json.dumps(self._object())


class RssFeed(Object):
    id: int
    channel: str
    title: str = ""
    link: str = ""
    author: str = ""
    description: str = ""
    categories: str = "[]"
    comments: str = ""
    enclosure: str = "{}"
    guid: str = "{}"
    pubDate: datetime.datetime = datetime.datetime.today()
    source: str = "{}"
    atomelink: str = "{}"
    contentencoded: str = "{}"
    dccreator: str = ""
    slashcomments: int = 0
    creativeCommonslicense: str = ""
    mediacontent: str = "{}"
    mediaratings: str = "[]"
    mediatitle: str = "{}"
    mediadescription: str = "{}"
    mediakeywords: str = "{}"
    mediathumbnails: str = "{}"
    mediacategory: str = "{}"
    mediahash: str = "{}"
    mediaplayer: str = "{}"
    mediacredit: str = "{}"
    mediacopyright: str = "{}"
    mediatext: str = "{}"
    mediarestriction: str = "{}"
    mediacommunities: str = "[]"
    mediacomments: str = "[]"
    mediaembed: str = "{}"
    mediaresponses: str = "[]"
    mediabackLinks: str = "[]"
    mediastatus: str = "{}"
    mediaprice: str = "{}"
    medialicense: str = "{}"
    mediasubTitle: str = "{}"
    mediapeerLink: str = "{}"
    mediarights: str = ""
    mediascenes: str = "[]"
    dctermsvalid: str = "{}"

    def __init__(self, id: int = None, channel: str = "", title: str = "", link: str = "", author: str = "",
                 description: str = "",
                 categories: str = "[]",
                 comments: str = "", enclosure: str = "{}", guid: str = "{}",
                 pubDate: datetime.datetime = datetime.datetime.today(), source: str = "{}", atomelink: str = "{}",
                 contentencoded: str = "{}", dccreator: str = "", slashcomments: int = 0,
                 creativeCommonslicense: str = "", mediacontent: str = "{}", mediaratings: str = "[]",
                 mediatitle: str = "{}", mediadescription: str = "{}", mediakeywords: str = "{}",
                 mediathumbnails: str = "{}", mediacategory: str = "{}", mediahash: str = "{}", mediaplayer: str = "{}",
                 mediacredit: str = "{}", mediacopyright: str = "{}", mediatext: str = "{}",
                 mediarestriction: str = "{}", mediacommunities: str = "[]", mediacomments: str = "[]",
                 mediaembed: str = "{}", mediaresponses: str = "[]", mediabackLinks: str = "[]",
                 mediastatus: str = "{}", mediaprice: str = "[]", medialicense: str = "{}", mediasubTitle: str = "{}",
                 mediapeerLink: str = "{}", mediarights: str = "", mediascenes: str = "[]",
                 dctermsvalid: str = "{}", object=None):
        if object:
            self._fromobject(object)
        else:
            self.id, self.channel, self.title, self.link, self.author, self.description, self.categories, self.comments, self.enclosure, self.guid, self.pubDate, self.source, self.atomelink, self.contentencoded, self.dccreator, self.slashcomments, self.creativeCommonslicense, self.mediacontent, self.mediaratings, self.mediatitle, self.mediadescription, self.mediakeywords, self.mediathumbnails, self.mediacategory, self.mediahash, self.mediaplayer, self.mediacredit, self.mediacopyright, self.mediatext, self.mediarestriction, self.mediacommunities, self.mediacomments, self.mediaembed, self.mediaresponses, self.mediabackLinks, self.mediastatus, self.mediaprice, self.medialicense, self.mediasubTitle, self.mediapeerLink, self.mediarights, self.mediascenes, self.dctermsvalid = id, channel, title, link, author, description, categories, comments, enclosure, guid, pubDate, source, atomelink, contentencoded, dccreator, slashcomments, creativeCommonslicense, mediacontent, mediaratings, mediatitle, mediadescription, mediakeywords, mediathumbnails, mediacategory, mediahash, mediaplayer, mediacredit, mediacopyright, mediatext, mediarestriction, mediacommunities, mediacomments, mediaembed, mediaresponses, mediabackLinks, mediastatus, mediaprice, medialicense, mediasubTitle, mediapeerLink, mediarights, mediascenes, dctermsvalid

    def _object(self):
        object = {}
        object["id"], object["title"], object["link"], object["author"], object["description"], object["categories"], \
        object[
            "comments"], object["enclosure"], object["guid"], object["pubDate"], object["source"], object["atomelink"], \
        object["contentencoded"], object["dccreator"], object["slashcomments"], object["creativeCommonslicense"], \
        object["mediacontent"], object["mediaratings"], object["mediatitle"], object["mediadescription"], object[
            "mediakeywords"], object["mediathumbnails"], object["mediacategory"], object["mediahash"], object[
            "mediaplayer"], object["mediacredit"], object["mediacopyright"], object["mediatext"], object[
            "mediarestriction"], object["mediacommunities"], object["mediacomments"], object["mediaembed"], object[
            "mediaresponses"], object["mediabackLinks"], object["mediastatus"], object["mediaprice"], object[
            "medialicense"], object["mediasubTitle"], object["mediapeerLink"], object["mediarights"], object[
            "mediascenes"], object[
            "dctermsvalid"] = self.id, self.title, self.link, self.author, self.description, self.categories, self.comments, self.enclosure, self.guid, self.pubDate, self.source, self.atomelink, self.contentencoded, self.dccreator, self.slashcomments, self.creativeCommonslicense, self.mediacontent, self.mediaratings, self.mediatitle, self.mediadescription, self.mediakeywords, self.mediathumbnails, self.mediacategory, self.mediahash, self.mediaplayer, self.mediacredit, self.mediacopyright, self.mediatext, self.mediarestriction, self.mediacommunities, self.mediacomments, self.mediaembed, self.mediaresponses, self.mediabackLinks, self.mediastatus, self.mediaprice, self.medialicense, self.mediasubTitle, self.mediapeerLink, self.mediarights, self.mediascenes, self.dctermsvalid
        return object

    def _fromobject(self, object):
        self.title, self.link, self.author, self.description, self.categories, self.comments, self.enclosure, self.guid, self.pubDate, self.source, self.atomelink, self.contentencoded, self.dccreator, self.slashcomments, self.creativeCommonslicense, self.mediacontent, self.mediaratings, self.mediatitle, self.mediadescription, self.mediakeywords, self.mediathumbnails, self.mediacategory, self.mediahash, self.mediaplayer, self.mediacredit, self.mediacopyright, self.mediatext, self.mediarestriction, self.mediacommunities, self.mediacomments, self.mediaembed, self.mediaresponses, self.mediabackLinks, self.mediastatus, self.mediaprice, self.medialicense, self.mediasubTitle, self.mediapeerLink, self.mediarights, self.mediascenes, self.dctermsvalid = \
            object["title"], object["link"], object["author"], object["description"], object[
                "categories"], object[
                "comments"], object["enclosure"], object["guid"], object["pubDate"], object["source"], object[
                "atomelink"], \
            object["contentencoded"], object["dccreator"], object["slashcomments"], object["creativeCommonslicense"], \
            object["mediacontent"], object["mediaratings"], object["mediatitle"], object["mediadescription"], object[
                "mediakeywords"], object["mediathumbnails"], object["mediacategory"], object["mediahash"], object[
                "mediaplayer"], object["mediacredit"], object["mediacopyright"], object["mediatext"], object[
                "mediarestriction"], object["mediacommunities"], object["mediacomments"], object["mediaembed"], object[
                "mediaresponses"], object["mediabackLinks"], object["mediastatus"], object["mediaprice"], object[
                "medialicense"], object["mediasubTitle"], object["mediapeerLink"], object["mediarights"], object[
                "mediascenes"], object["dctermsvalid"]

    def _array(self):
        return [self.channel, self.title, self.link, self.author, self.description, self.categories, self.comments,
                self.enclosure,self.guid, self.pubDate, self.source, self.atomelink, self.contentencoded, self.dccreator,
                self.slashcomments, self.creativeCommonslicense, self.mediacontent, self.mediaratings, self.mediatitle,
                self.mediadescription, self.mediakeywords, self.mediathumbnails, self.mediacategory, self.mediahash,
                self.mediaplayer, self.mediacredit, self.mediacopyright, self.mediatext, self.mediarestriction,
                self.mediacommunities, self.mediacomments, self.mediaembed, self.mediaresponses, self.mediabackLinks,
                self.mediastatus, self.mediaprice, self.medialicense, self.mediasubTitle, self.mediapeerLink,
                self.mediarights, self.mediascenes, self.dctermsvalid]
    def json(self):
        return json.dumps(self._object())
