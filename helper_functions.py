import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtPrintSupport, QtGui

def get_all(myjson): #U
    ''' Recursively find the keys and associated values in all the dictionaries
        in the json object or list.
    '''
    if isinstance(myjson, dict):
        for jsonkey, jsonvalue in myjson.items():
            if not isinstance(jsonvalue, (dict, list)):
                yield jsonkey, jsonvalue
            else:
                for k, v in get_all(jsonvalue):
                    yield k, v
    elif isinstance(myjson, list):
        for element in myjson:
            if isinstance(element, (dict, list)):
                for k, v in get_all(element):
                    yield k, v


def df_column_switch(df, column1, column2):
    i = list(df.columns)
    a, b = i.index(column1), i.index(column2)
    i[b], i[a] = i[a], i[b]
    df = df[i]
    return df


def local_html_to_pdf(html, pdf):

    # From https://stackoverflow.com/questions/63382399/how-to-convert-a-local-html-file-to-pdf-using-pyqt5
    # Does not work for workday websites, does not ignore or accept cookies whenever a msg appears
    # To get rid of the cookies thing, we could use the saved html from pywebcopy and covert that to pdf

    app = QtWidgets.QApplication(sys.argv)
    page = QtWebEngineWidgets.QWebEnginePage()

    def handle_print_finished(filename, status):
        print("finished", filename, status)
        QtWidgets.QApplication.quit()

    def handle_load_finished(status):
        if status:
            page.printToPdf(pdf)
        else:
            print("Failed")
            QtWidgets.QApplication.quit()

    page.pdfPrintingFinished.connect(handle_print_finished)
    page.loadFinished.connect(handle_load_finished)
    page.load(QtCore.QUrl.fromLocalFile(html))
    app.exec_()

