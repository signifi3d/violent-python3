'''
    Changes:
        - Encoded password before passing to extractall().
        -- It should be noted that various encodings and error methods will work, but it must be encoded or python 3 isn't happy.
'''
import zipfile
import argparse
from threading import Thread


def extractFile(zFile, password):
    try:
        zFile.extractall(pwd=password.encode('utf-8', 'ignore'))
        print('[+] Found password ' + password)
    except:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', dest='zname', type=str,
        required=True, help='specify zip file')
    parser.add_argument(
        '-d', dest='dname', type=str, 
        required=True, help='specify dictionary file')
    options = parser.parse_args()

    zname = options.zname
    dname = options.dname

    zFile = zipfile.ZipFile(zname)
    passFile = open(dname)

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile, password))
        t.start()


if __name__ == '__main__':
    main()
