from bs4 import BeautifulSoup
import re
import json
import os
import io
import urllib.request


def printHtml(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    return mystr


def startupCheck(filename,s):
    if os.path.exists(filename) and os.access('.', os.R_OK):
        # checks if file exists
        print("Base de donnée '%s' existe et est lisible, on peut passer à la suite."%filename)
        return True

    else:
        print("Base de données '%s' manquante ou illisible, création de celle-ci..."%filename)
        with io.open(os.path.join('.', filename), 'w') as db_file:
            db_file.write(s)
            return False