from track_new_jobs_greenhouse import *
from track_new_jobs_workday import *
from track_new_jobs_with_selenium import *
from track_new_jobs_efc import *
import time

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
                    if row[2] == 'W' and row[3] == 'G' and row[4] == 'Workday':
                        new_jobs_workday(row[0], row[1], save_to_excel=save)

                        print(' ')
                        print(' ')

                    elif row[2] == 'W' and row[3] == 'G' and row[4] == 'Greenhouse':
                        new_jobs_greenhouse(row[0], row[1], save_to_excel=save)

                        print(' ')
                        print(' ')

                    elif row[2] == 'W' and row[3] == 'G' and row[4] == 'Varied (Selenium)':
                        new_jobs_withSelenium(row[0], row[1], save_to_excel=save)

                        print(' ')
                        print(' ')

                except:
                    print('Error loading new jobs for ' +
                          '\033[1m' + row[0] + '\033[0m' +
                          '. Continuing onto the next company...')
                    print(' ')
                    print(' ')
                    continue

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