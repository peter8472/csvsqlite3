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
from collections import OrderedDict

from xml.dom import minidom

def print_column(filename, colnum, num=10):
    'print out the nth codlum of n rows of the table'
    infile = open(filename)
    reader=csv.reader(infile)
    for x in range(0,num):
        print(next(reader)[colnum])
   
def count_headers(filename):
    infile = open(filename)
    reader=csv.reader(infile)
    cols = next(reader)
    return len(cols)

class Schema():
    'inputs and outputs schemas from various formats'
    def __init__(self, fieldnames=None, datatypes=None, deftype='TEXT'):
        if fieldnames != None:
            self.fields = OrderedDict.fromkeys(fieldnames, value=deftype)
        elif datatypes != None:
            fnames = ["field{}".format(i) for i in range(len(datatypes))]
            self.fields = OrderedDict(zip(fnames, datatypes))
    def to_create(self):
        ray = []
        for x in self.fields.keys():
            ray.append("{} {}".format(x,self.fields[x]))
        return ",".join(ray)
    def get_fieldnames(self):
        return self.fields.keys()
    def set_type(self, fieldname, fieldtype):
        if not fieldname in self.fields.keys():
            
            raise KeyError
        self.fields[fieldname] = fieldtype






def first_tagval_ifany(tagname):
    'throw exception if length not in 0..1'
    desc = dom.getElementsByTagName(tagname)
    
    if len(desc) > 0:
        for line in desc:
            print(line.firstChild.nodeValue)
        # print (desc[0].firstChild.nodeValue)
        # return(desc[0].firstChild.nodeValue)


class Tablemaker(object):
    '''
    
    '''
    def __init__(self, databasefilename, dialect=None):
        'call with name of file in which to store the database'
        'then call save_to_database with optinoal column names'
        self.db = sqlite3.connect(databasefilename)
        self.cursor = self.db.cursor()
        if dialect != None:
            self.dialect = dialect
        else:
            self.dialect = csv.excel
        
        
    def drop_table(self, tablename = None):
        if tablename == None:
            tablename = os.path.basename(filename)

        self.cursor.execute("drop table IF EXISTS {};".format(tablename))
        self.db.commit()
    def save_to_database(self,filename,tablename = None, encoding = "utf-8-sig",
        colnames=None, drop=False, fieldstring=None, infile=None,schema=None):
        assert colnames == None or fieldstring == None # can't give both
        if infile==None:
            infile = open(filename,"r",encoding=encoding)
        myfieldnames = None
        if schema !=None:
            myfieldnames = list(schema.get_fieldnames())
        
        reader= csv.DictReader(infile, dialect=self.dialect, fieldnames=myfieldnames)
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
        if schema != None:
            fl = schema.to_create()
        
        create_statement = "create table if not exists {} ({});".format(tablename,fl)
        self.cursor.execute(create_statement)
        self.db.commit()
        print(create_statement)
        for x in reader:
            vals =tuple(x.values())
            inserter = ",".join(len(vals) * "?")
            self.cursor.execute("insert into {} values ({})".format(tablename,inserter), vals)
        
        self.db.commit()
    def add_data(self,filename,tablename = None,encoding = "utf-8-sig", skip_lines=1):
    
        f = open(filename,"r",encoding=encoding)
        reader = csv.DictReader(f)
        for x in range(0, skip_lines):
            next(reader ) # skip
    
        if tablename == None:
            
            print("you must give a tablename for add_data")
            return
        for x in reader:
            vals =tuple(x.values())
            inserter = ",".join(len(vals) * "?")
            self.cursor.execute("insert or ignore into {} values ({})".format(tablename,inserter), vals)
        
        self.db.commit()

if __name__ == "__main__":
    
    start = time.time()
    
    
    print("elapsed: {}".format(time.time() - start))
    print("this library no longer has a __main__ function")
    