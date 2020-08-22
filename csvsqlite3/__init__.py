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

from xml.dom import minidom

home = os.getenv("USERPROFILE")
# dldir = os.path.join(home,"Downloads")
s3url = "https://s3.amazonaws.com/irs-form-990/"
#filename = glob.glob(os.path.join(dldir,"irs charity 990", "index2019"))[0]


def first_tagval_ifany(tagname):
    'throw exception if length not in 0..1'
    desc = dom.getElementsByTagName(tagname)
    
    if len(desc) > 0:
        for line in desc:
            print(line.firstChild.nodeValue)
        # print (desc[0].firstChild.nodeValue)
        # return(desc[0].firstChild.nodeValue)
def save_xml_to_file(object_id):
    fname = s3url +   "_public.xml"
    print(fname)
    u = urllib.request.urlopen(fname)
    v = u.read()
    with open(x['OBJECT_ID'],'wb') as outfile:
        outfile.write(v)
def get_matching_orgs(orgname,saveorg=None):
    'gets matching charities, writes their xml files to disk'
    search = re.compile(orgname,re.IGNORECASE)
    # print(os.listdir(filename))
    f = open(filename,"r",encoding="utf-8-sig")
    reader = csv.DictReader(f)
    print("names: {}".format(reader.fieldnames))
    
    for x in reader:
        if search.search(x["TAXPAYER_NAME"]):
            if saveorg != None:
                saveorg(x['OBJECT_ID'])
            print(x["TAXPAYER_NAME"])
            
            
def show_data():
    """prints the name, description, and website of all the files
    in the directory that end with a digit
    """

    files = glob.glob("*[0-9]")
    for x in files:
        print("=========================")
        infile = open(x, encoding="utf-8-sig")
        dom = minidom.parse(infile)
        name = first_tagval_ifany("BusinessNameLine1Txt")
        desc = first_tagval_ifany("ActivityOrMissionDesc")
        website = first_tagval_ifany("WebsiteAddressTxt")


class tablemaker(object):
    def __init__(self, databasefilename):
        self.db = sqlite3.connect(databasefilename)
        self.cursor = self.db.cursor()
        
    
    def save_to_database(self,filename,tablename = None):
        
        f = open(filename,"r",encoding="utf-8-sig")
        reader = csv.DictReader(f)
        if tablename == None:
            tablename = os.path.basename(filename)
        # pdb.set_trace()
        self.cursor.execute("drop table IF EXISTS {};".format(tablename))
    
        fl = ",".join(['"{}" TEXT'.format(i) for i in reader.fieldnames])
        # print(fl)
        create_statement = "create table {} ({});".format(tablename,fl)
        self.cursor.execute(create_statement)
        self.db.commit()
        print(create_statement)
        for x in reader:
            vals =tuple(x.values())
            # pdb.set_trace()
            # print (vals)
            inserter = ",".join(len(vals) * "?")
            
            self.cursor.execute("insert into {} values ({})".format(tablename,inserter), vals)
        
        self.db.commit()
if __name__ == "__main__":
    start = time.time()
    tbl = tablemaker("blah2348977928347592834")
    tbl.save_to_database(filename)
    print("elapsed: {}".format(time.time() - start))