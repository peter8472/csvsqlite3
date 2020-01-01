#! /usr/bin/python
""" I'm going to try to make a loader that does not call local infile
because that is really iffy with not turning blank fields into null
fields.  the create statements are in tbcreate for now.

"""
import os
import sqlite3
import pdb
import re
#import MySQLdb not always available
import datetime # stupid mysqldb!
import sys
import csv

class testjunk():
    def execute(self,str):
        print str

def load_file(filename):
  typedb = sqlite3.connect("types.sqlite3")
  all_fields = ""
  tmp_fields = ""
  tname = filename.replace(".txt", "",1)
  fd = open(filename, "r")
  headstr = fd.readline().rstrip()
  tmp_fields = headstr.split(",")
  vals = fd.readline().rstrip()
  vlist = vals.split(",")
  vlist = [i if i is not "" else "\n" for i in vlist]
  vjoined = ",".join(vlist)
  pdb.set_trace()
  cur = testjunk()
  cur.execute("insert into %s (%s) values (%s)" % 
	(tname, headstr, vjoined))





if __name__ == "__main__":
  print "# this output created by the makeloaders.py script"
  print "create database if not exists unitrans;"
  print "use unitrans"
  for i in os.listdir("."):
     if i.endswith(".txt"):
	load_file(i)

