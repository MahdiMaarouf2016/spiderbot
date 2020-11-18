from os import system
from sys import argv

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings

from DataBase import SQLite, RssChannel
from Spiders import WebSitesSpider, RssChannelsSpider

settings = Settings()
settings.set("USER_AGENT", "Chrome/43.0.2357.134 Safari/537.36")
settings.set("LOG_ENABLED", False)
settings.set("ROBOTSTXT_OBEY", True)
process = None

def get_option(message: str):
    message += ">"
    while True:
        strinput = input(message)
        if (strinput == ""):
            print("No option specified , please try again ")
            continue
        else:
            try:
                option = int(strinput)
            except ValueError:
                print("Invalid option please inter a decimal number")
                continue
            return option

def get_total_domains():
    sqlite = SQLite()
    total_links = sqlite.select_collected_domains()
    total = []
    for link in total_links: total.append(link[0])
    return  total



def get_sqlite_rsschannels():
    sqlite = SQLite()
    sqlite_rss_channels = []
    data = sqlite.select_rss_channels()
    for info in data:
        sqlite_rss_channels.append(RssChannel(url=info[0],domain=info[1],last_update=info[2]))
    return sqlite_rss_channels




MAIN_MENU = "\n *********** MAIN MENU ************\n 1) START CRAWLING\n 2) PRINT SQLITE CHANNELS LINKS.\n 3) STOP CRAWLING.\n 4) EXIT.\n ********** END MENU ***********\n"

if __name__ == '__main__':
    system("cls")
    print(MAIN_MENU)
    sqlite_channels = get_sqlite_rsschannels()
    option = get_option("YOUR OPTION (DECIMAL NUMBER)")
    while option != 4:
        if option == 1:
            system("cls")
            sqlite_channels = get_sqlite_rsschannels()
            total_domains = get_total_domains()
            if sqlite_channels == []:
                print("!! ENABLE TO EXECTURE RSS CHANNELS SPIDER (LINKS ARRAY IS EMPTY)!!")
                input("PRESS ANY KEY TO CONTINUE ...")
                continue
            much = get_option("HOW MUCH DOMAIN YOU WANT TO CRAWL (0.." + str(len(sqlite_channels)) + ")")
            sqlite_channels = sqlite_channels[0:much]
            process = CrawlerProcess(settings=settings)
            process.crawl(RssChannelsSpider,sqlite_channels,get_total_domains())
            process.start()
            print("END CRAWLING FOR ", len(sqlite_channels))
            input("PRESS ANY KEY TO CONTINUE ....")
            break
        elif option == 2:
            sqlite_channels = get_sqlite_rsschannels()
            system("cls")
            counter = 0
            for link in sqlite_channels:
                counter += 1
                print("TOTAL : ", link.url)
                if counter % 10 == 0:
                    pt = get_option("PRINT MORE (1) OR IGNIORE (0) ?")
                    if pt == 0: break
            print(counter, "/", len(sqlite_channels), "  DATA PRINTED")
            input("Press any key to continue ...")

        elif 3:
            if process:
                process.stop()
            else:
                print("NO PROCESS IS RUNNING.")
            input("PRESS ANY KEY TO CONTINUE...")

        system("cls")
        print(MAIN_MENU)
        option = get_option("YOUR OPTION (DECIMAL NUMBER)")

    print("\n****  END CRAWLING , GOOD BYE :) **** \n")
    input("PRESS ANY KEY TO CONTINE...")
    if process != None:
        system("python rsschannels_spider_runner.py")
