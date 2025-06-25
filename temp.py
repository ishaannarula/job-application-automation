# import os
# import pandas as pd

# desired_width = 320
# pd.set_option('display.width', desired_width)
# pd.set_option('display.max_columns', 10)
# pd.set_option('display.max_rows', 1000)
# pd.set_option('display.max_colwidth', None) #To display full URL in dataframe


# excelFiles = os.listdir('Dataframes/')
# for file in excelFiles:
#     if file == 'eFinancial Careers' or file == '.DS_Store': continue

#     else:
#         # Read the dataframe in each Excel file in the Dataframes directory
#         df = pd.read_excel('Dataframes/' + str(file))

#         if df.empty: continue

#         # Narrow down the df to dates when scraping is done
#         filtDf = df[
#             (df['Date Viewed'].dt.date == pd.to_datetime('2023-08-24').date())
#             | (df['Date Viewed'].dt.date == pd.to_datetime('2023-08-25').date())
#         ]

#         print('Jobs saved in ' + file + ' file scraped on 24/08 and 25/08 but not reviewed')
#         print('')
#         print(filtDf)
#         print('')

import webbrowser
import tempfile
import pandas
from track_new_jobs_greenhouse import *
from track_new_jobs_workday import *
from track_new_jobs_with_selenium import *
from track_new_jobs_efc import *
import time
import warnings
warnings.filterwarnings('ignore')

df = create_jobsdf_workday_selenium_bs('Millennium', 'https://mlp.wd5.myworkdayjobs.com/en-US/mlpcareers', save_to_excel=False, recently_posted=False)
df_a = new_jobs_workday('Millennium Management', 'https://mlp.wd5.myworkdayjobs.com/en-US/mlpcareers', save_to_excel = False)

df2 = create_jobsdf_greenhouse('Airbnb', 'https://boards.greenhouse.io/embed/job_board?for=airbnb', save_to_excel=False)
df2_a = new_jobs_greenhouse('Airbnb', 'https://boards.greenhouse.io/embed/job_board?for=airbnb', save_to_excel = False)

df3 = create_jobsdf_withSelenium('Point72', 'https://careers.point72.com/', save_to_excel=False)


