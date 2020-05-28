'''
    Changes:
        - urllib2 and urlparse were replaced with calls to respective
        urllib libraries.
'''
import argparse
from urllib.request import urlopen
from urllib.parse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


def findImages(url):
    print('[+] Finding images on ' + url)
    urlContent = urlopen(url).read()
    soup = BeautifulSoup(urlContent)
    imgTags = soup.findAll('img')
    return imgTags


def downloadImage(imgTag):
    try:
        print('[+] Downloading image...')
        imgSrc = imgTag['src']
        imgContent = urlopen(imgSrc).read()
        imgFileName = basename(urlsplit(imgSrc)[2])
        imgFile = open(imgFileName, 'wb')
        imgFile.write(imgContent)
        imgFile.close()
        return imgFileName
    except:
        return ''


def testForExif(imgfileName):
    try:
        exifData = {}
        imgFile = IMage.open(imgFileName)
        info = imgFile._getexif()

        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value

            exifGPS = exifData['GPSinfo']
            if exifGPS:
                print('[*] ' + imgFileName + ' contains GPS MetaData')
    except:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', dest='url', type=str,
        required=True, help='specify url address')
    options = parser.parse_args()

    url = options.url

    imgTags = findImages(url)
    for imgTag in imgTags:
        imgFileName = downloadImage(imgTag)
        testForExif(imgFileName)


if __name__ == '__main__':
    main()
