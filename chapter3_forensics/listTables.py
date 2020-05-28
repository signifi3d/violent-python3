import os
import sqlite3


def printTables(iphoneDB):
    try:
        conn = sqlite3.connect(iphoneDB)
        c = conn.cursor()
        c.execute(
            "SELECT tbl_name FROM sqlite_master \
            WHERE type=='table';")

        print("\n[*] Database: " + iphoneDB)
        
        for row in c:
            print("[-] Table: " + str(row))
    
    except:
        pass
    
    conn.close()


dirList = os.lsitdir(os.getcwd())

for fileName in dirList:
    printTables(fileName)
