import mysql.connector
from mysql.connector import Error

from DataBase.items import RssChannel
from DataBase.SqlLite import SQLite

RSS_CHANNELS_TABLENAME = "rsschannel"
WEBSITES_TABLENAME = "websites"


class MySQL:
    connexion = None
    settings = None

    def __init__(self, host: str = "127.0.0.1", user: str = "root", password: str = "",
                 database: str = "feedspider", settings: {} = None):
        self.set_settings(host=host,user=user, password=password, database=database)
        self.open()

    def insert_domains(self, domains):
        args, domain = [], ""
        try:
            self.open()
            for domain in domains: args.append(domain._array())
            self.connexion.cursor().executemany(
                "INSERT INTO domains (url, name, description, roletype, title, image, keywords, icon, language, robots, starturl)  VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                args)
            self.commit()
        except Error as error:
            print("MY SQL INSERT DOMAINS ERROR : ", {"error": error, "domain": domain})
        finally:
            return self

    def update_domains(self):
        pass

    def delete_domains(self):
        pass

    def insert_rss_channels(self, channels):
        args, channel = [], ""
        try:
            self.open()
            for channel in channels: args.append(channel._array())
            self.connexion.cursor().executemany(
                "INSERT INTO rsschannels(url, domain, link, title, categories, cloud, copyright, docs, generator, imagelink, imagetitle, imageurl, imagedescription, imageheight, imagewidth, language, lastBuildDate, managingEditor, pubDate, rating, skipDays, skipHours, textInputdescription, textInputlink, textInputname, textInputtitle, ttl, webmaster,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                args)
            self.commit()
            sqlite = SQLite()
            sqlite.delete_rss_channels(rsschannels=channels)

        except Error as error:
            print("MY SQL INSERT CHANNELS ERROR : ", {"error": error, "channel": channel})
        finally:
            return self

    def update_rss_channels(self):
        pass

    def delete_rss_channels(self):
        pass

    def insert_rss_feeds(self, feeds):
        args, feed = [], ""
        try:
            self.open()
            for feed in feeds: args.append(feed._array())
            self.connexion.cursor().executemany("INSERT INTO `rssfeeds`(`channel`, `title`, `link`, `author`, `description`, `categories`, `comments`, `enclosure`, `guid`, `pubDate`, `source`, `atomelink`, `contentencoded`, `dccreator`, `slashcomments`, `creativeCommonslicense`, `mediacontent`, `mediaratings`, `mediatitle`, `mediadescription`, `mediakeywords`, `mediathumbnails`, `mediacategory`, `mediahash`, `mediaplayer`, `mediacredit`, `mediacopyright`, `mediatext`, `mediarestriction`, `mediacommunities`, `mediacomments`, `mediaembed`, `mediaresponses`, `mediabackLinks`, `mediastatus`, `mediaprice`, `medialicense`, `mediasubTitle`, `mediapeerLink`, `mediarights`, `mediascenes`, `dctermsvalid`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", args)
            self.commit()
        except Error as error:
            print("MY SQL INSERT FEEDS ERROR : ", {"error": error, "feed": feed})
        finally:
            return self

    def update_rss_feed(self):
        pass

    def delete_rss_feed(self):
        pass

    def close(self):
        if self.connexion: self.connexion.close()
        self.connexion = None

    def commit(self):
        if self.connexion: self.connexion.commit()

    def open(self):
        if self.connexion: return self.connexion
        try:
            self.connexion = mysql.connector.connect(host=self.settings["host"],
                                                     user=self.settings["user"], passwd=self.settings["password"],
                                                     database=self.settings["database"])
            self.connexion.cursor().executemany("", )
            self.connexion.cursor().fetchall()


        except  Error as error:
            print("MYSQL ERROR : ", error)
        finally:
            return self.connexion

    def set_settings(self, host: str = "localhost", user: str = "root", password: str = "",
                     database: str = "", settings: {} = None):
        if settings:
            self.settings = settings
        else:
            self.settings = {"host": host,"user": user, "password": password, "database": database}

        return self.settings

# sql = "INSERT INTO domains (url, name, description, roletype, title, image, keywords, icon, language, robots, starturl)  VALUES(" + data['url']+ "," +data['name']+ "," +data['description']+ "," +data['roletype']+ "," +data['title']+ "," +data['image']+ "," +data['keywords']+ "," +data['icon']+ "," +data['language']+ "," +data['robots']+ "," +data['starturl'] + ")"
