from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from webdriver_manager.chrome import ChromeDriverManager
import json, requests
from urllib.request import Request, urlopen
import pprint
import pandas as pd
import numpy as np
from datetime import datetime
import time
#import progressbar
import os
from helper_functions import *
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', None) #To display full URL in dataframe

def create_jobsdf_workday_selenium_bs(company_name, url, save_to_excel = False, recently_posted = False):
    os.environ['WDM_LOG_LEVEL'] = '0'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    caps = webdriver.DesiredCapabilities().CHROME.copy()
    caps["pageLoadStrategy"] = "normal"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities = caps, options = option)
    driver.get(url)

    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ul[@role = 'list']")))

    #print(driver.page_source)

    roles = []
    role_urls = []
    recent_roles = []
    recent_role_urls = []

    while True:
        sections = BeautifulSoup(driver.page_source, 'html.parser').find_all('li', {'class': 'css-1q2dra3'})
        #print(sections)

        for section in sections:
            #print(section)

            try: role = section.find('a', {'data-automation-id': 'jobTitle'}).getText()
            except: role = 'Role Name Unspecified'

            try:
                if company_name == 'Fidelity International':
                    location = section.find('ul', {'class': 'css-14a0imc'}).find('li', {'class': 'css-h2nt8k'}).getText()
                else:
                    location = section.find('div', {'class': 'css-248241'}).find('dd', {'class': 'css-129m7dg'}).getText()

            except: location = 'Location Unspecified'

            try:
                partial_url = section.find('a', {'data-automation-id': 'jobTitle'}).get('href')
                common_size = SequenceMatcher(None, partial_url, url).get_matching_blocks()[0].size  # U #.find_longest_match(0, len(partial_url), 0, len(url))
                role_url = url + partial_url[common_size : ] #U

            except: role_url = 'URL Unspecified'

            try:
                if company_name == 'Fidelity International':
                    dateposted = section.find_all('li', {'class': 'css-h2nt8k'})[2].getText()
                else:
                    dateposted = section.find('div', {'class': 'css-zoser8'}).find('dd', {'class': 'css-129m7dg'}).getText()

            except: dateposted = 'Date Posted Unspecified'

            # print(role)
            # print(location)
            # print(role_url)
            # print(dateposted)

            fullrole = role + ' - ' + location + ' - ' + dateposted
            roles.append(fullrole)
            role_urls.append(role_url)

            if recently_posted:
                days_num = list(range(1, 11))
                days_wrd = ['Today', 'Yesterday']

                if any(i in dateposted for i in days_wrd):
                    recent_roles.append(fullrole)
                    recent_role_urls.append(role_url)

                for i in dateposted.split():
                    if i.isdigit():
                        if int(i) in days_num:
                            recent_roles.append(fullrole)
                            recent_role_urls.append(role_url)

        try:
            driver.find_element(by=By.XPATH, value="//button[@aria-label = 'next']").click()
            if company_name == 'Merrill Lynch (Lateral US)': time.sleep(3)
            elif company_name == 'M&G Investments': time.sleep(2)
            else: time.sleep(1.5)

        except: break

    jobs_df = pd.DataFrame(pd.Series(roles), columns=['Role'])
    jobs_df['URL'] = pd.Series(role_urls)
    jobs_df.insert(0, 'Company', company_name)

    recent_jobs_df = pd.DataFrame(pd.Series(recent_roles), columns = ['Role'])
    recent_jobs_df['URL'] = pd.Series(recent_role_urls)
    recent_jobs_df.insert(0, 'Company', company_name)

    if save_to_excel:
        jobs_df['Date Viewed'] = datetime.now()
        fname = company_name + '.xlsx'
        jobs_df.to_excel('Dataframes/' + fname)

        print("All jobs on the given webpage saved as a new Excel file", company_name + '.xlsx')

    #print(jobs_df)

    if recently_posted: return recent_jobs_df
    else: return jobs_df

