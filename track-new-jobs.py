import json
from urllib.request import Request, urlopen
import pprint
import pandas as pd
desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_colwidth', None) #To display full URL in dataframe
from datetime import datetime

def get_all(myjson): #Understand
    """ Recursively find the keys and associated values in all the dictionaries
        in the json object or list.
    """
    if isinstance(myjson, dict):
        for jsonkey, jsonvalue in myjson.items():
            if not isinstance(jsonvalue, (dict, list)):
                yield jsonkey, jsonvalue
            else:
                for k, v in get_all(jsonvalue):
                    yield k, v
    elif isinstance(myjson, list):
        for element in myjson:
            if isinstance(element, (dict, list)):
                for k, v in get_all(element):
                    yield k, v

def create_jobsdf(company_name, url):
    '''
    Returns a dataframe of the first 50 (or fewer) positions listed on a company's Workday website
    at the time the function is run.
    '''

    url = str(url)
    company_name = str(company_name)

    req = Request(url)
    req.add_header("Accept", "application/json,application/xml")
    raw = urlopen(req).read().decode()
    page_dict = json.loads(raw) #Sometimes Workday needs to be scrolled all the way to the end to load more jobs. This dict does not include jobs all the way to the end. It is unable to extract postings which appear after scrolling all the way down.

    #pprint.pprint(page_dict) #The above code does not work for Arrowstreet Capital

    jobs_lst = []
    partial_urls = []
    for key, value in get_all(page_dict):
        if key == 'text':
            jobs_lst.append(value)

        elif key == 'commandLink':
            partial_urls.append(value)

    if company_name == 'Vontobel Asset Management': # for Vontobel careers site - find a more general solution later
        n = 5
        jobs_lst = [jobs_lst[i * n:(i + 1) * n] for i in range((len(jobs_lst) + n - 1) // n)]  # Understand
        jobs_df = pd.DataFrame(jobs_lst, columns=['Position', 'Division', 'Job ID', 'Location', 'Date Posted'])

    else:
        n = 4
        jobs_lst = [jobs_lst[i * n:(i + 1) * n] for i in range((len(jobs_lst) + n - 1) // n)]  # Understand
        jobs_df = pd.DataFrame(jobs_lst, columns=['Position', 'Job ID', 'Location', 'Date Posted'])

    #print(jobs_lst)
    #print(partial_urls)
    #print(len(partial_urls))

    jobs_df.insert(0, 'Company', company_name)
    jobs_df['URL'] = pd.DataFrame(partial_urls)
    s = 'myworkdayjobs.com'
    idx_crit = url.find(s) + len(s)
    jobs_df['URL'] = url[ : idx_crit] + jobs_df['URL']

    return jobs_df


def first_jobsdf_toexcel(company_name, url):
    '''
    Saves the jobs dataframe created for the first time using the create_jobsdf function as an Excel file
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

def new_jobs(company_name, url):
    '''
    Returns a dataframe with new jobs added/ existing jobs changed on the company's Workday website compared
    with the jobs in the last saved Excel file
    '''

    url = str(url)
    company_name = str(company_name)

    latest_jobs_df = create_jobsdf(company_name, url)
    latest_jobs_df.fillna('', inplace = True)
    latestdf_DatePosted = latest_jobs_df.pop('Date Posted')
    #print(latest_jobs_df)

    prev_jobs_df = pd.read_excel('Dataframes/' + company_name + '.xlsx', index_col = [0], dtype = object)
    prev_jobs_df = prev_jobs_df.drop(['Date Posted', 'Date Viewed'], axis = 1)
    prev_jobs_df.fillna('', inplace = True)
    #print(prev_jobs_df)

    #df_diff = pd.concat([prev_jobs_df,latest_jobs_df]).drop_duplicates(keep = False) #Understand
    df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', indicator = True)
    #print(df_combined)
    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop = True)
    df_diff = df_diff.drop('_merge', axis = 1)

    latest_jobs_df.insert(latest_jobs_df.columns.get_loc('URL'), 'Date Posted', latestdf_DatePosted)
    dfdiff_DatePosted = pd.merge(df_diff.copy(), latest_jobs_df, how = 'inner', on = 'Job ID')['Date Posted']
    df_diff.insert(df_diff.columns.get_loc('URL'), 'Date Posted', dfdiff_DatePosted)
    df_diff['Date Viewed'] = datetime.now()

    print("New jobs added/ existing jobs changed on " + '\033[1m' + company_name + '\033[0m' + " website compared with the jobs in the last saved Excel file")
    print(df_diff)

    return df_diff

def save_newjobs(new_jobs, file_name):
    '''
    Saves new jobs viewed on a given company's webpage to the company's pre-existing Excel file
    '''

    prev_jobs_df = pd.read_excel('Dataframes/' + file_name, index_col = [0])
    updated_jobs_df = pd.concat([new_jobs, prev_jobs_df])
    updated_jobs_df.to_excel('Dataframes/' + file_name)

    print("New jobs on the given webpage added to the existing Excel file", file_name)

#targetlinks_df = pd.read_excel('careerswebsitelinks2.xlsx')
#for idx, row in targetlinks_df.iterrows():
#    new_jobs(row[0], row[1])

#mill = new_jobs('Millennium Management', 'https://mlp.wd5.myworkdayjobs.com/en-US/mlpcareers')
#save_newjobs(mill, 'Millennium Management.xlsx')