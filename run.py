from track_new_jobs_greenhouse import *
from track_new_jobs_workday import *

targetlinks_df = pd.read_excel('careerswebsitelinks.xlsx')
for idx, row in targetlinks_df.iterrows():
    if (row[2] == 'W' and row[3] == 'G' and row[4] == 'Workday'):
        new_jobs_workday(row[0], row[1], save_to_excel = False)
        print(' ')
        print(' ')

    elif (row[2] == 'W' and row[3] == 'G' and row[4] == 'Greenhouse'):
        new_jobs_greenhouse(row[0], row[1], save_to_excel = False)
        print(' ')
        print(' ')

