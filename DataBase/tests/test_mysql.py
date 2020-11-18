import datetime
import unittest

from DataBase import SQLite
from items import Domaine, RssChannel, RssFeed
from ..MySQL import MySQL
class test__mysql(unittest.TestCase):

    def test_mysql_init(self):
        mysql = MySQL()
        self.assertNotEqual(mysql.connexion,None,"FAILED CREATING CONNEXION")
        mysql.close()
        self.assertEqual(mysql.connexion,None,"FAILED CLOSING DB")
    def test_mysql_insert_domaine(self):
        #d = Domaine(url="sddss",name="sdfsdfsdfsf",description="dsfdsfdfg",roletype="Kj",title="GO AWAy",image="... YOU",keywords="bla/bla",icon="==>",language="0°",robots="sqdqsd",starturl="fsdf")
        d = Domaine(object={'url': 'https://nytimes.com', 'name': 'The New York Times', 'description': 'The New York Times: Find breaking news, multimedia, reviews & opinion on Washington, business, sports, movies, travel, books, jobs, education, real estate, cars & more at nytimes.com.', 'roletype': 'website', 'title': 'Breaking News, World News & Multimedia', 'image': 'https://static01.nyt.com/newsgraphics/images/icons/defaultPromoCrop.png', 'keywords': ['Funerals', 'Judaism', 'Coronavirus;COVID-19', 'Bill de Blasio', 'Williamsburg Brooklyn', 'Hasidism', 'NYPD', 'Greenhouse gas', 'Electric power', 'Air conditioning', 'Quarantines', 'Manhattan', 'Endowments', 'Private Schools', 'Wages and salaries', 'CARES Act;Coronvirus Stimulus', 'Pingry School', 'Sidwell Friends School', "St. Andrew's Episcopal", 'US Politics', 'Medicine and Health', 'Health and Human Services', 'Alex Azar', 'Donald Trump', 'Seema Verma', '', 'Appointments and Executive Changes', 'Federal Reserve', 'Jerome Powell', 'US Economy', 'Interest rate', 'Joe Biden', 'Tara Reade', 'Rape', '2020 Election', 'Women and Girls', 'MeToo Movement', 'Polls', 'Republicans', 'Brad Parscale', 'Mobile Apps', 'Government Surveillance', 'Privacy', 'Smartphone', 'Software', 'Apple', 'Google', 'Douglas Burgum', 'Karnataka India', 'Maharashtra', 'Norway', 'Great Britain', 'North Dakota', 'Medical test', 'Antibody', 'Quest Diagnostics', 'Laboratory Corporation of America Holdings', 'your-feed-science', 'Rutgers', 'Yale', 'Audio Recordings', ' Downloads and Streaming', 'Music', 'Luxury Goods', 'London', 'The Electric Recording Co.', 'Pete Hutchison'], 'icon': 'https://www.nytimes.com/vi-assets/static-assets/favicon-4bf96cb6a1093748bf5b3c429accb9b4.ico', 'language': 'en-US', 'robots': ['noarchive', 'noodp', 'noydir'], 'starturl': 'https://www.nytimes.com'})
        mysql = MySQL()
        mysql.insert_domains([d])
    def test_insert_rsschannels(self):
        rsschannel = RssChannel(url="https://akashjaindxb.com/about/feed/",cloud="{\"test\":12}",skipHours="[]",skipDays="[]",imagewidth=0,imageheight=0,pubDate=datetime.datetime.strptime("Wed, 29 Apr 2020 22:49:17 +0000","%a, %d %b %Y %H:%M:%S %z"))
        mysql = MySQL()
        mysql.insert_rss_channels([rsschannel])
        mysql.commit()
        sqlite = SQLite()
        sqlitersschannels = []
        for rssch in [rsschannel]:
            sqlitersschannels.append(RssChannel(url=rssch.url))
        sqlite.delete_rss_channels(rsschannels=sqlitersschannels)
    def test_insert_rss_feeds(self):
        rssfeed = RssFeed()
        mysql = MySQL()
        mysql.insert_rss_feeds([rssfeed])



if __name__ == "__main__":
    unittest.main()