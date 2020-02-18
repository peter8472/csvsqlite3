#! /usr/bin/python
import sqlite3
import pdb
# this program load the file data_types into the database types.sqlite3




def isin(db, val):
   u = db.execute("select * from types where name = '%s';" % (val))
   if u.rowcount == -1:
      return False
   else:
      return True
   
fi = open("data_types")
b = fi.readlines()
b = [i.strip() for i in b]
b = [i.replace(",", "") for i in b]
db = sqlite3.connect("types.sqlite3")
db.execute("create table if not exists types (name varchar(30)  , type varchar(30));")
for k in b:
  u = k.split(" ")
  if isin(db, u[0]) ==  False:
    try:
      j = db.execute("insert into types values ('%s', '%s');" % tuple(u))
      print "insert into types values ('%s', '%s');" % tuple(u)
    except sqlite3.IntegrityError, mess:
      print mess, tuple(u)
      exit()

db.commit()

