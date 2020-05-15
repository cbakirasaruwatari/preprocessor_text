#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# base
import os
import sys
import configparser
import mysql.connector as mydb

class PersitenceDatabaseConnector:
  _CFG_PATH:str = './resource/settings/db.cfg'
  errors = mydb.errors
  def __init__(
                self,
                db_name: str
              ):

    # if os.path.isfile(self._CFG_PATH) is False:
    #     raise FileNotFoundError
    # cfg = configparser.SafeConfigParser(os.environ)
    # cfg.read(self._CFG_PATH)

    self.__host="twitter-persistent-db"
    self.__port=3306
    self.__user="root"
    self.__password="mysql"
    self.__database=db_name

  def connect(self):
    self.conn = mydb.connect(
      host=self.__host,
      port=self.__port,
      user=self.__user,
      password=self.__password,
      database=self.__database
    )
    self.cursor = self.conn.cursor()
  def close(self):
    self.conn.close()
    self.cursor.close()
  def commit(self):
    self.conn.commit()   
  def rollback(self):
    self.conn.rollback()

if __name__ == "__main__":
  db = PersitenceDatabaseConnector("twitter")
  db.connect()