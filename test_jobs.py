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

def mongodb_put_doc(col,doc):
    db=mongodb_init()
    col=mongodb_get_collection(db,col)

    try:
        global docNum
        re=col.insert_one(doc)
        ret=re.inserted_id
        docNum += 1
    except:
        ret=doc['JobID']
          
    return ret

def mongodb_update_doc(col,doc):
    db=mongodb_init()
    col=mongodb_get_collection(db,col)

    try:
        global docNum
        re=col.update_one(doc,doc, {upsert==True})
        ret=re.upserted_id
        docNum += 1
    except:
        ret=doc['JobID']
          
    return ret

def clean_item(item):
    item = item.replace('\n', ' ')
    item = item.strip()
    return item


def generate_scrape_url(scrape_url, config):


    title = config['Job Title']
 #   print('\nSelect period from the given options. Type 1, 2, 3 or 4 and press ENTER')
 #   print('1. Past 24 Hours')
 #   print('2. Past Week')
 #   print('3. Past Month')
 #   print('4. Anytime')
    period = int(config['Period'])
 

    while not 0 < int(period) < 5:
        print('\nERROR: Invalid Input. Try again.')
        period = input("Period: ")

    scrape_url += title
    if period == 1:
        scrape_url += '&f_TPR=r86400'
    elif period == 2:
        scrape_url += '&f_TPR=r604800'
    elif period == 3:
        scrape_url += '&f_TPR=r2592000'

    scrape_url += '&location=United States'

    valid_title_name = title.strip().replace(' ', '_')
    valid_title_name = re.sub(r'(?u)[^-\w.]', '', valid_title_name)

    return scrape_url

def scrape(config):
    chrome_driver = os.getcwd() + "/chromedriver.exe"
    base_url = "https://www.linkedin.com/jobs/search?keywords="
    sign_in_url = "https://www.linkedin.com/uas/login?fromSignIn=true"
    main_obj = {}
    all_jobs = []
    job_postings = []
    page = 1
    jCount = 0
    USERNAME = config['User Name']
    PASSWORD = config['Password']
    col=config['Collection']

    job_search_url = generate_scrape_url(base_url, config)

    print('\nSTATUS: Opening website')
    browser = webdriver.Chrome(chrome_driver)
    browser.get(sign_in_url)
    time.sleep(2)

    print('STATUS: Signing in')
    browser.find_element_by_id('username').send_keys(USERNAME)
    time.sleep(2)

    browser.find_element_by_id('password').send_keys(PASSWORD)
    time.sleep(2)

    browser.find_element_by_class_name('login__form_action_container ').click()
    time.sleep(2)

    print('STATUS: Searching for jobs\n')
    browser.get(job_search_url)
   
    jobs = browser.find_elements_by_class_name('search-result-card__link')

    if len(jobs) == 0:
   
        jobs = browser.find_elements_by_class_name('jobs-search-result-item')

        if len(jobs) == 0:
            jobs = browser.find_elements_by_xpath("//li[@class='occludable-update artdeco-list__item--offset-4 artdeco-list__item p0 ember-view']")
            
            if len(jobs) == 0:
                print('STATUS: No jobs found. Press any key to exit scraper')
                browser.quit()
                print("Check docnum.txt for # of documents submitted!")
                today = datetime.now()
                f = open("docnum.txt","w+")
                f.write("Ran:", str(today))
                f.write("Number of documents submitted:", (docNum))
                f.close()
                exit = input('')
                sys.exit(0)

    all_jobs = jobs

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
                    job_div = browser.find_element_by_xpath("//div[@class='job-view-layout jobs-details ember-view']")
                    break
                except:
                    time.sleep(1)
                    browser.execute_script("window.history.go(-1)")


            try:
                job_title = clean_item(job_div.find_element_by_xpath("//h1[@class='jobs-details-top-card__job-title t-20 t-black t-normal']").text)
                obj['Job Title'] = job_title
            except:
                obj['Job Title'] = ''

            try:
                salary = clean_item(job_div.find_element_by_xpath("//p[@class='salary-main-rail__data-amount t-24 t-black t-normal']").text)
                obj['Salary'] = salary
            except:
                obj['Salary'] = 'Not Available'

            try:
                company = clean_item(job_div.find_element_by_xpath("//a[@class='jobs-details-top-card__company-url ember-view']").text)
                obj['Company'] = company
            except: 
                obj['Company'] = ''

            try:
                job_size = job_div.find_elements_by_class_name("jobs-details-job-summary__text--ellipsis")
                size = clean_item((job_size[2]).text)
                obj['Size'] = size
            except:
                obj['Size'] = ''

            try:
                location = clean_item(job.find_element_by_xpath("//span[@class='job-card-search__location artdeco-entity-lockup__caption ember-view']").text)
                obj['Location'] = location
            except:
                obj['Location'] = ''

            try:
                description = clean_item(job_div.find_element_by_xpath("//div[@class='display-flex justify-space-between mb1']/following-sibling::span").text)
                obj['Description'] = description
            except:
                obj['Description'] = ''

            other_fields_list = job_div.find_element_by_id('job-details').find_elements_by_class_name('jobs-box__group')

            for list_item in other_fields_list:
                field_name = list_item.find_element_by_tag_name('h3').text
                field_text = list_item.text.replace(field_name, '')

                field_name = clean_item(field_name)
                field_text = clean_item(field_text)

                obj[field_name] = field_text

            doc_id=mongodb_put_doc(col,obj)
            # doc_id=mongodb_update_doc(col,obj)
            print('post id: ', doc_id)
 #           job_postings.append(obj)
 #           main_obj['postings'] = job_postings

            jobs = browser.find_elements_by_xpath("//li[@class='occludable-update artdeco-list__item--offset-4 artdeco-list__item p0 ember-view']")
            index += 1

        next_page = job_search_url + '&start=' + str(page*25)
        browser.get(next_page)
        page += 1
        time.sleep(5)
        jobs = browser.find_elements_by_xpath("//li[@class='occludable-update artdeco-list__item--offset-4 artdeco-list__item p0 ember-view']")

        if len(jobs) == 0:
            break
    
    browser.quit()
  

if "__main__":
    # Reads in the config file so input is automatic.
    with open("cfg.json") as json_cfg:
        d = json.load(json_cfg)
        JobTitle=d['Job Title']


    jobList = []
    tempStr = ""

    print("Now scraping:", JobTitle)
    scrape(d)

    # Searches multiple jobs in a row.
    # for x in range(len(jobList)):
    #     print("Now scraping:", jobList[0])
    #     scrape(jobList[0], configArray)
    #     time.sleep(5)
    #     del jobList[0]

    print("Daily automation has been completed for: get_jobs.py")
    print("Check docnum.txt for # of documents submitted!")
    today = datetime.now()
    f = open("docnum.txt","w+")
    f.write("Ran:\n")
    f.write(str(today))
    f.write("\nNumber of documents submitted:\n")
    f.write(str(docNum))
    f.write("\n")
    f.close()

    sys.exit(0)