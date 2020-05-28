'''
    Changes:
        - The isMessageTable function has a case where it doesn't reach 
        a return statement, as originally written. In a lot of cases
        this won't be a huge deal since the default return for python
        functions is None, which will not register as True in the
        situation presented in the example. However, as far as best
        coding practices are concerned if you've got a function that's
        supposed to return a certain type of value, make sure it does so.
        - The help parameter when adding the option was originally
        'specify skype profile path'.
'''
import os
import sqlite3
import argparse


def isMessageTable(iphoneDB):
    try:
        conn = sqlite3.connect(iphoneDB)
        c = conn.cursor()
        c.execute(
            "SELECT tbl_name FROM sqlite_master \
            WHERE type=='table';")

        for row in c:
            if 'message' in str(row):
                return True
    except:
        return False

    return False


def printMessage(msgDB):
    try:
        conn = sqlite3.connect(msgDB)
        c = conn.cursor()
        c.execute(
            "SELECT datetime(date,'unixepoch'),\
            address, text FROM message WHERE address>0;")

        for row in c:
            date = str(row[0])
            addr = str(row[1])
            text = row[2]

            print(
                "\n[+] Date: " + date + ", Addr: " +\
                addr + " Message: " + text)
        
    except:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", dest="pathName", type=str,
        required=True, help="specify iphone database path")
    options = parser.parse_args()

    pathName = options.pathName
    dirList = os.listdir(pathName)

    for fileName in dirList:
        iphoneDB = os.path.join(pathName, fileName)

        if isMessageTable(iphoneDB):
            try:
                print("\n[*] --- Found Messages ---")
                printMessage(iphoneDB)
            except:
                pass


if __name__ == '__main__':
    main()
