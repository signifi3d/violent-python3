'''
    Changes:
        - Bounded printGoogle function with try..except statement
'''
import re
import argparse
import os
import sqlite3


def printDownloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute(
        "SELECT name, source, datetime(endTime/100000,\
        'unixepoch') FROM moz_downloads:")
    print("\n[*] --- Files Downloaded --- ")

    for row in c:
        print(
            "[+] File: " + str(row[0]) + " from source: " +\
            str(row[1]) + " at: " + str(row[2]))


def printCookies(cookiesDB):
    try:
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        c.execute("SELECT host, name, value FROM moz_cookies")
        print("\n[*] -- Found Cookies --")

        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print(
                "[+] Host: " + host + ", Cookie: " +\
                name + ", Value: " + value)

    except Exception as e:
        if "encrypted" in str(e):
            print("\n[*] Error reading your cookies database.")
            print("[*] Upgrade your Python-Sqlite3 Library")


def printHistory(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute(
            "SELECT url, datetime(visit_date/100000, \
            'unixepoch') from moz_places, moz_historyvisits \
            WHERE visit_count > 0 and moz_places.id==\
            moz_historyvisits.place_id;")
        print("\n[*] -- Found History --")
        
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print("[+] " + date + " - Visited: " + url)
    except Exception as e:
        if 'encrypted' in str(e):
            print("\n[*] Error reading your places database.")
            print("[*] Upgrade your Python-Sqlite3 Library")
            exit(0)


def printGoogle(placesDB):
    try:
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        c.execute(
            "SELECT url, datetime(visit_date/100000, \
            'unixepoch') from moz_places, moz_historyvisits \
            WHERE visit_count > 0 and moz_places.id==\
            moz_historyvisits.place_id;")
        print("\n[*] -- Found Google --")

        for row in c:
            url = str(row[0])
            date = str(row[1])
    
            if "google" in url.lower():
                r = re.findall(r'q=.*\&', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print("[+] " + date + " - Searched For: " + search)
    except Exception as e:
        print("\n[*] Error reading Google data.")
        print("[*] " + e)
        exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", dest="pathName", type=str,
        required=True, help="specify skype profile path")
    options = parser.parse_args()

    pathName = options.pathName

    if os.path.isdir(pathName) == False:
        print('[!] Path Does Not Exist: ' + pathName)
        exit(0)
    else:
        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        if os.path.isfile(downloadDB):
            printDownloads(downloadDB)
        else:
            print('[!] Downloads Db does not exist: ' + downloadDB)

        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        if os.path.isfile(cookiesDB):
            printCookies(cookiesDB)
        else:
            print('[!] Cookies Db does not exist:' + cookiesDB)

        placesDB = os.path.join(pathName, 'places.sqlite')
        if os.path.isfile(placesDB):
            printHistory(placesDB)
            printGoogle(placesDB)
        else:
            print("[!] PlacesDb does not exist: " + placesDB)


if __name__ == '__main__':
    main()
