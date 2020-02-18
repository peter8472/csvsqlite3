import boto3
import os
import glob
import subprocess

def mytail(fname,outfilename):
    infile=open(fname)
    outfile = open(outfilename, 'w')
    next(infile) # skip first line
    for x in infile:
        outfile.write(x)
    outfile.close()
    infile.close()
        
    

if __name__ == "__main__":
    os.chdir("nutrient")
    s3 = boto3.client('s3')
    files = glob.glob("*.csv")
    for i in files:
        root = os.path.splitext(i)[0]
        if root == "food" or root == "branded_food":
            continue
        obj_name = root + "/1.csv"
        # print(obj_name)
        # s3.upload_file(root,'przwy-food',obj_name)
        