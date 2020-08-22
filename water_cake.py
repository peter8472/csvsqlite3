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
        


def query3(filename, serving_size = 15.0, nutrient="sodium"):
    t1 = Timer()
    db = sqlite3.connect(filename)
    cur = db.cursor()
    t2 = Timer()
    cur.execute("""create temporary table foodlist as 
    select fdc_id,description from food 
     where description like '%rice%cakes%'  
      ;
    """)
    # patterns = ["bread,%wheat%", "rice%raw%", "%saltines%"]
    patterns = ['%rice%paper%']
    for x in patterns:
        
        cur.execute("""insert into foodlist  select fdc_id,description
            from food  where description like '{}';""".format(x))
    
    # lookup the nutrient
    cur.execute("""
    create temporary table nutlist as
    
        select * from nutrient where name like '{}'
    """.format(nutrient))

    cur.execute("""create temporary table temp as 
    select * from food_nutrient inner join foodlist using(fdc_id) 
    inner join nutlist on nutlist.id == food_nutrient.nutrient_id

      
      
      ;
    """)
    for x in ['%breading%', '%breadfruit%', '%breaded%',
                'shortening bread%','fast foods%','SUBWAY, %']:
        
        cur.execute("delete from  temp where description  like '{}';".format(x))
    
    
    

    
    cur.execute("select description,amount from temp ;")
    
    rows = cur.fetchall()
    for i in rows:
        print(i)
        

def runtest(db_name, callback):
    t = Timer()
    callback(db_name)
    t.print("{} {}".format(db_name, callback))
    
def getdesc(filename):
    t1 = Timer()
    db = sqlite3.connect(filename)
    cur = db.cursor()
    t2 = Timer()
    cur.execute("""
    select *  from food 

      where description like '%keebler%export%' or 
      description like  '%premium%cracker%mini%' or
      description like  '%premium%cracker%mini%' or 
      description like  '%salti%market%pantry%' 
      limit 100
      ;
    """)
    

    
    
    rows = cur.fetchall()
    for i in rows:
        print(i)
    
    
if __name__ == "__main__":
    
    
    query3("newdb",  serving_size=14, nutrient="water")

    