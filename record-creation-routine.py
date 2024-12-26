import os
import glob
import shutil
from finder_sidebar_editor import FinderSidebar
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from pywebcopy import save_webpage
from helper_functions import local_html_to_pdf

var = 'create'


dirLst = [
    # 'Stimulus - Remote Software engineer (1539721e-7c7d-4f45-a5b0-17e5c02d7bd0) -  Amsterdam',
    # 'Plumerai - Software Engineer (D25FB0EE0B) - Amsterdam',
    # 'Optiver - Capital & Credit Risk Analyst (6550563002) - AMSTERDAM',

# Saved on Raindrop
    # 'NatWest Group - Data Scientist - Climate - 18837133 - London',
    # 'Macquarie Group - Data Scientist or Senior Analyst - 18864560 - Sydney',

    # 'Beacon - Senior Product Manager - 5537662003 - London or Remote',
    # 'M&G plc - Research Analyst - Climate, Energy & Utilities - R09921 - London',
    # 'State Street - Quantitative Researcher, Officer - R-730133 - Cambridge',
    # 'State Street - Global Markets Entry-Level Rotational – Professional Development Program, Senior Associate - R-729822 - Sydney',
    # 'HSBC - Quantitative Equity Analyst, HSBC Global Asset Management - 0000IOER - Birmingham',

    # Saved on 10 March 2023
    # 'Course Hero - Senior Data Scientist, Monetization - 4850553 - Vancouver, BC & Toronto, ON',
    # 'MFS Investment Management - EM Corporates Fixed Income Research Associate - MFS-220716 - Boston',
    # 'Neuberger Berman - Research Analyst - R0007681 - Hong Kong',
    # 'Neuberger Berman - Analyst - R0007971 - New York, NY, BM01 - Bermuda',

    # Saved on 11 March 2023
    # 'Adblock - Remote Controller, Financial Planning & Analysis Manager - San Francisco',
    # 'Lifetimely - Remote Senior Product Manager - Singapore',
    # 'Toggl - Remote Product Marketing Manager - Tallinn',
    # 'BP - Data Strategist - Quant Researcher - 143320BR - Singapore - Flexible, United Kingdom - South East - London, United States - Illinois - Chicago',
    # 'Bloomberg - Financial Engineer - 100886 - London',
    # 'Blackstone - Associate - ICS, Mumbai - 25927 - Mumbai',
    # 'DRW - Power Risk Manager - 4923654 - Chicago',
    # 'Neuberger Berman - Analyst or Associate Secondaries - R0007841 - London',
    # 'Point72 - BUSINESS ANALYST, L-S EQUITY - IVS-0010799 - New York',
    # 'S&P Global - Analyst, Equity Research or Fixed Income - 282204 - Buenos Aires, AR',
    # 'State Street -  FX Trading Officer - R-730340 - Taipei',

    # Saved on 13 March 2023
    # 'BlackRock - Associate, Credit Research, SSA - R230734 - Mumbai, Gurgaon',
    # 'CMC Markets - Junior Quant Developer - CMC3077 - London',
    # 'Optiver - Macro Analyst - 6661535002 - SYDNEY',
    # 'Optiver - Macro Strategist - 6661537002 - SYDNEY',
    # 'T. Rowe Price - Investment Specialist – Fixed Income - 64742 - San Francisco',
    # 'Western Union - Manager, Data Engineering - JR0111051 - Pune',
    # 'Western Union - Senior Analyst, Customer Analytics(Data Science, SQL, PowerBI) - JR0112883 - Pune',
    # 'Squarepoint Capital - Desk Quant Analyst - 2546549 - London, Madrid, Montreal, Bangalore, Singapore',
    # 'FTI Consulting - Senior Quantitative Energy Specialist | Capital Markets |Economic and Financial Consulting - 211O9 - London',
    # 'FTI Consulting - Quantitative Energy Specialist | Capital Markets | Economic and Financial Consulting - 211OA - London',

    # 15 March 2023
    # 'PwC - Quantitative Analyst – Pricing & Traded Risk - 14155733 - London',
    # 'Google - Software Engineer III, Project Starline - 110260539117970118 - Mountain View, CA, USA, Seattle, WA, USA',
    # 'Google - Software Engineer III, Full Stack, Core - 114961493163680454 - USA Multiple Locations',
    # 'BlackRock - Data Pipeline Engineers - Associate - ATL - R230648 - Atlanta',
    # 'Brevan Howard - Quant Analyst - JR100270 - London',
    # 'Brevan Howard - Quant Analyst - JR100272 - Geneva',
    # 'Brevan Howard - Quant Analyst - JR100273 - Singapore',
    # 'Centrica - Python Developer - R0040614 - Aalborg',
    # 'Centrica - Market Insight Analyst - R0038515 - Flexible, Leicester, Windsor',
    # 'GAM Investments - ESG Analyst - JR740 - London, Dublin',
    # 'M&G plc - Equity Investment Risk Analyst - R10793 - London',
    # 'Mako Trading - Market Risk Analyst - 6664124002 - London',
    # 'Man Group - Asset Management Analyst - JR004022 - Charlotte, NC',
    # 'Millennium Management - Electronification of Trading - Data Analysis/ML engineer - REQ-16746 - Bangalore',
    # 'Vanguard - Quantitative Model Developer - 154093 - Malvern, PA'


# eFinancial Careers
#     'Danos Group - FM Risks & Valuations Quantitative Analyst - 18735180 - Singapore',
#     'United Overseas Bank - Manager, Quantitative Investment Analyst, UOB Asset Management - 18825566 - Singapore',
#     'eFinancial Careers - Non-disclosed - Senior Data Engineer – New Data Science & Research Division – Python / SQL - 18977373 - New York',
#     'Stanford Black - Senior Data Engineer - 18976243 - New York',
#     'Anson McCade - Quantitative Researcher or Trader Fixed Income - 18980634 - London',
#     'Innovation Programmes and Projects Asia Limited (IPPA) - Data Scientist - 18906386 - Singapore',
#     'Anson McCade - Python Quantitative Developer - 18964842 - London',
#     'Macquarie Group - Data Scientist or Senior Analyst - 18970670 - Sydney',
#     'Deutsche Bank - Quantitative Analyst (m-f-x) - Algo Trading Model Validation Specialist - 18974827 - Berlin',
#     'Deutsche Bank - Quantitative Strategist (m-f-x) in Group Strategic Analytics - 18975090 - Berlin',
#     'HKHR - Quantative Risk Researcher (60k pm ++) - 18968649 - Hong Kong',
#     'TEKsystems (Allegis Group Singapore Pte Ltd) - Data Scientist - 18966535 - Singapore',
#     'TEKsystems (Allegis Group Singapore Pte Ltd) - Data Scientist - 18948893 - Singapore',
#     'Kite Human Capital - Quant Developer - Pricing Analytics - London - Competitive Salary + Bonuses - 18981794 - London',
#     'Anson McCade - Quantitative Developer (Intraday HFT Futures) - 18964839 - London',
#     'Anson McCade - Python Quantitative Developer - 18964842 - London',
#     'Anson McCade - Quantitative Researcher - Data Science - 18977374 - London',
#     'Anson McCade - Quantitative Researcher or Trader Fixed Income - 18980634 - London',
#     'Webbe International - Equity Finance Quant or Strategist - 18975408 - Hong Kong',
#     'S&P Global - Quantitative Product Manager - 18947479 - Chicago',
#     'Goldman Sachs - Risk-NEW YORK-Associate-Quantitative Engineering - 18975834 - New York',
#     'eFinancial Careers - Non-disclosed - Exotics Quantitative Research - 18435900 - New York',
#     'State Street - Quant Equity Strategist, Assistant Vice President - 18954375 - Boston',
#     'Selby Jennings - Quantitative Researcher (Trading Ops) - 18975645 - Singapore',
#     'Rivertowns Group - Senior Quantitative Analyst - 18971796 - New York',
#     'Selby Jennings - Quant Researcher (Portfolio Construction) - 18944512 - New York',
#     'Falcon Brook Search - Gas and Power Quantitative Analyst - 18964807 - London',
#     'eFinancial Careers - Non-disclosed - Sr Analyst - Event-Driven - 18944730 - New York',
#     'JK Barnes - Quantitative Researcher - 18972261 - New York',
#     'Rimrock Associates - Electronic Trading Equity or Algo Support - 00469131 - New York',
#     'Profile Search & Selection - Equity Analyst, Asian Hedge Fund - 18966487 - Singapore',
#     'Hays - Finance Manager Germany - 8944146 - Wiesbaden',
#     'FXC Intelligence - VP Finance - 18971237 - London'


# Constructed Response
    # 'Wise - Product Manager or Senior Product Manager - 4455823 - Budapest',
    # 'Borg Collective - Data Scientist (Remote) - d21miiNM75oZYdeUZdEWvL - Berlin, Remote',
    # 'MFS Investment Management - Rotational Development Program Associate - MFS-230026 - Boston',
    # 'Wise - India Expansion Lead - 4905560 - Mumbai',
    ]

