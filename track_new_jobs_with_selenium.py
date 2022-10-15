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

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', None) #To display full URL in dataframe

def create_jobsdf_withSelenium(company_name, url, save_to_excel = False):
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

    if company_name == 'Hudson River Trading':
        jobsRoles = driver.find_elements(by = By.XPATH, value = "//table[@class = 'jobs-container']")
        jobsUrls_lst = []

        for i in jobsRoles:
            text = str(i.text)

            jobsUrls = i.find_elements(by = By.CLASS_NAME, value = 'job-url')
            for j in jobsUrls:
                link = j.get_attribute('href')
                jobsUrls_lst.append(link)

        jobsRoles_lst = text.split('\n')
        n = 3 #no. of columns in the table
        jobsRoles_lst2 = [jobsRoles_lst[i * n:(i + 1) * n] for i in range((len(jobsRoles_lst) + n - 1) // n)]

    elif ((company_name == 'Susquehanna International Group') or
          (company_name == 'IMC Trading')):
        jobsRoles_lst2 = []
        jobsUrls_lst = []

        #if company_name == 'IMC Trading': #simulate pressing Escape to skip page from loading entirely
            #time.sleep(float(3))
            #ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            #currentElem = driver.switch_to.active_element
            #currentElem.send_keys(Keys.ESCAPE)

            #element = driver.find_element(by=By.XPATH, value="//body")
            #element.send_keys(Keys.ESCAPE)

        while True:
            jobsRoles = driver.find_elements(by = By.XPATH, value="//div[@class = 'content-block']")

            for i in jobsRoles:
                elem = i.find_elements(by = By.XPATH, value = "//li[@class = 'jobs-list-item']//div[@class = 'information']//a")

                for j in elem:
                    role = j.text
                    link = j.get_attribute('href')
                    location = j.get_attribute('data-ph-at-job-location-text')    #.find_element(by = By.XPATH, value = "//a[@data-ph-at-job-location-area-text]")
                    datePosted = j.get_attribute('data-ph-at-job-post-date-text')
                    jobid = j.get_attribute('data-ph-at-job-id-text')

                    jobsRole = role + ' - ' + location + ' - ' + datePosted + ' - ' + jobid
                    #print(jobsRole)

                    jobsRoles_lst2.append(jobsRole)
                    jobsUrls_lst.append(link)

            try:
                if company_name == 'Susquehanna International Group': driver.find_element(by = By.XPATH, value = "//div[@class = 'pagination-block au-target']//ul[@class = 'pagination au-target']//a[@class = 'next-btn au-target']").click()

                #elif company_name == 'IMC Trading':
                    #time.sleep(2)
                    #ActionChains(driver).send_keys(Keys.ESCAPE).perform()

                    #driver.find_element(by = By.XPATH, value = "//div[@class = 'pagination-block au-target']//ul[@class = 'pagination au-target']//a[@aria-label = 'View next page']").click()

                    # simulate pressing Escape to skip page from loading entirely
                    #time.sleep(3)
                    #element2 = driver.find_element(by = By.XPATH, value = "//body")
                    #element2.send_keys(Keys.ESCAPE)

                    #ActionChains(driver).send_keys(Keys.ESCAPE).perform()

            except: break

    elif company_name == 'Point72':
        while True:
            try:
                WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH,
                                                                                       "//a[@class = 'btn-view "
                                                                                       "o-button o-button--primary "
                                                                                       "u-spacing--double--top "
                                                                                       "btn-load-more']")))
                driver.find_element(by=By.XPATH, value=
                "//a[@class = 'btn-view "
                "o-button o-button--primary "
                "u-spacing--double--top "
                "btn-load-more']").click()

            except: break

        role = [i.text for i in driver.find_elements(by=By.XPATH, value=str(
            "//"
            "div[@class = 'thumbnail']//"
            "div[@class = 'o-listing--table__left']//"
            "h4[@class = 'u-font u-font--l u-font-weight--bold u-line-height--140']//"
            "a[@class = 'searchSite']"))]

        focus = [i.text for i in driver.find_elements(by=By.XPATH, value=str(
            "//"
            "div[@class = 'thumbnail']//"
            "div[@class = 'o-listing--table__middle']//"
            "p[@class = 'u-line-height--140']"))]

        location = [i.text for i in driver.find_elements(by=By.XPATH, value=str(
            "//"
            "div[@class = 'thumbnail']//"
            "div[@class = 'o-listing--table__right']//"
            "p[@class = 'u-line-height--140']"))]

        jobsUrls_lst = [i.get_attribute('href') for i in driver.find_elements(by=By.XPATH, value=str(
            "//"
            "div[@class = 'thumbnail']//"
            "div[@class = 'o-listing--table__left']//"
            "h4[@class = 'u-font u-font--l u-font-weight--bold u-line-height--140']//"
            "a[@class = 'searchSite']"))]

        jobsRoles_lst2 = []
        for pair in zip(role, focus, location):
            jobsRoles = pair[0] + ' - ' + pair[1] + ' - ' + pair[2]
            jobsRoles_lst2.append(jobsRoles)

        #print(jobsRoles_lst2)

    elif company_name == 'Caxton Associates':
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH,
                                                           "//button[@data-ui = 'load-more-button']"))
                )
                button = driver.find_element(by=By.XPATH,
                                             value="//button[@data-ui = 'load-more-button']")
                driver.execute_script("arguments[0].click();", button)

            except: break

        role = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//ancestor::div[1]//h2")]
        # date_posted = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//small[@data-ui='job-posted']")]
        location = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//span[@data-ui='job-location']")]
        jobsUrls_lst = [i.get_attribute('href') for i in driver.find_elements(by = By.XPATH, value = "//li[@data-ui='job']//ancestor::div[1]//a")]


        # print(jobsUrls_lst)
        # print(role)
        # # print(date_posted)
        # print(location)

        id = []
        for i in jobsUrls_lst:
            id.append(i.split('/')[-2])

        #print(id)

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location[i] + ' - ' + id[i]
            jobsRoles_lst2.append(jobsRoles)

    elif company_name == 'Trexquant Investment':
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH,
                                                           "//a[@data-ui = 'clear-filters']"))
                )
                driver.find_element(by=By.XPATH, value="//a[@data-ui = 'clear-filters']").click()

                WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH,
                                                           "//button[@data-ui = 'load-more-button']"))
                )
                button = driver.find_element(by=By.XPATH,
                                             value="//button[@data-ui = 'load-more-button']")
                driver.execute_script("arguments[0].click();", button)

            except: break
        role = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job-opening']//ancestor::div[1]//h3")]
        # date_posted = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//small[@data-ui='job-posted']")]
        location = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job-opening']//span[@data-ui='job-location']")]
        jobsUrls_lst = [i.get_attribute('href') for i in driver.find_elements(by = By.XPATH, value = "//li[@data-ui='job-opening']//ancestor::div[1]//a")]

        # print(jobsUrls_lst)
        # print(role)
        # # print(date_posted)
        # print(location)

        id = []
        for i in jobsUrls_lst:
            id.append(i.split('/')[-2])

        #print(id)

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location[i] + ' - ' + id[i]
            jobsRoles_lst2.append(jobsRoles)

    elif company_name == 'Abu Dhabi Investment Authority (ADIA)':
        # while True:
        #     try:
        #         WebDriverWait(driver, 20).until(
        #             EC.visibility_of_all_elements_located((By.XPATH,
        #                                                    "//ul[@data-ui = 'list']"))
        #         )
        #         # button = driver.find_element(by=By.XPATH,
        #         #                              value="//button[@data-ui = 'load-more-button']")
        #         # driver.execute_script("arguments[0].click();", button)
        #
        #     except:
        #         break

        WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.XPATH,
                                                   "//ul[@data-ui = 'list']"))
        )

        role = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//ancestor::div[1]//h2")]
        # date_posted = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//small[@data-ui='job-posted']")]
        location = [i.text for i in
                    driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//span[@data-ui='job-location']")]
        jobsUrls_lst = [i.get_attribute('href') for i in
                        driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//ancestor::div[1]//a")]

        # print(jobsUrls_lst)
        # print(role)
        # print(date_posted)
        # print(location)

        id = []
        for i in jobsUrls_lst:
            id.append(i.split('/')[-2])

        # print(id)

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location[i] + ' - ' + id[i]
            jobsRoles_lst2.append(jobsRoles)


    elif company_name == 'Hike':
        while True:
            try:
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH,
                                                           "//button[@data-ui = 'load-more-button']"))
                )
                button = driver.find_element(by=By.XPATH,
                                             value="//button[@data-ui = 'load-more-button']")
                driver.execute_script("arguments[0].click();", button)

            except: break
        role = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job-opening']//ancestor::div[1]//h3")]
        # date_posted = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job']//small[@data-ui='job-posted']")]
        location = [i.text for i in driver.find_elements(by=By.XPATH, value="//li[@data-ui='job-opening']//span[@data-ui='job-location']")]
        jobsUrls_lst = [i.get_attribute('href') for i in driver.find_elements(by = By.XPATH, value = "//li[@data-ui='job-opening']//ancestor::div[1]//a")]

        # print(jobsUrls_lst)
        # print(role)
        # # print(date_posted)
        # print(location)

        id = []
        for i in jobsUrls_lst:
            id.append(i.split('/')[-2])

        #print(id)

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location[i] + ' - ' + id[i]
            jobsRoles_lst2.append(jobsRoles)

    elif company_name == 'D.E. Shaw Full-time Jobs':

        WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'accept-button']")))
        cookie_button = driver.find_element(by=By.XPATH, value="//div[@class = 'accept-button']")
        driver.execute_script("arguments[0].click();", cookie_button)

        #WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class = 'job-filter-results dark regular-jobs']")))
        time.sleep(5)

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class = 'more-plus']"))).click()           #element_to_be_clickable(((By.XPATH, "//span[@class = 'more-plus']"))).click()
        #driver.find_element(by=By.XPATH, value="//span[@class = 'more-plus']").click()

        sections = BeautifulSoup(driver.page_source, 'html.parser').find('section', {'class': 'section choose-your-path'}).find_all('div', {'class': 'job'})

        roles = []
        role_urls = []

        for section in sections:
            print(section)
            #role = section.find_all('div', {'class': 'description wrapper'}).find('span').getText()
            #role_url = section.find
            #print(role)

        #elems = driver.find_elements(by = By.XPATH, value = "//div[@class = 'job-filter-results dark regular-jobs']//div[@class = 'job-wrapper']//div[@class = 'job']")
        #print(elems)

    elif company_name == 'Balyasny Asset Management':
        time.sleep(10) # to be replaced by WebDriverWait
        role = [i.text for i in driver.find_elements(by=By.XPATH, value="//p[@class = 'jobRequisitionName']")]

        location_req_dateposted = [i.text for i in driver.find_elements(
            by=By.XPATH, value="//p[@class = 'jobRequisitionInformation']")]

        # print(len(role), len(location_req_dateposted))
        # print(role)
        # print(location_req_dateposted)

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location_req_dateposted[i]
            jobsRoles_lst2.append(jobsRoles)

        # print(jobsRoles_lst2)

        req = []
        for i in location_req_dateposted:
            req.append(i.split()[0])

        # print(req)

        role_dashed = []
        for i in role:
            i_dash = i.replace(' ', '-')
            i_dash = i_dash.replace('/', '-')
            i_dash = i_dash.replace('(', '-')
            i_dash = i_dash.replace(')', '-')
            i_dash = i_dash.replace(',', '-')
            role_dashed.append(i_dash)

        jobsUrls_lst = []
        # if len(req) == len(role_dashed):
        #     for (i, j) in zip(req, role_dashed):
        #         url_structure = url + 'details?jobReq=' + j + '_' + i
        #         jobsUrls_lst.append(url_structure)

        jobsUrls_lst = [url] * len(jobsRoles_lst2)
        # print(jobsUrls_lst)

    elif company_name == 'EDF Trading':
        role = [i.text
                for i in driver.find_elements(by=By.XPATH, value="//table[@id = 'cws-search-results']//tbody//b[1]//a")
                if i.text != 'Title' and
                i.text != 'Location' and
                i.text != '']
        # print(role)

        location = [i.text
                    for i in driver.find_elements(by=By.XPATH, value="//table[@id = 'cws-search-results']//tbody//td[2]//b")]
        # print(location)

        # print(len(role), len(location))

        jobsRoles_lst2 = []

        for i in range(len(role)):
            jobsRoles = role[i] + ' - ' + location[i]
            jobsRoles_lst2.append(jobsRoles)

        jobsUrls_lst = [i.get_attribute('href')
                for i in driver.find_elements(by=By.XPATH, value="//table[@id = 'cws-search-results']//tbody//b[1]//a")
                if i.text != 'Title' and
                i.text != 'Location' and
                i.text != '']

        # print(jobsRoles_lst2)

    elif company_name == 'Citadel Students Full-time':
        time.sleep(5)
        elem = driver.find_elements(by=By.XPATH, value="//div[@id='DataTables_Table_0_filter']//table//tbody")
        print(elem)

        role = [i.text
                for i in driver.find_elements(by=By.XPATH, value="//div[@id='DataTables_Table_0_filter']"
                                                                 "//table[@class='sortable-table dataTable no-footer']"
                                                                 "//tbody//tr//td[@class='sorting_1']//a")
                ]
        print(role)

    jobs_df = pd.DataFrame(pd.Series(jobsRoles_lst2), columns = ['Role'])
    jobs_df['URL'] = pd.Series(jobsUrls_lst)
    if company_name == 'Balyasny Asset Management':
        jobs_df['Requisition ID'] = pd.Series(req)
    jobs_df.insert(0, 'Company', company_name)

    if save_to_excel == True:
        jobs_df['Date Viewed'] = datetime.now()
        fname = company_name + '.xlsx'
        jobs_df.to_excel('Dataframes/' + fname)

        print("All jobs on the given webpage saved as a new Excel file", company_name + '.xlsx')

    # print(jobs_df)
    return jobs_df


