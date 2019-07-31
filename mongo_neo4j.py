import os
import re
import sys
import time
import json
import pprint
from selenium import webdriver
from datetime import datetime
from datetime import date
from pymongo import MongoClient
from neo4j import GraphDatabase

# Mongo DB fuctions
def mongodb_init():
    client=MongoClient('mongodb://34.73.180.107:27017')
    db=client.smartcareer
    return db

def mongodb_get_collection(db,item):
    col=db[item]
    return col

def mongodb_put_doc(doc):
    db=mongodb_init()
    col=mongodb_get_collection(db,'jobdescription')

    try:
        global docNum
        re=col.insert_one(doc)
        ret=re.inserted_id
        docNum += 1
    except:
        ret=doc['JobID']
          
    return ret

def mongodb_read_docs(col):
    db=mongodb_init()
    col=mongodb_get_collection(db,col)

    try:

        ret=col.find().limit(500)
        
    except Exception as e:
        print(e)
          
    return ret

# Neo4j Functions
def neo4j_init():
    # uri = "bolt://34.66.112.119"
    # userName = "neo4j"
    # passwd = "SmartCareer0!"
    uri = "bolt://localhost"
    userName = "neo4j"
    passwd = "Random1234"
    ndb=GraphDatabase.driver(uri, auth=(userName,passwd))
    return ndb

def neo4j_read(neoObj,cqlNode):
    grapDB=neoObj

    try:
        with grapDB.session() as tx:
            ret=tx.run(cqlNode)

        
    except Exception as e:
        print(e)
          
    return ret

def neo4j_merge(neoObj,cqlNode):
    grapDB=neoObj

    try:
        with grapDB.session() as tx:
            ret=tx.run(cqlNode)

        
    except Exception as e:
        print(e)
          
    return ret

def clean_item(item):
    item = item.replace('\n', ' ')
    item = item.strip()
    return item

def write_log(msg):
    logf=open("smartcareer.log","w")
    ret=logf.write(msg)
    return ret


if "__main__":

    print("Starting")
    docs=mongodb_read_docs('jobdescription')
    graphDB = neo4j_init()

    for d in docs:
        jobTitle=d['Job Title'].replace("'","")
        company=d['Company'].replace("'","")
        location=d['Location'].replace("'","")
        
        if location is "":
           location = "Not Specified"
        else:
           location = d['Location'].replace("'","")

        seniority=d.get('Seniority Level')

        if seniority is None:
            seniority = "Not Specified"
        else:
            seniority = d['Seniority Level'].replace("'","")

        industry=d.get('Industry')
        
        if industry is None:
            industry = "Not Specified"
        else:
            industry=d['Industry'].replace("'","")
        
        try:
            employmentType=d['Employment Type']
        
        except:
            continue

        try:
            jobFunction=d['Job Functions'].replace("'","")

        except:
            continue

        cqlNode="""Merge (j:`Job Title` {Name:'%s', Seniority:'%s', Job_Functions:'%s', Employment_Type:'%s'})
                 Merge (c:`Company` {Name:'%s',  Industry:'%s'})
                 Merge (l:`Location` {Name:'%s'})
                 Merge (c)-[:POSTED]->(j)
                 Merge (l)-[:HASJOB]->(j)""" % (jobTitle,seniority,jobFunction,employmentType,company,industry,location)

        try:
            ret=neo4j_merge(graphDB,cqlNode)
        except Exception as e:
            write_log(str(e))         
            continue

        print("Neo4j inserted: %s" % ret)

     
    graphDB.close()
    print("completed")