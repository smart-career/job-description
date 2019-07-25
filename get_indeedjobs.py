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

# Global Variable
docNum = 0

# REPLACE With your LinkedIn Credentials
USERNAME = ""
PASSWORD = ""

def mongodb_init():
    client=MongoClient('mongodb://34.73.180.107:27017')
    db=client.smartcareer
    return db

def mongodb_get_collection(db,item):
    col=db[item]
    return col

def mongodb_put_doc(doc):
    db=mongodb_init()
    col=mongodb_get_collection(db,'indeedjobdescription')

    try:
        global docNum
        re=col.insert_one(doc)
        ret=re.inserted_id
        docNum += 1
    except:
        ret=doc['JobID']
          
    return ret

def clean_item(item):
    item = item.replace('\n', ' ')
    item = item.strip()
    return item


def generate_scrape_url(scrape_url, jobList, configArray):

 #   print('1. Since last visit')
 #   print('2. Past Week')
 #   print('3. Past Month')
 #   print('4. Anytime')
    title = jobList
    period = int(configArray[0])

    while not 0 < int(period) < 5:
        print('\nERROR: Invalid Input. Try again.')
        period = input("Period: ")

    scrape_url += "q="
    scrape_url += title
    scrape_url += '&l=United States'
    if period == 1:
        scrape_url += '&fromage=last'
    elif period == 2:
        scrape_url += '&f_TPR=r604800'
    elif period == 3:
        scrape_url += '&f_TPR=r2592000'

    valid_title_name = title.strip().replace(' ', '_')
    valid_title_name = re.sub(r'(?u)[^-\w.]', '', valid_title_name)

    return scrape_url

def scrape(jobList, configArray):
    chrome_driver = os.getcwd() + "/chromedriver.exe"
    base_url = "https://indeed.com/jobs?"
    main_obj = {}
    all_jobs = []
    job_postings = []
    page = 1
    jCount = 0

    job_search_url = generate_scrape_url(base_url, jobList, configArray)

    print('\nSTATUS: Opening website')
    browser = webdriver.Chrome(chrome_driver)
    time.sleep(2)

    print('STATUS: Searching for jobs\n')
    browser.get(job_search_url)
    jobs = browser.find_elements_by_class_name('result-card__full-card-link')

    if len(jobs) == 0:
        jobs = browser.find_elements_by_xpath("//*[@id='resultsCol']")
        print("Opened resultsCol")

        if len(jobs) == 0:
            jobs = browser.find_elements_by_xpath("//id[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")
            print("opened jobsearch-SerpJobCard")
            if len(jobs) == 0:
                print('STATUS: No jobs found. Press any key to exit scraper')
                browser.quit()
                print("Check docnum.txt for # of documents submitted!")
                today = datetime.now()
                f = open("docnum.txt","w+")
                f.write("Ran:\n")
                f.write(str(today))
                f.write("\n")
                f.write("\nNumber of documents submitted:\n")
                f.write(str(docNum))
                f.close()
                exit = input('')
                sys.exit(0)

    all_jobs = jobs

    #Scrapes until the list of jobs is exhausted.
    while True:
        print('STATUS: Scraping Page ' + str(page))
        index = 0
        while index < len(jobs):
            obj = {}
            job = jobs[index]

            job.click()
            time.sleep(2)

            current_url = browser.current_url
            job_id = current_url[current_url.find('currentJobId=') + 13: current_url.find('currentJobId=') + 23]
            dateCaptured = str(date.today())
            obj['JobID'] = job_id
            obj['Date Captured'] = dateCaptured

            job_div = None
            while True:
 
                try:
                    job_div = browser.find_element_by_xpath("//*[@id='vjs-container']")
                    break
                except:
                    time.sleep(1)
                    browser.execute_script("window.history.go(-1)")
                    break


            try:
                job_title = clean_item(job_div.find_element_by_xpath("//*[@id='vjs-jobtitle']").text)
                obj['Job Title'] = job_title
            except:
                obj['Job Title'] = ''

            try:
                company = clean_item(job_div.find_element_by_xpath("//*[@id='vjs-cn']").text)
                obj['Company'] = company
            except:
                obj['Company'] = ''

            try:
                location = clean_item(job_div.find_element_by_xpath("//*[@id='vjs-loc']").text)
                obj['Location'] = location
            except:
                obj['Location'] = ''

            try:
                reviews = clean_item(job_div.find_element_by_xpath("//span[@class= 'slNoUnderline']").text)
                obj['reviews'] = reviews
            except:
                obj['reviews'] = ''

            try:
                description = clean_item(job_div.find_element_by_xpath("//*[@id='vjs-desc']").text)
                obj['Description'] = description
            except:
                obj['Description'] = ''

            doc_id=mongodb_put_doc(obj)
            print('post id: ', doc_id)

            jobs = browser.find_elements_by_xpath("//id[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")
            index += 1

        next_page = job_search_url + '&start=' + str(page*10)
        browser.get(next_page)
        page += 1
        time.sleep(5)
        jobs = browser.find_elements_by_xpath("//id[@class='jobsearch-SerpJobCard unifiedRow row result clickcard']")

        if len(jobs) == 0:
            break
    
    browser.quit()
  

if "__main__":
    # Reads in the config file so input is automatic.
    with open("cfg.txt") as newFile:
        configArray = newFile.readlines()

    jobList = []
    tempStr = ""

    while len(configArray) > 0:
        try:
            int(configArray[0])
            break
        except:
            jobList.append(configArray[0])
            del configArray[0]

    # Searches multiple jobs in a row.
    for x in range(len(jobList)):
        print("Now scraping:", jobList[0])
        scrape(jobList[0], configArray)
        time.sleep(5)
        del jobList[0]

    print("Daily automation has been completed for: get_jobs.py")
    print("Check docnum.txt for # of documents submitted!")
    today = datetime.now()
    f = open("docnum.txt","w+")
    f.write("Ran:\n")
    f.write(str(today))
    f.write("\n")
    f.write("\nNumber of documents submitted:\n")
    f.write(str(docNum))
    f.close()

    sys.exit(0)