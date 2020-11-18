from os import system
from sys import argv

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.settings import Settings

from DataBase import SQLite
from Spiders import WebSitesSpider

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


def get_waiting_domains():
    sqlite = SQLite()
    return sqlite.select_collected_domains(state=0)


def get_total_domains():
    sqlite = SQLite()
    return sqlite.select_collected_domains()


MAIN_MENU = "\n *********** MAIN MENU ************\n 1) START CRAWLING\n 2) PRINT TOTAL LINKS.\n 3) PRINT STARTING LINKS.\n 4) STOP CRAWLER PROCESS\n 5) EXIT.\n ********** END MENU ***********\n"

if __name__ == '__main__':
    system("cls")
    total_links = get_total_domains()
    print(MAIN_MENU)
    option = get_option("YOUR OPTION (DECIMAL NUMBER)")
    while option != 5:
        if option == 1:
            system("cls")
            links = get_waiting_domains()
            total_links = get_total_domains()
            if links == []:
                print("!! ENABLE TO EXECTURE WEBSITES SPIDER (LINKS ARRAY IS EMPTY)!!")
                input("PRESS ANY KEY TO CONTINUE ...")
                continue
            if total_links == []:
                print("!! ENABLE TO EXECTURE WEBSITES SPIDER (TOTAL LINKS ARRAY IS EMPTY) !!")
                input("PRESS ANY KEY TO CONTINUE ...")
                continue
            start_urls = []
            for link in links: start_urls.append(link[0])
            total = []
            for link in total_links: total.append(link[0])
            much = get_option("HOW MUCH DOMAIN YOU WANT TO CRAWL (0.." + str(len(start_urls)) + ")")
            start_urls = start_urls[0:much]
            spider = WebSitesSpider(start_urls=start_urls, total_external_links=total)
            process = CrawlerProcess(settings=settings)
            process.crawl(WebSitesSpider,start_urls,total)
            process.start()
            print("END CRAWLING FOR ", len(start_urls))
            input("PRESS ANY KEY TO CONTINUE ....")
            break
        elif option == 2:
            total_links = get_total_domains()
            system("cls")
            counter = 0
            for link in total_links:
                counter += 1
                print("TOTAL : ", link[0])
                if counter % 10 == 0:
                    pt = get_option("PRINT MORE (1) OR IGNIORE (0) ?")
                    if pt == 0: break
            print(counter, "/", len(total_links), "  DATA PRINTED")
            input("Press any key to continue ...")
            break


        elif option == 3:
            system("cls")
            waiting_links = get_waiting_domains()
            counter = 0
            for link in waiting_links:
                print("WAITING : ", link[0])
                counter += 1
                if counter % 10 == 0:
                    pt = get_option("PRINT MORE (1) OR IGNIORE (0) ?")
                    if pt == 0: break
            print(counter, "/", len(waiting_links), "  DATA PRINTED")
            input("Press any key to continue ...")
        elif 4:
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
        system("python websites_spider_runner.py")
