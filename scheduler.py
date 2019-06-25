# This program will activate the script to run once a day.
import os
import schedule
import time

def script():
    os.system('python get_jobs.py')

schedule.every().day.do(script)

while 1:
    schedule.run_pending()
    time.sleep(1)