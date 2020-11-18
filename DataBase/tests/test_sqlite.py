import unittest

from DataBase import SQLite
from DataBase.items import Domain, RssChannel


class test__mysql(unittest.TestCase):
    def test_sqlite_init(self):
        sqlite = SQLite("../../Storage/localdb.db")
        self.assertNotEqual(sqlite.connexion,None,"FAILED CRFEATING SQLITE CONNEXION")
        sqlite.close()
        self.assertEqual(sqlite.connexion,None,"FAILED CLOSING DB")
    def test_insert_domains(self):
        d = Domain("domain_test")
        sqlite = SQLite("../../Storage/localdb.db")
        sqlite.insert_collected_domains([d])
        sqlite.close()
    def test_insert_rss_channels_links(self):
        rch = RssChannel("hellodomain","domain_test")
        sqlite = SQLite("../../Storage/localdb.db")
        sqlite.insert_rss_channels([rch])
        sqlite.close()
    def test_update_collected_domains_state(self):
        dmns = [Domain("https://nytimes.com"),Domain("https://twitter.com"),Domain("https://noidea.com")]
        sqlite = SQLite("../../Storage/localdb.db")
        sqlite.update_collected_domains(dmns)
        sqlite.close()
    def test_select_domains(self):
        sqlite = SQLite("../../Storage/localdb.db")
        print(sqlite.select_collected_domains(state=2))
        sqlite.close()
    def test_select_rss_channels(self):
        sqlite = SQLite("../../Storage/localdb.db")
        print(sqlite.select_rss_channels())
        sqlite.close()
if __name__ == "__main__":
    unittest.main()