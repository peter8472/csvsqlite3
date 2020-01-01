#! /usr/bin/python
""" 
This is tbcreate, a mostly working copy of tbload.  I am putting this
here to get it out of the way.  If it is to be used, it must create
primary keys for django.
"""
import os
import sqlite3
import pdb
import re
import csv

def create_table(filename):
  'commenting out the types stuff, which was designed for pygtfs
  typedb = sqlite3.connect("types.sqlite3")
  all_fields = ""
  tmp_fields = ""
  tname = filename.replace(".txt", "",1)
  fd = open(filename, "r")
  headstr = fd.readline().rstrip()
  tmp_fields = headstr.split(",")

  for i in tmp_fields:
    ty =     typedb.execute("select type from types where name = '" +
	i+"';")#    if ty.rowcount == -1: rowcount doesn' twork with select
    rows = ty.fetchall()
    
    if len(rows) != 1:
      print "missing or extra data type %s" % i
      pdb.set_trace()    
    all_fields = all_fields + "%s %s,\n" % ( i, rows[0][0])
  
  all_fields = re.sub(",$", "", all_fields)

  dropper = "drop table if exists %s;" % tname
  print dropper
  u = """
create table if not exists %s(
%s
);
""" % (tname,  all_fields)
  print u

def load_file(filename):
  typedb = sqlite3.connect("types.sqlite3")
  all_fields = ""
  tmp_fields = ""
  tname = filename.replace(".txt", "",1)
  fd = open(filename, "r")
  headstr = fd.readline().rstrip()
  tmp_fields = headstr.split(",");
  for i in tmp_fields:
    ty =     typedb.execute("select type from types where name = '" +
	i+"';")#    if ty.rowcount == -1: rowcount doesn' twork with select
    rows = ty.fetchall()
    
    if len(rows) != 1:
      print "missing or extra data type %s" % i
      pdb.set_trace()    
    all_fields = all_fields + "%s %s,\n" % ( i, rows[0][0])
  
  all_fields = re.sub(",$", "", all_fields)

  dropper = "drop table if exists %s;" % tname
  print dropper
  u = """
create table if not exists %s(
%s
);
""" % (tname,  all_fields)
  print u
if __name__ == "__main__":
  print "# this output created by the makeloaders.py script"
  print "create database if not exists unitrans;"
  print "use unitrans"
  for i in os.listdir("../nutrient"):
     if i.endswith(".csv")
     print(i)
	#create_table(i)


