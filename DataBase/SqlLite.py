import datetime
import sqlite3
from collections import Iterable
from sqlite3 import Error

import ipdb

RSS_CHANNELS_TABLENAME = "rsschannels"
DOMAINS_TABLENAME = "domains"

class SQLite:
    connexion = None
    db_path = str
    def __init__(self,db_path = "./Storage/localdb.db"):
        self.db_path = db_path
        self.open()

    def open(self):
        if self.connexion:return self
        try:
            self.connexion = sqlite3.connect(self.db_path)
        except Error as error:
            print("OPENING FAILED ",error)
        finally:
            return self

    def insert_collected_domains(self, domains, commit:bool=True):
        args = []
        for domain in domains:
            args.append(domain._array())
        try:
            self.connexion.executemany("INSERT INTO " + DOMAINS_TABLENAME + " values(?,?,?)",args)
        except Error as error:
            print("SQLITE ERROR :" ,error)
        finally:
            if commit: self.connexion.commit()

    def delete_collected_domains(self,domains:Iterable = [],commit:bool=True):
        try:
            if domains == []:self.connexion.execute("DELETE FROM " + DOMAINS_TABLENAME)
            else:
                args=  []
                for domain in domains:
                    args.append([domain])
                self.connexion.executemany("DELETE FROM "  + DOMAINS_TABLENAME +" WHERE domain = ?",args)
        except Error as error:
            print("SQLITE ERROR :" ,error)
        finally:
            if commit: self.connexion.commit()
    def update_collected_domains(self, domains, commit:bool=True):
        args = []
        try:
            for domain in domains:
                args.append([domain.state,domain.last_update,domain.domain])
            self.connexion.executemany("UPDATE domains SET state = ?,last_update=? WHERE domain = ?",args)
        except Error as error:
            print("SQLITE UPDATE DOMAINS ERROR : ",error)
        finally:
            if commit:self.commit()
    def select_collected_domains(self,last_update=None,state=None):
        try:
            self.open()
            sql = "SELECT * FROM " + DOMAINS_TABLENAME
            if state != None:sql += " WHERE state = " + str(state)
            if last_update != None:
                if state: sql += " and last_update = " + str(last_update)
                else:sql += " WHERE state = " + str(state) + " and last_update = " + str(last_update)
            cursor = self.connexion.cursor().execute(sql)
            cursor = cursor.execute(sql)
            return cursor.fetchall()
        except Error as error:
            print("SQLITE ERROR :" ,error)

    def insert_rss_channels(self,rsschannels,commit:bool=True):
        args = []
        for rsschannel in rsschannels:
            args.append(rsschannel._array())
        try:
            self.connexion.executemany("INSERT INTO " + RSS_CHANNELS_TABLENAME + " VALUES ( ?, ? ,? )",args)
        except Error as error:
            print("SQLITE ERROR :" ,error,"=>",args)
        finally:
            if commit: self.connexion.commit()
    def delete_rss_channels(self,rsschannels:Iterable = [],commit:bool=True):
        try:
            if rsschannels == []:self.connexion.execute("DELETE FROM " + RSS_CHANNELS_TABLENAME)
            else:
                args = []
                for rsschannel in rsschannels:
                    args.append([rsschannel.url])
                self.connexion.executemany("DELETE FROM " + RSS_CHANNELS_TABLENAME + " WHERE url = ?",args)
        except Error as error:
            print("SQLITE ERROR :" ,error)
        finally:
            if commit: self.connexion.commit()

    def select_rss_channels(self,withdateupdate:bool=True):
        try:
            if withdateupdate:return self.connexion.cursor().execute("SELECT * FROM " + RSS_CHANNELS_TABLENAME).fetchall()
            else: return self.connexion.cursor().execute("SELECT url FROM " + RSS_CHANNELS_TABLENAME).fetchall()
        except Error as error:
            print("SQLITE ERROR :" ,error)

    def close(self):
        if self.connexion:
            self.connexion.close()
            self.connexion = None
    def commit(self):
        if self.connexion:self.connexion.commit()