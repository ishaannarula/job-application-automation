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
    Returns a dataframe of the first 50 positions listed on a company's Workday website
    at the time the function is run.
    '''

    url = str(url)
    company_name = str(company_name)

    req = Request(url)
    req.add_header("Accept", "application/json,application/xml")
    raw = urlopen(req).read().decode()
    page_dict = json.loads(raw) #Sometimes Workday needs to be scrolled all the way to the end to load more jobs. This dict does not include jobs all the way to the end. It is unable to extract postings which appear after scrolling all the way down.

    #pprint.pprint(page_dict)

    jobs_lst = []
    partial_urls = []
    for key, value in get_all(page_dict):
        if key == 'text':
            jobs_lst.append(value)

        elif key == 'commandLink':
            partial_urls.append(value)

    #print(jobs_lst)
    #print(partial_urls)
    #print(len(partial_urls))

    if company_name == 'Vontobel Asset Management': # for Vontobel careers site - find a more general solution later
        n = 5
        jobs_lst = [jobs_lst[i * n:(i + 1) * n] for i in range((len(jobs_lst) + n - 1) // n)]  # Understand
        jobs_df = pd.DataFrame(jobs_lst, columns=['Position', 'Division', 'Job ID', 'Location', 'Date Posted'])

    else:
        n = 4
        jobs_lst = [jobs_lst[i * n:(i + 1) * n] for i in range((len(jobs_lst) + n - 1) // n)]  # Understand
        jobs_df = pd.DataFrame(jobs_lst, columns=['Position', 'Job ID', 'Location', 'Date Posted'])

    jobs_df.insert(0, 'Company', company_name)
    #jobs_df.drop(jobs_df.tail(1).index, inplace=True)
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
    jobs_df.to_excel(fname)

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
    latestdf_DatePosted = latest_jobs_df.pop('Date Posted')    #.drop('Date Posted', axis = 1)
    #print(latest_jobs_df)

    prev_jobs_df = pd.read_excel(company_name + '.xlsx', index_col = [0])
    prevdf_DatePosted = prev_jobs_df.pop('Date Posted')       #.drop(['Date Posted', 'Date Viewed'], axis = 1)
    prevdf_DateViewed = prev_jobs_df.pop('Date Viewed')
    prev_jobs_df.fillna('', inplace = True)

    #print(prev_jobs_df)

    #df_diff = pd.concat([prev_jobs_df,latest_jobs_df]).drop_duplicates(keep = False) #Understand
    df_combined = pd.merge(prev_jobs_df, latest_jobs_df, how = 'outer', indicator = True)
    df_diff = df_combined.loc[df_combined._merge == 'right_only'].reset_index(drop = True)
    dfdiff_merge = df_diff.pop('_merge')     #.drop('_merge', axis = 1)

    latest_jobs_df.insert(latest_jobs_df.columns.get_loc('URL'), 'Date Posted', latestdf_DatePosted)
    dfdiff_DatePosted = pd.merge(df_diff.copy(), latest_jobs_df, how = 'inner', on = 'Job ID')['Date Posted']
    df_diff.insert(df_diff.columns.get_loc('URL'), 'Date Posted', dfdiff_DatePosted)
    df_diff['Date Viewed'] = datetime.now()

    print("These are the new jobs added/ existing jobs changed on the company's website compared with the jobs in the last saved Excel file")
    print(df_diff)

    #cache = (prev_jobs_df, prevdf_DatePosted, prevdf_DateViewed)
    return df_diff

def save_newjobs(new_jobs, file_name):
    '''
    Saves new jobs viewed on a given company's webpage to the company's pre-existing Excel file
    '''

    prev_jobs_df = pd.read_excel(file_name, index_col = [0])
    updated_jobs_df = pd.concat([new_jobs, prev_jobs_df])
    updated_jobs_df.to_excel(file_name)

    print("New jobs on the given webpage added to the existing Excel file", file_name)


    #prev_jobs_df.insert(prev_jobs_df.columns.get_loc('URL'), 'Date Posted', prevdf_DatePosted)
    #prev_jobs_df = prev_jobs_df.join(prevdf_DateViewed)
    #updated_jobs_df = pd.concat([df_diff, prev_jobs_df])
    #print(updated_jobs_df)



#first_jobsdf_toexcel('AllianceBernstein', 'https://abglobal.wd1.myworkdayjobs.com/alliancebernsteincareers')
#added = new_jobs('AllianceBernstein', 'https://abglobal.wd1.myworkdayjobs.com/alliancebernsteincareers')
#save_newjobs(added, 'Fidelity International.xlsx')







#targetlinks_df = pd.read_excel('careerswebsitelinks.xlsx')
#for idx, row in targetlinks_df.iterrows():
#    init_jobsdb_xlsx(row[0], row[1])


#jobsMaster_df = pd.concat(jobs_dfs, ignore_index = True)

#with pd.option_context('display.max_rows', 100000, 'display.max_columns', 100):
#print(jobsMaster_df)

#print(jobs_lst)
#print(jobs_df)

#new_lst2 = ['Quantitative PM', 'REQ0001', 'Paris', 'Posted Today', 'IT Project Manager', 'REQ2806', '2 Locations', 'Posted Yesterday', 'Procurement Manager - Technology', 'REQ2804', 'New York', 'Posted Yesterday', 'Quantitative Developer - Macro', 'REQ2803', 'New York', 'Posted Yesterday', 'Intern, BAM Elevate Growth Tech Private Equity (undergrad)', 'REQ2800', '3 Locations', 'Posted 2 Days Ago', 'Intern, BAM Elevate Growth Tech Private Equity (MBA)', 'REQ2787', '3 Locations', 'Posted 2 Days Ago', 'Software Engineer - Elevate Technology', 'REQ2792', '2 Locations', 'Posted 3 Days Ago', 'Senior Full Stack Developer – React/NodeJS', 'REQ2796', 'New York', 'Posted 3 Days Ago', 'Intern, Software Engineer (QA)', 'REQ2773', '2 Locations', 'Posted 7 Days Ago', 'Credit Repo Trader', 'REQ2785', 'London', 'Posted 8 Days Ago', 'Quantitative Researcher - Equity Risk Research', 'REQ2784', '2 Locations', 'Posted 8 Days Ago', 'Associate, Fund Accountant', 'REQ2763', 'New York', 'Posted 8 Days Ago', 'Senior Associate, Fund Accounting', 'REQ2762', 'New York', 'Posted 8 Days Ago', 'Compliance Officer, Non-Equity Trade Surveillance', 'REQ2715', 'New York', 'Posted 8 Days Ago', 'Compliance Officer', 'REQ2242', 'New York', 'Posted 8 Days Ago', 'Compliance Officer', 'REQ2716', 'New York', 'Posted 8 Days Ago', 'Workday Security Administrator', 'REQ2774', '8 Locations', 'Posted 8 Days Ago', 'Intern, MBA Fundamental L/S Equity Analyst', 'REQ2770', '2 Locations', 'Posted 8 Days Ago', 'Intern, SPACs L/S Equity Analyst (MBA)', 'REQ2710', 'New York', 'Posted 8 Days Ago', 'Network Automation Engineer', 'REQ2777', 'Chicago', 'Posted 9 Days Ago', 'Intern, MBA REITS Equity Analyst', 'REQ2772', 'New York', 'Posted 9 Days Ago', 'Intern, Software Engineer - Data Platform', 'REQ2504', 'New York', 'Posted 10 Days Ago', 'Data Specialist (APAC) – Data Sourcing & Strategy', 'REQ2754', '2 Locations', 'Posted 20 Days Ago', 'Recruiting Coordinator', 'REQ2740', '3 Locations', 'Posted 22 Days Ago', 'Onboarding Coordinator', 'REQ2739', '3 Locations', 'Posted 22 Days Ago', 'Macro QA Automation Test Engineer', 'REQ2729', 'London', 'Posted 23 Days Ago', 'Data Integrity Specialist', 'REQ2714', '2 Locations', 'Posted 23 Days Ago', 'Fund Research Coordinator', 'REQ2680', '3 Locations', 'Posted 23 Days Ago', 'Commodities Data Engineer', 'REQ2727', '2 Locations', 'Posted 24 Days Ago', 'Senior Recruiter', 'REQ2718', '4 Locations', 'Posted 24 Days Ago', 'Intern, PM Development Quantitative Researcher', 'REQ2500', 'Singapore', 'Posted 24 Days Ago', 'Senior Software Engineer - Data Platform', 'REQ2546', 'Hong Kong', 'Posted 28 Days Ago', 'Intern, Python Developer – Data Analytics', 'REQ2632', '2 Locations', 'Posted 29 Days Ago', 'Associate, Futures Commission Procedures', 'REQ2657', 'New York', 'Posted 30 Days Ago', 'Senior Quant Researcher, PM Engagement', 'REQ2617', '3 Locations', 'Posted 30 Days Ago', 'Intern, Quantitative Researcher - Data Scientist', 'REQ2691', 'Chicago', 'Posted 30+ Days Ago', 'Intern, Quantitative Risk Analyst (Summer 2022)', 'REQ2482', 'London', 'Posted 30+ Days Ago', 'Python Developer - Quantitative PM Team', 'REQ2693', '2 Locations', 'Posted 30+ Days Ago', 'Intern, Compliance Software Engineer', 'REQ2692', 'New York', 'Posted 30+ Days Ago', 'Intern, Equity Risk Portfolio Construction', 'REQ2513', '2 Locations', 'Posted 30+ Days Ago', 'Macro Quant Developer', 'REQ2678', '3 Locations', 'Posted 30+ Days Ago', 'Macro Data Engineer', 'REQ2665', '3 Locations', 'Posted 30+ Days Ago', 'Python Developer – Systematic Infrastructure', 'REQ2566', '6 Locations', 'Posted 30+ Days Ago', 'Senior Real-Time Data Developer', 'REQ2642', '2 Locations', 'Posted 30+ Days Ago', 'Junior Equity Trader', 'REQ2641', 'New York', 'Posted 30+ Days Ago', 'Intern, Systems Engineering', 'REQ2639', '2 Locations', 'Posted 30+ Days Ago', 'Market Data Developer - Tick Data', 'REQ2637', '2 Locations', 'Posted 30+ Days Ago', 'Intern, Investment Data Analyst', 'REQ2521', 'London', 'Posted 30+ Days Ago', 'Operations Associate – Commodities', 'REQ2594', 'New York', 'Posted 30+ Days Ago', 'Operations Associate – US and Listed & Quant', 'REQ2581', '2 Locations', 'Posted 30+ Days Ago', 'Scrum Master', 'REQ2603', '3 Locations', 'Posted 30+ Days Ago', 'Follow Us', 'LinkedIn', '']

#print(set(new_lst2) - set(new_lst))

'''
Approach:
- Extract the json of each page and save it
- When looking for changes, extract a new json. Compare it with the saved json and print additions(/changes?)

14 Jan 2021 Update:
- Save an Excel file with name of company and workday website link
- Extract this data and save it in a dictionary
- In jobs_df, add the name of the company to which the listed jobs correspond

To-dos:
- Add a column with job links
- Create code for difference between dfs to see new job postings

15 Jan 2021:
- Separate functions to create a df from a url, save the df into Excel (with Date of Saving) and to compare the df extracted at a point in time with the saved Excel df to look for job additions   
'''


'''
response.raise_for_status()  # raises exception when not a 2xx response

if response.status_code != 204:
    print(response.json())









# Step2: Parse the HTML content
#soup = BeautifulSoup(r.content, 'html5lib')

#print(soup) # just printing the HTML code

#print(soup.get_text()) # just printing the text
'''