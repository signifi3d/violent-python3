'''
    Changes:
        - The original uses the file builtin function, which is now
        well deprecated and isn't in the builtin namespace anymore.
        Replaced with call to open.
'''
import PyPDF2
import argparse
from PyPDF2 import PdfFileReader


def printMeta(fileName):
    pdfFile = PdfFileReader(open(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print('[*] PDF MetaData For: ' + str(fileName))
    for metaItem in docInfo:
        print('[+] ' + metaItem + ':' + docInfo[metaItem])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-F', dest='fileName', type=str,
        required=True, help='specify PDF file name')
    options = parser.parse_args()

    fileName = options.fileName

    printMeta(fileName)


if __name__ == '__main__':
    main()