def create_jobsdf_workday_selenium(company_name, url, save_to_excel = False):
    '''
    Add description
    '''
    os.environ['WDM_LOG_LEVEL'] = '0'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

    caps = webdriver.DesiredCapabilities().CHROME.copy()
    caps["pageLoadStrategy"] = "normal"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), desired_capabilities = caps, options = option)
    driver.get(url)

    role = []
    jobsUrls_lst = []
    location = []
    #jobid = []
    dateposted = []
    page_count = 0

    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ul[@role = 'list']")))

    #bar = progressbar.ProgressBar(max_value = progressbar.UnknownLength)
    #bar_count = 0

    while True:
        page_count += 1
        #bar_count += 1
        #bar.update(bar_count)

        role += [i.text for i in driver.find_elements(by=By.XPATH, value="//a[@data-automation-id = 'jobTitle']")]
        jobsUrls_lst += [i.get_attribute('href') for i in driver.find_elements(by=By.XPATH, value="//a[@data-automation-id = 'jobTitle']")]

        loc = []
        for i in driver.find_elements(by = By.XPATH, value = "//div[@class = 'css-248241']"):
            if i.text == '': loc.append('Location Unspecified')
            else: loc.append(i.text.splitlines()[1])
        location += loc

        #location += [i.text for i in driver.find_elements(by=By.XPATH, value="//div[@data-automation-id = 'locations']//dd")]

        if ((company_name != 'Barings') and
            (company_name != 'Blackstone') and
            (company_name != 'Blackstone Campus')):
            dateposted += [i.text for i in driver.find_elements(by=By.XPATH, value="//div[@data-automation-id = 'postedOn']//dl//dd")]

        # ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        # WebDriverWait(driver, 20, ignored_exceptions = ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label = 'next']")))

        #print('THIS IS PAGE', page_count)

        #print(role)
        #print(jobsUrls_lst)
        #print(location)
        #print(jobid)
        #print(dateposted)

        #print(len(role))
        #print(len(jobsUrls_lst))
        #print(len(location))
        #print(len(jobid))
        #print(len(dateposted))

        try:
            driver.find_element(by = By.XPATH, value = "//button[@aria-label = 'next']").click()

            if company_name == 'Merrill Lynch (Lateral US)': time.sleep(3)
            else: time.sleep(1.5)
            #WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//ul[@role = 'list']")))

        except: break

    #print(role)
    #print(jobsUrls_lst)
    #print(location)
    #print(jobid)
    #print(dateposted)

    #print(len(role))
    #print(len(jobsUrls_lst))
    #print(len(location))
    #print(len(jobid))
    #print(len(dateposted))

    jobsRoles_lst = []

    for i in range(len(role)):
        if ((company_name != 'Barings') and
            (company_name != 'Blackstone') and
            (company_name != 'Blackstone Campus')):
            jobsRoles = role[i] + ' - ' + location[i] + ' - ' + dateposted[i]

        else: jobsRoles = role[i] + ' - ' + location[i]

        jobsRoles_lst.append(jobsRoles)

    #print(jobsRoles_lst)

    jobs_df = pd.DataFrame(pd.Series(jobsRoles_lst), columns = ['Role'])
    jobs_df['URL'] = pd.Series(jobsUrls_lst)
    jobs_df.insert(0, 'Company', company_name)

    if save_to_excel == True:
        jobs_df['Date Viewed'] = datetime.now()
        fname = company_name + '.xlsx'
        jobs_df.to_excel('Dataframes/' + fname)

        print("All jobs on the given webpage saved as a new Excel file", company_name + '.xlsx')

    #print(jobs_df)
    return jobs_df

