#! /usr/bin/python
''' looks quite useless, as it doesn't use CSV library'''
import os
import sqlite3
import pdb
import re
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
load data local infile '%s'
  into table %s
  fields TERMINATED BY ','
#   OPTIONALLY ENCLOSED BY '"' was from Unitrans/makeloaders.py
  lines TERMINATED BY '\\r\\n'
  ignore 1 lines;

""" % (tname,  all_fields, filename,tname)
  print u
if __name__ == "__main__":
  print "# this output created by the makeloaders.py script"
  print "create database if not exists unitrans;"
  print "use unitrans"
  for i in os.listdir("."):
     if i.endswith(".txt"):
	load_file(i)


