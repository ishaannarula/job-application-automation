import requests
from bs4 import BeautifulSoup
import pandas as pd
from difflib import SequenceMatcher
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', None) #To display full URL in dataframe
from datetime import datetime

def df_column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df

def create_jobsdf_greenhouse(company_name, url, save_to_excel = False):
    '''
    Add function description here
    '''
    url = str(url)
    company_name = str(company_name)

    page = requests.get(url)
    sections = BeautifulSoup(page.text, 'html.parser').find_all('section', {'class': 'level-0'})

    roles = []
    role_urls = []
    for section in sections:
        #print(section)

        for opening in section.find_all('div', {'class': 'opening'}):
            #print(opening)
            #print(' ')

            role_title = opening.find('a').getText().strip()
            role_location = opening.find('span', {'class': 'location'}).getText().strip()

            partial_url = [elem.get('href') for elem in opening.find_all('a')][0]

            if ((company_name == 'Optiver') or
                (company_name == 'Glovo') or
                (company_name == 'Graviton Research Capital')):
                job_no = partial_url.split('/')[-1].split('=')[-1]
                role_url = partial_url

            elif company_name == 'Squarepoint Capital':
                job_no = partial_url.split('/')[-1].split('=')[-1]
                role_url = partial_url.split('?')[0] + '/job#' + job_no

            else:
                job_no = partial_url.split('/')[-1]
                common_size = SequenceMatcher(None, partial_url, url).get_matching_blocks()[0].size   #U #.find_longest_match(0, len(partial_url), 0, len(url))
                role_url = url + partial_url[common_size : ] #U

            roles.append(role_title + ' - ' + role_location + ' - ' + job_no)
            role_urls.append(role_url)

    jobs_df = pd.DataFrame(pd.Series(roles), columns = ['Role'])
    jobs_df['URL'] = pd.DataFrame(pd.Series(role_urls))
    jobs_df.insert(jobs_df.columns.get_loc('Role'), 'Company', company_name)

    #print(roles)
    #print(role_urls)

    if save_to_excel == True:
        jobs_df['Date Viewed'] = datetime.now()
        fname = company_name + '.xlsx'
        jobs_df.to_excel('Dataframes/' + fname)

        print("All jobs on the given webpage saved as a new Excel file", company_name + '.xlsx')

    #print(jobs_df)
    return jobs_df

def new_jobs_greenhouse(company_name, url, save_to_excel = False):
    '''
    Add function description here
    '''
    url = str(url)
    company_name = str(company_name)

    latest_jobs_df = create_jobsdf_greenhouse(company_name, url)
    latest_jobs_df.fillna('', inplace = True)
    latest_jobs_df.pop('Company')
    #print('latest jobs df')
    #print(latest_jobs_df)

    prev_jobs_df = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col = [0], dtype = object)
    prev_jobs_df = prev_jobs_df.drop(['Company', 'Date Viewed'], axis = 1)
    prev_jobs_df.fillna('', inplace = True)
    #print('previous jobs df')
    #print(prev_jobs_df)

    df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', on = 'URL', indicator = True)
    #print(df_combined)
    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop = True)
    df_diff = df_diff.drop('_merge', axis = 1)
    #print(df_diff)

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