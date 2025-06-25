import os
import ctypes
from ctypes import wintypes
import glob
import shutil
# from finder_sidebar_editor import FinderSidebar
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# from pywebcopy import save_webpage
# from helper_functions import local_html_to_pdf

var = 'create'
parent_dir = 'C:\\Users\\in\\OneDrive - Association Groupe ESSEC\\Temp Folders\\To be Added to Excel Database\\'
dirLst = [
    # 'Stimulus - Remote Software engineer (1539721e-7c7d-4f45-a5b0-17e5c02d7bd0) -  Amsterdam',
    # 'Plumerai - Software Engineer (D25FB0EE0B) - Amsterdam',
    # 'Optiver - Capital & Credit Risk Analyst (6550563002) - AMSTERDAM',

# Saved on Raindrop

                                                    # TO BE SORTED
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
                                                    # 'Bloomberg - Financial Engineer - 100886 - London',
                                                    # 'Blackstone - Associate - ICS, Mumbai - 25927 - Mumbai',
                                                    # 'DRW - Power Risk Manager - 4923654 - Chicago',
                                                    # 'Neuberger Berman - Analyst or Associate Secondaries - R0007841 - London',
                                                    # 'Point72 - BUSINESS ANALYST, L-S EQUITY - IVS-0010799 - New York',
                                                    # 'S&P Global - Analyst, Equity Research or Fixed Income - 282204 - Buenos Aires, AR',
                                                    # 'State Street -  FX Trading Officer - R-730340 - Taipei',

                                                    # Saved on 13 March 2023
                                                    # 'BlackRock - Associate, Credit Research, SSA - R230734 - Mumbai, Gurgaon',
                                                    # 'Optiver - Macro Analyst - 6661535002 - SYDNEY',
                                                    # 'Optiver - Macro Strategist - 6661537002 - SYDNEY',
                                                    # 'T. Rowe Price - Investment Specialist – Fixed Income - 64742 - San Francisco',
                                                    # 'Western Union - Manager, Data Engineering - JR0111051 - Pune',
                                                    # 'Western Union - Senior Analyst, Customer Analytics (Data Science, SQL, PowerBI) - JR0112883 - Pune',
                                                    # 'Squarepoint Capital - Desk Quant Analyst - 2546549 - London, Madrid, Montreal, Bangalore, Singapore',
                                                    # 'FTI Consulting - Senior Quantitative Energy Specialist | Capital Markets |Economic and Financial Consulting - 211O9 - London',
                                                    # 'FTI Consulting - Quantitative Energy Specialist | Capital Markets | Economic and Financial Consulting - 211OA - London',

                                                    # 15 March 2023
                                                    # 'Google - Software Engineer III, Project Starline - 110260539117970118 - Mountain View, CA, USA, Seattle, WA, USA',
                                                    # 'Google - Software Engineer III, Full Stack, Core - 114961493163680454 - USA Multiple Locations',
                                                    # 'BlackRock - Data Pipeline Engineers - Associate - ATL - R230648 - Atlanta',
                                                    # 'Centrica - Python Developer - R0040614 - Aalborg',
                                                    # 'Centrica - Market Insight Analyst - R0038515 - Flexible, Leicester, Windsor',
                                                    # 'GAM Investments - ESG Analyst - JR740 - London, Dublin',
                                                    # 'M&G plc - Equity Investment Risk Analyst - R10793 - London',
                                                    # 'Man Group - Asset Management Analyst - JR004022 - Charlotte, NC',

                                                    # 19 March 2023
                                                    # 'Ramp - Senior Data Scientist | Data Products -  6668077002 - New York',

                                                    # Saved on 21 March 2023
                                                    # 'FARFETCH - Data Scientist - Search - ef06574c-e1a0-4d8c-871c-7aadb7c7180e - LISBON',
                                                    # 'FARFETCH - Data Scientist - Search Marketplace - 87a38a57-d809-4b0e-9748-e9d8e1cba39a - PORTO',
                                                    # 'FARFETCH - Data Scientist - dded0639-c4dc-46db-badd-ea1c3b25e745 - PORTO',
                                                    # 'FARFETCH - Senior Data Scientist - Experimentation - 660e2e0f-07ff-46fe-ae4b-90a8f092639f - DELHI',
                                                    # 'FARFETCH - Senior Machine Learning Engineer - 7d192558-2d4d-4f06-bcb2-899f23aacaa8 - PORTO',
                                                    # 'FARFETCH - Data Product Manager - b48a9428-6048-435d-b6a0-0b330d324208 - PORTO',
                                                    # 'FARFETCH - Data Product Manager - 8f55607a-188e-47b2-b5a0-82312c11e642 - LISBON',
                                                    # 'FARFETCH - Product Manager - Data - dd057a7a-4d36-4fae-9421-396355394c14 - PORTO',
                                                    # 'FARFETCH - Product Manager - Data - 79a7a61c-0a5c-4eaf-8246-d4a0cd4eac75 - LISBON',
                                                    # 'FARFETCH - Data Scientist - Search - ef06574c-e1a0-4d8c-871c-7aadb7c7180e - LISBON'

                                                    # Saved on 23 March 2023
                                                    # 'Ramp - Senior Data Scientist, Product - 6673436002 - New York, Miami, Remote',

    # Saved on 16 July 2023
    # 'Capula Investment Management - Risk Developer - F7687409FC - London',
    # 'Capula Investment Management - Front Office Excel Developer - 1D068547E2 - London',
    # 'Capula Investment Management - Python Developer - 5BF2988D70 - New York',
    # 'Capula Investment Management - Economic Analyst - 35C8F45C3D - London',
    # 'Capula Investment Management - Capula Analyst Programme - D78FBFE445 - London',
    # 'Capula Investment Management - Capula Analyst Programme - 7D45C28D2B - Singapore',


    # Saved on 22 August 2023
    # , 'Figma - Data Scientist, Early Career (2024) - 4945812004 - San Francisco, CA, New York, NY, United States'
    # , 'Figma - Data Scientist Intern (2024) - 4956894004 - San Francisco, CA, New York, NY, United States'
    # , 'Figma - Software Engineer - Early Career (2024) - 4941380004 - San Francisco, CA, New York, NY, United States'
    # , 'Figma - Software Engineer Intern (2024) - 4942607004 - San Francisco, CA, New York, NY, United States'
    # , 'Figma - Business Analyst - 4951984004 - San Francisco, CA, New York, NY, United States'
    # , 'Figma - Data Engineer - Product - 4958498004 - San Francisco, CA, New York, NY, United States'
    # , 'PGIM - PGIM Private Capital – Investment Analyst, Structured Credit (Newark, NJ, Hybrid) - R-115137 - Newark, NJ, USA'
    # , 'TIAA - 2024 Early Talent Rotational Program Nuveen Asset Management - R230700512 - Chicago, IL, USA'
    # , 'TIAA - 2024 Early Talent Rotational Program Nuveen Equities and Fixed Income - R230700639 - Chicago, IL, USA'

    # Saved on 24th August 2023
    # , 'Bracebridge Capital - 2024 Winternship - 4308226005 - Boston, MA'
    # , 'Fidelity Investments - Senior Manager, Data Science - 2081935 - Westlake, TX'
    # , 'Discord - Senior Data Scientist, Analytics (Nitro Perks) - 4014761002 - San Francisco, CA or Remote'

    # , 'Deliveroo - Senior Data Analyst - 5295296 - Hyderabad, India (Main Office)'

        'Talos - Data Engineer Intern - 5040783004 - London'

    # eFinancial Careers







# Constructed Response

    # , 'Tide - Senior Lead Data Scientist - 5795319003 - Delhi NCR, Remote'
    # , 'Tide - Senior Lead Data Scientist - 5795318003 - Hyderabad, Remote'
    # , 'Tide - Senior Lead Data Scientist - 5795320003 - Bengaluru, Remote'

    # Saved on 18 October 2023
    # , 'Optiver - Graduate HFT Researcher (2024 Start - Austin) - (PhD Preferred) - 6805890002 - Austin, Texas, United States'
    # , 'Optiver - Trading Risk Analyst - 6964305002 - Amsterdam, North Holland, Netherlands'
    # , 'Reddit - Data Science Manager, Ads Platform & Experience - 5392918 - Remote - United States'
    # , 'Reddit - Staff Data Scientist, Core Experience Analytics - 5249535 - Remote - United States'
    # , 'CoinList - Senior Data Engineer - 6966791002 - SF, NY, Montreal - San Francisco, CA, New York, NY, Montreal, Canada'

    # OLD BUT OPEN AS ON 11 SEPT 2023
    # 'Sourcegraph - Product Manager, Code AI Platform - 4904034004 - Remote',
    # 'Remote - Data Analyst - 5563412003 - Remote-Argentina',
    # 'Remote - Data Analyst - 5564850003 - Remote-New-Zealand',
    # 'Remote - Data Analyst - 5564844003 - Remote-South-Korea',
    # 'Remote - Senior Data Engineer - 5662654003 - Remote-Indonesia'
    # , 'Remote - Senior Data Engineer - 5661275003 - Remote-Vietnam'
    # , 'Remote - Senior Data Engineer - 5662655003 - Remote-Taiwan'
    # , 'Remote - Senior Data Engineer - 5662656003 - Remote-South Korea'
    # , 'Flow Traders - Graduate Trader - 2539283 - Amsterdam'
    # , 'Flow Traders -  Digital Assets Graduate Trader - 4136522 - Amsterdam'
    # , ' Wintermute - Quantitative Researcher - c550e7cb-601b-4ac8-b5a7-6479f0d0a2de- LONDON'

    # SAVED ON 9 SEPT 2023
    # , 'CoinList - General Interest - Opportunistic - 5649028002 - Anywhere'
    # , 'CoinList - Senior Software Engineer - Trading Team - 6879412002 - Remote (Americas, EMEA, APAC regions)'
    # , 'CoinList - Senior Software Engineer - Money Team - 4036680002 - Remote (Americas, EMEA, APAC regions)'

    # SAVED ON 11 SEPT 2023
    # , 'Chainlink - Market Strategy Manager, Capital Markets - b7abcfd2-cb2c-4ad1-ae44-8eacdcf937a9 - UNITED STATES, REMOTE'
    # , 'Chainlink - Research Engineer - 53bbb447-181c-472f-b900-6d3550d95b70 - MADRID, REMOTE'
    # , 'Chainlink - Research Internship - c79ebded-4d90-417f-8958-fbaffdae6018 - ZUG, REMOTE'
    # , 'Chainlink - Strategic Finance Manager - b3de1995-8e96-480f-ab4d-e5939db7b351 - UNITED STATES'
    # , 'Chainlink - FP&A Manager - ba4bc1fc-574f-45a0-9bb7-16e488302591 - MEXICO, REMOTE'
    # , 'Chainlink - Go-To-Market Researcher- 1d6e4101-1c43-4177-951a-a0f4f4f55b9e - LONDON, REMOTE'
    # , 'Cleo - Product Analyst - 6520205002 - London'
    # , 'Cleo - Product Analyst, Risk & Payments - 6912046002 - London'
    # , 'Cleo - Senior Credit Risk Analyst - 6907618002 - New York, US'
    # , 'Cleo - Senior Product Analyst - Financial Literacy - 6895622002 - London'
    # , 'Invisible Technologies - Senior Product Manager - 4123844101 - North, South America - Remote'
    # , 'Invisible Technologies - Senior Software Engineer - AI, ML - 4215590101 - United States - Remote'
    # , 'Invisible Technologies - Technical Lead - AI Enablement - 4201162101 - United States - Remote'
    # , 'Customer.io - Senior Product Manager, Mobile - 5283615 - Americas Remote'
    # , 'Customer.io - Future Opportunities - 2182646 - Remote'

    # SAVED ON 15 SEPT 2023
    # , 'Upwork - Product Manager, Enterprise Growth - 5696392003 - Remote'
    # , 'Upwork - Sr. Analyst, Trust and Safety Product Analytics - 5677241003 - Remote'


]


