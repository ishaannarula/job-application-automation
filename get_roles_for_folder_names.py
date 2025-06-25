import os
import pandas as pd
import datetime as dt

urls = [
    'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-Analyst---New-Product-Development_REQ-041655'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Lead-Quantitative-Analyst_REQ-036491'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-analyst_REQ-036546'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-Analyst--Index-Management---Analytics_REQ-040360'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-analyst--Index-Management---Analytics_REQ-040313'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/SQL-Data-Engineer_REQ-041742-1'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-Analyst_REQ-041406'
    , 'https://morningstar.wd5.myworkdayjobs.com/en-US/Americas/job/Mumbai/Quantitative-Analyst---New-Product-Development---Morningstar-Indexes_REQ-041839'
]

folderNames = {}

excelFiles = os.listdir('Dataframes/')

for file in excelFiles:
    if file == 'eFinancial Careers' or file == '.DS_Store': continue

    else:
        # Read the dataframe in each Excel file in the Dataframes directory
        df = pd.read_excel('Dataframes/' + str(file))

        if df.empty: continue

        # Narrow down the df to dates when scraping is done
        filtDf = df[
            (
                (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-22').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-23').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-24').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-25').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-26').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-27').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-28').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-29').date())
                | (df['Date Viewed'].dt.date == pd.to_datetime('2023-11-30').date())
            )
        ]

        if filtDf.empty: continue

        for idx, row in filtDf.iterrows():
            # Check if a URL is found in urls list
            if filtDf.loc[idx, 'URL'] in urls:
                url = filtDf.loc[idx, 'URL']
                folderName = filtDf.loc[idx, 'Company'] + ' - ' + filtDf.loc[idx, 'Role']
                folderNames[url] = folderName

# Print folder names corresponding to the various urls in the same order as the urls appear in
# the urls list

for url in urls:
    print(', ' + "'" + folderNames[url] + "'")


print('')
print('No. of input URLs:', len(urls))
print('No. of folder names created:', len(folderNames))

