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


class Timer(object):
    def __init__(self):
        self.start = time.time()
    def print(self, message=""):
        print("{} {}".format(message,time.time() - self.start))
    def end(self):
        return time.time() - self.start
        

def query1(filename):
    '''unnecessary inner join with branded food database, which had
    no special information.
    '''
    t1 = Timer()
    db = sqlite3.connect(filename)
    cur = db.cursor()
    cur.execute("""create temporary table oyster as select * from "food" inner join 
    "branded_food" using (fdc_id) where 
    description like '%soup%oyster%';""")
    # t1.print("food inner join branded where description like soup...")
    t2 = Timer()
    

    cur.execute("create temporary table tempnut as select * from food_nutrient inner join oyster using(fdc_id)")
    # t2.print('select * from food_nutrient inner join oyster using(fdc_id)')

    cur.execute( """
    select brand_owner,description,tempnut.amount from nutrient inner join tempnut on tempnut.nutrient_id = nutrient.id
     where nutrient.name like '%sodium%' order by cast(amount as float);""")
    

    
    rows = cur.fetchall()
    for i in rows:
        print(i[0], i[1],(float(i[2]) * (15.0/ 100)))
    

def query2(filename):
    t1 = Timer()
    db = sqlite3.connect(filename)
    cur = db.cursor()
    t2 = Timer()
    cur.execute("""create temporary table tempnut as 
    select * from food_nutrient inner join food using(fdc_id) 
    where description like '%oyster%crackers%'
      or description like '%cracker%oyster%' ;
    """)
    # t2.print('select * from food_nutrient inner join oyster using(fdc_id)')

    cur.execute( """
    create temporary table beforebranding as 
    
    select fdc_id,description,tempnut.amount,food_category_id from 
        nutrient inner join tempnut on tempnut.nutrient_id = nutrient.id
     where nutrient.name like '%sodium%' order by cast(amount as float);""")
    cur.execute("""
    select brand_owner,description,amount,food_category_id 
    from beforebranding  inner join branded_food using (fdc_id)
    """) 
    rows = cur.fetchall()
    for i in rows:
        print("{}\t{}\t{:.0f}\t{}".format(i[0],i[1], (float(i[2])) * (15.0/ 100),i[3]))

def runtest(db_name, callback):
    t = Timer()
    callback(db_name)
    t.print("{} {}".format(db_name, callback))
    
if __name__ == "__main__":
    # runtest("newdb", query1) slower...
    
    runtest("newdb", query2)

    