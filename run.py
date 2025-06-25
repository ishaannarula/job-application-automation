import webbrowser
import tempfile
import pandas as pd
from track_new_jobs_greenhouse import *
from track_new_jobs_workday import *
from track_new_jobs_with_selenium import *
from track_new_jobs_efc import *
import time
import warnings
warnings.filterwarnings('ignore')


save = True
speed = 'Okay'
see_recent = False
tab_name = 'Companies'  # Choose between 'Companies', 'eFinancial Careers'

targetlinks_df = pd.read_excel('careerswebsitelinks.xlsx', tab_name)

if not see_recent:
    if tab_name == 'Companies':
        for idx, row in targetlinks_df.iterrows():
            if row[5] == speed:
                try:
                    print('Company in progress:', row[0])
                    if row[2] == 'W':
                        if row[3] == 'G' and row[4] == 'Workday':
                            df = new_jobs_workday(row[0], row[1], save_to_excel=save)
                            # df = create_jobsdf_workday_selenium_bs(row[0], row[1], save_to_excel=False, recently_posted=False)

                            print(' ')
                            print(' ')

                        if row[3] == 'G' and row[4] == 'Greenhouse':
                            df = new_jobs_greenhouse(row[0], row[1], save_to_excel=save)
                            # df = create_jobsdf_greenhouse(row[0], row[1], save_to_excel=False)

                            print(' ')
                            print(' ')

                        if row[3] == 'G' and row[4] == 'Varied (Selenium)':
                            df = new_jobs_withSelenium(row[0], row[1], save_to_excel=save)
                            # df = create_jobsdf_withSelenium(row[0], row[1], save_to_excel=False)

                            print(' ')
                            print(' ')
                        
                        # if df is not None and not df.empty:
                        html_table = df.to_html(index=False)
                                            
                        # else:
                        #     print('Empty jobs dataframe')
                            
                        # Define a specific folder (e.g., Desktop)
                        save_folder = os.path.expanduser("/Users/ishaan/Library/CloudStorage/GoogleDrive-ishaan.narula1@gmail.com/My Drive/Personal Development/GitHub/job-application-automation/new_job_html_files")
                        os.makedirs(save_folder, exist_ok=True)
                        
                        html_path = os.path.join(save_folder, f"{row[0]}.html")
                        with open(html_path, "w", encoding="utf-8") as tmpfile:
                            tmpfile.write(html_table)
                        # webbrowser.open(f"file://{html_path}")

                    else: continue
    
                except:
                    print('Error loading new jobs for ' +
                          '\033[1m' + row[0] + '\033[0m' +
                          '. Continuing onto the next company...')
                    print(' ')
                    print(' ')
                    continue
            # break            

    elif tab_name == 'eFinancial Careers':
        for idx, row in targetlinks_df.iterrows():
            try:
                new_jobs_efc(row[0], row[1], save_to_excel=save)
                print(' ')
                print(' ')

            except:
                print('Error loading new jobs for ' +
                      '\033[1m' + row[0] + '\033[0m' +
                      ' query. Continuing onto the next query...')
                print(' ')
                print(' ')
                continue

if see_recent:
    for idx, row in targetlinks_df.iterrows():
        if row[5] == speed:
            try:
                if row[2] == 'W' and row[3] == 'G' and row[4] == 'Workday':
                    print(create_jobsdf_workday_selenium_bs(row[0], row[1],
                                                            save_to_excel=False,
                                                            recently_posted=see_recent))

                    print(' ')
                    print(' ')

            except:
                print('Error loading new jobs for ' +
                      '\033[1m' + row[0] + '\033[0m' +
                      '. Continuing onto the next company...')
                print(' ')
                print(' ')
                continue
