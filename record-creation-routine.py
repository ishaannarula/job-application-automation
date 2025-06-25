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

var = 'destroy'  # 'create' or 'destroy'

dirLst = [

    "AlphaGrep Securities – Trading Analyst – 8027780002 – (Location not specified)",
    "Bridgewater Associates – Investment Engineer – 8034705002 – New York, NY, USA",
    "DataCamp – Senior Marketing Data Analyst – 6983066 – Europe (Remote)",
    "DataCamp – Senior Marketing Data Analyst – 6983086 – Europe (Remote)",
    "DataCamp – Senior Marketing Data Analyst – 6983089 – Europe (Remote)",
    "Fidelity Investments – Lead, Data Analytics and Insights – 2112010 – Bangalore, Karnataka, India",
    "Flow Traders – Macro Strategy Analyst – 6980497 – Amsterdam, Netherlands",
    "Garda Capital Partners – Risk Analyst – 4242729004 – Geneva, Switzerland",
    "Garda Capital Partners – Senior Risk Analyst – 5112062004 – Singapore",
    "LSEG – Senior Data Engineer – R0105833 – London, United Kingdom",
    "LSEG – Lead Data Engineer – R0106650 – London, United Kingdom",
    "Schonfeld Strategic Advisors – Optimization Quantitative Researcher (Neutrality) – 6984817 – New York, NY, USA",
    "Schonfeld Strategic Advisors – Quantitative Researcher (Equity Derivatives) – 6985245 – New York, NY, USA",
    "T. Rowe Price – Senior Equity Portfolio Investment Analyst – 76911 – Hong Kong",
    "Tudor Investment Corporation – Low Latency Quantitative Researcher (Pipeline Team) – 5358163 – New York, NY, USA",
    "Tudor Investment Corporation – Medium Frequency Quantitative Researcher (Pipeline Team) – 5358422 – New York, NY, USA",
    
    
    

    # Pending
    # "Eastspring Investments - Data Engineer - 25040336 - Singapore",
    # "Khan Academy - Analytics Manager - 6706448 - India",

    # 18 April 2025
    # "Optiver - Quantitative Researcher - HFT Futures or Equities - 7940581002 - Amsterdam",
    # "Optiver - Data Engineer - 7899128002 - Sydney",
    # "Optiver - Quantitative Developer - 7887332002 - Amsterdam",
    # "Optiver - Quantitative Trader or Researcher - Systematic Options Trading - 7251404002 - Chicago",
    # "Optiver - Quantitative Researcher - SVT - 7801772002 - Chicago",

    # Consructed response
    # "Coinbase - Senior Analytics Engineer - 6884049 - Remote - Canada",
    # "Coinbase - Senior Analytics Engineer - 6884044 - Remote - USA",

]



parent_dir = '/Users/ishaan/Library/CloudStorage/GoogleDrive-ishaan.narula1@gmail.com/My Drive/Career/Jobs/Search/Applications/To be Added to Excel Database/'
sidebar = FinderSidebar()

if var == 'create':

    for directory in dirLst:
        # Create folder
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        # Add CV files
        cv_location = '/Users/ishaan/Library/CloudStorage/GoogleDrive-ishaan.narula1@gmail.com/My Drive/Career/CVs/7 with morningstar/'
        cv_files = ['CV_Ishaan Narula.pdf']

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
        sidebar.add(path)

elif var == 'destroy':
    for directory in dirLst:
        sidebar.remove(directory)