def create_jobsdf_workday(company_name, url, save_to_excel = False): #Used to work with the old version of workday. Now outdated
    '''
    Returns a dataframe of the first 50 (or fewer) positions listed on a company's Workday website
    at the time the function is run.
    '''
    url = str(url)
    company_name = str(company_name)

    req = Request(url)
    req.add_header("Accept", "application/json,application/xml")
    req.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
    raw = urlopen(req).read().decode()
    print('Raw', raw)
    page_dict = json.loads(raw) #Sometimes Workday needs to be scrolled all the way to the end to load more jobs. This dict does not include jobs all the way to the end. It is unable to extract postings which appear after scrolling all the way down for the first time.

    #pprint.pprint(page_dict) #The above code does not work for Arrowstreet Capital

    jobs_lst = []
    partial_urls = []
    for key, value in get_all(page_dict):
        if key == 'text':
            jobs_lst.append(value)

        elif key == 'commandLink':
            partial_urls.append(value)

    if company_name == 'Vontobel Asset Management': n = 5 #for Vontobel careers site - find a more general solution later
    elif company_name == 'Barings': n = 3
    else: n = 4

    jobs_lst = [jobs_lst[i * n:(i + 1) * n] for i in range((len(jobs_lst) + n - 1) // n)]  #U

    jobs_lst2 = []
    date_posted = []
    for lst in jobs_lst:
        lst2 = [x for x in lst if not x.startswith('Posted')]
        lst_dp = list(set(lst) - set(lst2))
        jobs_lst2.append(lst2)
        date_posted.append(lst_dp)

    if (company_name == 'Blackstone' or
        company_name == 'Blackstone Campus' or
        company_name == 'T. Rowe Price International'):
        jobs_df = pd.DataFrame()

    else:
        jobs_df = pd.DataFrame(pd.Series(jobs_lst2), columns = ['Role'])

    #print(jobs_lst)
    #print(date_posted)
    #print(len(date_posted), len(jobs_df.index))
    #print(partial_urls)
    #print(len(partial_urls))

    jobs_df['URL'] = pd.DataFrame(partial_urls)

    if company_name == 'PGIM': s = 'myworkdaysite.com'
    else: s = 'myworkdayjobs.com'

    idx_crit = url.find(s) + len(s)
    jobs_df['URL'] = url[ : idx_crit] + jobs_df['URL']

    jobs_df.insert(jobs_df.columns.get_loc('URL'), 'Date Posted', pd.Series(date_posted))

    jobs_df.insert(0, 'Company', company_name)

    #if len(date_posted) != len(jobs_df.index):
    #    diff = len(date_posted) - len(jobs_df.index)
    #    date_posted = date_posted[:-diff]

    #jobs_df['Date Posted'] = date_posted

    if save_to_excel == True:
        jobs_df['Date Viewed'] = datetime.now()
        fname = company_name + '.xlsx'
        jobs_df.to_excel('Dataframes/' + fname)

        print("First 50 jobs on the given webpage saved as a new Excel file", fname)

    #print(jobs_df)
    return jobs_df

def first_jobsdf_toexcel(company_name, url): #Not used anymore
    '''
    Saves the jobs dataframe created for the first time using the create_jobsdf_... functions as an Excel file
    named after the company, adding a 'Date Viewed' column which specifies the date and
    time the jobs were viewed and dataframe was saved
    '''
    url = str(url)
    company_name = str(company_name)

    jobs_df = create_jobsdf(company_name, url)
    jobs_df['Date Viewed'] = datetime.now()

    fname = company_name + '.xlsx'
    jobs_df.to_excel('Dataframes/'+ fname)

    print("First 50 jobs on the given webpage saved as a new Excel file", fname)

def new_jobs_workday(company_name, url, save_to_excel = False):
    '''
    Returns a dataframe with new jobs added/ existing jobs changed on the company's Workday website compared
    with the jobs in the last saved Excel file

    Drawbacks to Fix:
    - Some jobs posted earlier are often re-posted. This would not capture jobs when they are re-posted (only
    when they were posted for the first time)
    '''
    url = str(url)
    company_name = str(company_name)

    latest_jobs_df = create_jobsdf_workday_selenium_bs(company_name, url)
    latest_jobs_df.fillna('', inplace = True)
    latest_jobs_df.pop('Company')
    #print('latest jobs df')
    #print(latest_jobs_df)

    prev_jobs_df = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col = [0], dtype = object)
    prev_jobs_df = prev_jobs_df.drop(['Company', 'Date Viewed'], axis = 1)
    prev_jobs_df.fillna('', inplace = True)
    #print('previous jobs df')
    #print(prev_jobs_df)

    #df_diff = pd.concat([prev_jobs_df,latest_jobs_df]).drop_duplicates(keep = False) #Understand
    df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', on = 'URL', indicator = True)
    #print(df_combined)
    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop = True)
    df_diff = df_diff.drop('_merge', axis = 1)
    #print(df_diff)

    #latest_jobs_df.insert(latest_jobs_df.columns.get_loc('URL'), 'Date Posted', latestdf_DatePosted)
    #dfdiff_DatePosted = pd.merge(df_diff.copy(), latest_jobs_df, how = 'inner', on = 'URL')['Date Posted']
    #df_diff.insert(df_diff.columns.get_loc('URL'), 'Date Posted', dfdiff_DatePosted)

    df_diff.insert(df_diff.columns.get_loc('Role_x'), 'Company', company_name)

    df_diff = df_column_switch(df_diff, 'Role_x', 'Role_y')
    df_diff = df_diff.drop('Role_x', axis = 1)
    df_diff = df_diff.rename({'Role_y': 'Role'}, axis = 1)

    df_diff['Date Viewed'] = datetime.now()

    print("New jobs added/ existing jobs changed on " + '\033[1m' + company_name + '\033[0m' + " website compared with the jobs in the last saved Excel file")
    print(df_diff)

    if save_to_excel == True:
        prev_jobs_df2 = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col=[0])
        updated_jobs_df = pd.concat([df_diff, prev_jobs_df2]).reset_index(drop = True)
        updated_jobs_df.to_excel('Dataframes/' + company_name + '.xlsx')

        print("New jobs on the given webpage added to the existing Excel file", company_name + '.xlsx')

    return df_diff

def dfs_old20220120_tonew(file_name):
    '''
    Converts dataframes saved in old format in folder Dataframes to new format
    '''
    old_df = pd.read_excel('Dataframes (Old Format 2022 01 20)/' + file_name, index_col=[0])
    #print('\033[1m' + 'Old Dataframe for ' + file_name + '\033[0m')
    #print(old_df)
    #old_df['Job ID'] = old_df['Job ID'].astype('Int64') #Only for Vontobel

    combined = old_df[['Position', 'Division', 'Job ID', 'Location']].values.tolist()
    old_df.insert(old_df.columns.get_loc('Date Posted'), 'Role', combined)

    new_df = old_df[['Company', 'Role', 'Date Posted', 'URL', 'Date Viewed']]
    #print('\033[1m' + 'New Dataframe for ' + file_name + '\033[0m')
    #print(new_df)

    new_df.to_excel('Dataframes/' + file_name)
    print('Converted old dataframe format for file ' + '\033[1m' + file_name + '\033[0m')