parent_dir = '/Volumes/GoogleDrive/My Drive/Career/Jobs/Search/Applications/To be Added to Excel Database/'

if var == 'create':

    for directory in dirLst:
        # Create folder
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        # Add CV files
        cv_location = '/Volumes/GoogleDrive/My Drive/Career/CVs/6 After MS Versions/English CVs/Markets, Hedge Funds, Investment Management/'
        cv_files = ['CV_Ishaan Narula.docx', 'CV_Ishaan Narula.pdf']

        for f in cv_files:
            src = os.path.join(cv_location, f)
            shutil.copy2(src, path)

        # Save job description as HTML
        # Does not work for Workday, Workable, BAM Funds websites
        # save_webpage(
        #     url=url,
        #     project_folder=path,
        #     project_name="Job Description",
        #     bypass_robots=True,
        #     debug=False,
        #     open_in_browser=True,
        #     delay=None,
        #     threaded=False,
        # )

        # Save local HTML as PDF

        # Maybe you can save all JDs in one folder (eg Downloads), and move each to its respective folder
        # Only viable if the downloads are ordered by time of saving. Bcs then, for the oldest download move it to the 1st folder and so on

        # Add resulting folder to favourites
        FinderSidebar().add(path)

elif var == 'destroy':
    for directory in dirLst:
        FinderSidebar().remove(directory)




