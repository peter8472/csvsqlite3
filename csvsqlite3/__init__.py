import pdb
import sys
import csv
import sqlite3
import os
import glob
import re
import urllib.request
import datetime
import time
from pathlib import Path

from xml.dom import minidom

home = os.getenv("USERPROFILE")

s3url = "https://s3.amazonaws.com/irs-form-990/"






def first_tagval_ifany(tagname):
    'throw exception if length not in 0..1'
    desc = dom.getElementsByTagName(tagname)
    
    if len(desc) > 0:
        for line in desc:
            print(line.firstChild.nodeValue)
        # print (desc[0].firstChild.nodeValue)
        # return(desc[0].firstChild.nodeValue)


class tablemaker(object):
    def __init__(self, databasefilename):
        self.db = sqlite3.connect(databasefilename)
        self.cursor = self.db.cursor()
        
    def drop_table(self, tablename = None):
        if tablename == None:
            tablename = os.path.basename(filename)

        self.cursor.execute("drop table IF EXISTS {};".format(tablename))
    def save_to_database(self,filename,tablename = None, 
        colnames=None, drop=False, fieldstring=None):

        
        f = open(filename,"r",encoding="utf-8-sig")
        reader = csv.DictReader(f)
        if tablename == None:
            
            tablename =    os.path.basename(filename).split(".")[0]
        if drop == True:

            self.cursor.execute("drop table IF EXISTS {};".format(tablename))
        myfieldnames = reader.fieldnames
        if colnames != None:
            if len(colnames ) <= len(myfieldnames):
                # too few or just enough

                myfieldnames[0:len(colnames)] = colnames
            else:
                # too many colnames, use only as needed
                myfieldnames = colnames[0:len(myfieldnames)]

    
        fl = ",".join(['"{}" TEXT'.format(i) for i in myfieldnames])
        if fieldstring != None:
            fl = fieldstring
        
        create_statement = "create table if not exists {} ({});".format(tablename,fl)
        self.cursor.execute(create_statement)
        self.db.commit()
        print(create_statement)
        for x in reader:
            vals =tuple(x.values())
            inserter = ",".join(len(vals) * "?")
            self.cursor.execute("insert into {} values ({})".format(tablename,inserter), vals)
        
        self.db.commit()
if __name__ == "__main__":
    
    start = time.time()
    tbl = tablemaker("blah2348977928347592834")
    tbl.save_to_database(filename)
    print("elapsed: {}".format(time.time() - start))