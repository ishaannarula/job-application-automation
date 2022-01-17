# Create folder
import os
directory = 'Aberdeen Standard Investments - Senior Investment Analyst (R0067938) - Edinburgh'
parent_dir = '/Volumes/GoogleDrive/My Drive/Career/Search/Applications/To be Added to Excel Database/'
path = os.path.join(parent_dir, directory)
os.mkdir(path)

# Add CV files
cv_location = 'enter file path'
cv_files = ['fname.docx', 'fname.pdf']

import shutil
for f in cv_files:
    src = os.path.join(cv_location, f)
    shutil.copy2(src, path)

# Add resulting folder to favourites
from finder_sidebar_editor import FinderSidebar
FinderSidebar().add(path)

# Rough
#print(os.path.abspath(directory))
#print(os.path.join(cv_location, cv_files[0]))