def new_jobs_withSelenium(company_name, url, save_to_excel = False):
    '''
    Add function description here
    '''
    url = str(url)
    company_name = str(company_name)

    latest_jobs_df = create_jobsdf_withSelenium(company_name, url)
    latest_jobs_df.fillna('', inplace = True)
    latest_jobs_df.pop('Company')
    if company_name == 'Balyasny Asset Management':
        latest_jobs_df.pop('URL')

    # print('latest jobs df')
    # print(latest_jobs_df)

    prev_jobs_df = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col = [0], dtype = object)
    prev_jobs_df = prev_jobs_df.drop(['Company', 'Date Viewed'], axis = 1)
    if company_name == 'Balyasny Asset Management':
        prev_jobs_df = prev_jobs_df.drop(['URL'], axis=1)

    prev_jobs_df.fillna('', inplace = True)
    # print('previous jobs df')
    # print(prev_jobs_df)

    if company_name == 'Balyasny Asset Management':
        df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', on = 'Requisition ID', indicator = True)
    else:
        df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', on = 'URL', indicator = True)

    # print(df_combined)

    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop = True)
    df_diff = df_diff.drop('_merge', axis = 1)
    # print(df_diff)

    df_diff.insert(df_diff.columns.get_loc('Role_x'), 'Company', company_name)
    df_diff = df_column_switch(df_diff, 'Role_x', 'Role_y')
    df_diff = df_diff.drop('Role_x', axis = 1)
    df_diff = df_diff.rename({'Role_y': 'Role'}, axis = 1)

    if company_name == 'Balyasny Asset Management':
        df_diff.insert(df_diff.columns.get_loc('Requisition ID'), 'URL', url)

    df_diff['Date Viewed'] = datetime.now()

    print("New jobs added/ existing jobs changed on " + '\033[1m' + company_name + '\033[0m' + " website compared with the jobs in the last saved Excel file")
    print(df_diff)

    if save_to_excel == True:
        prev_jobs_df2 = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col=[0])
        updated_jobs_df = pd.concat([df_diff, prev_jobs_df2]).reset_index(drop = True)
        updated_jobs_df.to_excel('Dataframes/' + company_name + '.xlsx')

        print("New jobs on the given webpage added to the existing Excel file", company_name + '.xlsx')

    return df_diff