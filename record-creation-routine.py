import os
import shutil
from finder_sidebar_editor import FinderSidebar

dirLst = ['Folder Name 1', 'Folder Name 2']

parent_dir = 'enter directory path to house folders in dirLst'

for dir in dirLst:
    # Create folder
    path = os.path.join(parent_dir, dir)
    os.mkdir(path)

    # Add CV files
    cv_location = 'enter directory path where CV files are located'
    cv_files = ['cvfname.docx', 'cvfname.pdf']

    for f in cv_files:
        src = os.path.join(cv_location, f)
        shutil.copy2(src, path)

    # Add resulting folder to favourites
    FinderSidebar().add(path)




# Rough
#print(os.path.abspath(directory))
#print(os.path.join(cv_location, cv_files[0]))