import os
import shutil
from finder_sidebar_editor import FinderSidebar

var = 'create'

dirLst = []

parent_dir = ''

if var == 'create':
    for dir in dirLst:
        # Create folder
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)

        # Add CV files
        cv_location = ''
        cv_files = ['CV_Ishaan Narula.docx', 'CV_Ishaan Narula.pdf']

        for f in cv_files:
            src = os.path.join(cv_location, f)
            shutil.copy2(src, path)

        # Add resulting folder to favourites
        FinderSidebar().add(path)

#elif var == 'destroy':
#    #Remove folders in dirLst from favourites after applying
#    for dir in dirLst:
#        path2 = os.path.join(parent_dir, dir)
#        print(path2)
#        FinderSidebar().remove(path2)



# Rough
#print(os.path.abspath(directory))
#print(os.path.join(cv_location, cv_files[0]))