from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time
import os
from helper_functions import *
from bs4 import BeautifulSoup
import re

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', None) #To display full URL in dataframe

def create_jobsdf_efc(criterion, url, save_to_excel = False):
    '''
    Add function description here
    '''
    os.environ['WDM_LOG_LEVEL'] = '0'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    caps = webdriver.DesiredCapabilities().CHROME.copy()
    caps["pageLoadStrategy"] = "normal"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities = caps, options = option)
    driver.get(url)
    time.sleep(5)

    # Click on 'Show more' button to display all results
    # count = 0
    while True:
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH,
                                                       "//button[@class = 'btn btn-outline btn-small ng-star-inserted']"
                                                       ))
                                            )
            button = driver.find_element(by=By.XPATH,
                                         value="//button[@class = 'btn btn-outline btn-small ng-star-inserted']")
            driver.execute_script("arguments[0].click();", button)
            # count += 1

        except: break

    # Extract required data
    roles = pd.Series(
        [i.get_attribute('title')
         for i in driver.find_elements(by=By.XPATH,
                                       value="//a[@type='button']")]
                     )

    # companies = pd.Series(
    #     [i.text
    #      for i in driver.find_elements(by=By.XPATH,
    #                                    value="//div[@class='font-body-3 company col ng-star-inserted']")]
    #                     )

    # locations = pd.Series(
    #     [i.text
    #      for i in driver.find_elements(by=By.XPATH,
    #                                    value="//span[@class='dot-divider']")]
    #                     )

    urls = pd.Series(
        [i.get_attribute('href')
         for i in driver.find_elements(by=By.XPATH,
                                       value="//a[@type='button']")]
                    )

    # tags = pd.Series(
    #     [i.text
    #      for i in driver.find_elements(by=By.XPATH,
    #                                    value="//div[@class='pills-section ng-star-inserted']")]
    #                  )

    # times_posted = pd.Series(
    #     [i.text
    #      for i in driver.find_elements(by=By.XPATH,
    #                                    value="//efc-job-meta[@id='metaInfo']")]
    #                         )

    # print(roles)
    # print(companies)
    # print(locations)
    # print(urls)
    # print(tags)
    # print(times_posted)

    # print(len(roles))
    # print(len(companies))
    # print(len(locations))
    # print(len(urls))
    # print(len(tags))
    # print(len(times_posted))

    # roles = []
    # companies = []
    # locations_contracts = []
    # tags = []
    # times_posted = []
    #
    # for i in driver.find_elements(by=By.XPATH, value="//div[@class='d-flex g-0 w-100']"):
    #     job_data = i.text.splitlines()
    #     role = job_data[0]
    #     company = job_data[1]
    #     location_contract = job_data[2]
    #     tag = job_data[3]
    #     time_posted = job_data[4]
    #
    #     roles.append(role)
    #     companies.append(company)
    #     locations_contracts.append(location_contract)
    #     tags.append(tag)
    #     times_posted.append(time_posted)
    #
    #     print(job_data)
    #     print(role)
    #     print(company)
    #     print(location_contract)
    #     print(tags)
    #     print(time_posted)

    jobsdf = pd.DataFrame(
        {'Role': roles,
        'URL': urls}
                          )

    if save_to_excel is True:
        jobsdf['Date Viewed'] = datetime.now()
        fname = criterion + '.xlsx'
        jobsdf.to_excel('Dataframes/eFinancial Careers/' + fname)

        print("All jobs on the given webpage saved as a new Excel file", criterion + '.xlsx')

    # print(jobsdf)
    return jobsdf


def new_jobs_efc(criterion, url, save_to_excel=False):
    '''
    Add function description here
    '''
    url = str(url)
    criterion = str(criterion)

    latest_jobs_df = create_jobsdf_efc(criterion, url)
    latest_jobs_df.fillna('', inplace=True)
    # latest_jobs_df.pop('Company')

    # print('latest jobs df')
    # print(latest_jobs_df)

    prev_jobs_df = pd.read_excel('Dataframes/eFinancial Careers/' + criterion + '.xlsx', index_col = [0], dtype = object)
    prev_jobs_df = prev_jobs_df.drop(['Date Viewed'], axis = 1)
    prev_jobs_df.fillna('', inplace=True)

    # print('previous jobs df')
    # print(prev_jobs_df)

    df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', on = 'URL', indicator = True)
    # print(df_combined)

    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop=True)
    df_diff = df_diff.drop('_merge', axis = 1)
    # print(df_diff)

    df_diff = df_column_switch(df_diff, 'Role_x', 'Role_y')
    df_diff = df_diff.drop('Role_x', axis = 1)
    df_diff = df_diff.rename({'Role_y': 'Role'}, axis = 1)

    df_diff['Date Viewed'] = datetime.now()

    print("New jobs added/ existing jobs changed on " + '\033[1m' + criterion + '\033[0m' + " search query compared with the jobs in the last saved Excel file")
    print(df_diff)

    if save_to_excel is True:
        prev_jobs_df2 = pd.read_excel('Dataframes/eFinancial Careers/' + criterion + '.xlsx', index_col=[0])
        updated_jobs_df = pd.concat([df_diff, prev_jobs_df2]).reset_index(drop=True)
        updated_jobs_df.to_excel('Dataframes/eFinancial Careers/' + criterion + '.xlsx')

        print("New jobs on the given webpage added to the existing Excel file", criterion + '.xlsx')

    return df_diff