if var == 'create':
    for directory in dirLst:
        # Create folder
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

        # Add CV files
        cv_location = 'C:\\Users\\in\\OneDrive - Association Groupe ESSEC\\Career\\CVs\\6 After MS Versions\\English CVs\\Quant, Data Science, Tech\\'
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
        # shell32 = ctypes.WinDLL('shell32.dll')
        # CSIDL_APPDATA = 26  # Represents the AppData folder, which is typically used for Quick Access links
        # SHGFP_TYPE_CURRENT = 0
        # PIDLIST_ABSOLUTE = 0x08
        # SFGAO_FOLDER = 0x20000000
        #
        # # Define the necessary IID_IShellItem constant
        # class GUID(ctypes.Structure):
        #     _fields_ = [
        #         ("Data1", ctypes.c_ulong),
        #         ("Data2", ctypes.c_ushort),
        #         ("Data3", ctypes.c_ushort),
        #         ("Data4", (ctypes.c_ubyte * 8)),
        #     ]
        #
        #
        # IID_IShellItem = GUID(0x43826D1E, 0xE718, 0x42EE,
        #                       (ctypes.c_ubyte * 8)(0xBC, 0x55, 0xA1, 0xE2, 0x61, 0xC3, 0x7B, 0xFE))
        #
        # path_buffer = wintypes.LPWSTR()
        # shell32.SHGetFolderPathW(0, CSIDL_APPDATA, 0, SHGFP_TYPE_CURRENT, path_buffer)
        # quick_access_path = path_buffer.value
        #
        # item = ctypes.POINTER(ctypes.c_void_p)()
        # shell32.SHCreateItemFromParsingName(path, None, IID_IShellItem,
        #                                     ctypes.byref(item))
        #
        # quick_access = ctypes.POINTER(ctypes.c_void_p)()
        # shell32.SHGetKnownFolderItem(SFGAO_FOLDER, item, IID_IShellItem, ctypes.byref(quick_access))
        #
        # shell32.ILFree(item)
        # shell32.ILFree(quick_access)



elif var == 'destroy':
    # for directory in dirLst:
    #     FinderSidebar().remove(directory)
    pass