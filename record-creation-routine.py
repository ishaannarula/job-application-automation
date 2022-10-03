import os
import shutil
from finder_sidebar_editor import FinderSidebar

var = 'create'

dirLst = ['Zego - Lead Data Scientist (Pricing) (rbyAQxoXgSoprpEoMoh5Zs) - UK (Remote Working)',
          'Point72 - Cubist - ENTRY-LEVEL QUANTITATIVE RESEARCHER (CSS-0010275) - New York | London | Hong Kong | Singapore | Dubai, UAE',
          'Point72 - Cubist - QUANTITATIVE ANALYST (CSS-0010274) - New York',
          'Point72 - RESEARCH ANALYST AEJ - QUANTITATIVE ANALYST (LSI-0010244) - Hong Kong',
          'Schonfeld - Quantitative Researcher (4590869) - Singapore',
          'Schonfeld - Quantitative Researcher (4590868) - Hong Kong']

parent_dir = '/Volumes/GoogleDrive/My Drive/Career/Jobs/Search/Applications/To be Added to Excel Database/'

if var == 'create':
    for dir in dirLst:
        # Create folder
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)

        # Add CV files
        cv_location = '/Volumes/GoogleDrive/My Drive/Career/CVs/6 After MS Versions/English CVs/Markets, Hedge Funds, Investment Management/'
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