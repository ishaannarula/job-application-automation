from track_new_jobs_greenhouse import *
from track_new_jobs_workday import *
from track_new_jobs_with_selenium import *
import time

bool = True
speed = 'Okay'
see_recent = False

targetlinks_df = pd.read_excel('careerswebsitelinks.xlsx')

if not see_recent:
    for idx, row in targetlinks_df.iterrows():
        if row[5] == speed:
            try:
                if row[2] == 'W' and row[3] == 'G' and row[4] == 'Workday':
                    new_jobs_workday(row[0], row[1], save_to_excel=bool)

                    print(' ')
                    print(' ')

                elif row[2] == 'W' and row[3] == 'G' and row[4] == 'Greenhouse':
                    new_jobs_greenhouse(row[0], row[1], save_to_excel=bool)

                    print(' ')
                    print(' ')

                elif row[2] == 'W' and row[3] == 'G' and row[4] == 'Varied (Selenium)':
                    new_jobs_withSelenium(row[0], row[1], save_to_excel=bool)

                    print(' ')
                    print(' ')

            except:
                print('Error loading new jobs for ' +
                      '\033[1m' + row[0] + '\033[0m' +
                      '. Continuing onto the next company...')
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
