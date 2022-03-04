import os
import shutil
from finder_sidebar_editor import FinderSidebar

dirLst = []

parent_dir = 'enter file path'

for dir in dirLst:
    # Create folder
    path = os.path.join(parent_dir, dir)
    os.mkdir(path)

    # Add CV files
    cv_location = 'enter file path'
    cv_files = ['CV_Ishaan Narula.docx', 'CV_Ishaan Narula.pdf']

    for f in cv_files:
        src = os.path.join(cv_location, f)
        shutil.copy2(src, path)

    # Add resulting folder to favourites
    FinderSidebar().add(path)




# Rough
#print(os.path.abspath(directory))
#print(os.path.join(cv_location, cv_files[0]))