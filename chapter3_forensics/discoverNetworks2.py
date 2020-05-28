'''
    Changes:
        - Originally the author had mixed up the help statements for
        the username and password arguments in the add_option calls.
        Just sorted those back out.
        - Made use of urllib.parse.urlparse instead of deprecated urlparse
'''
import os
import argparse
import mechanize
import urllib
import re
from urllib.parse import urlparse
from _winreg import *


def val2addr(val):
    addr = ''
    for ch in val:
        addr += '%02x'% ord(ch)
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr


def wiglePrint(username, password, netid):
    browser = mechanize.Browser()
    browser.open('http://wigle.net')
    reqData = urllib.urlencode(
        {'credential_0': username,
        'credential_1': password})
    browser.open('https://wigle.net//gps/gps/main/login', reqData)
    params = {}
    params['netid'] = netid
    reqParams = urllib.urlencode(params)
    respURL = 'http://wigle.net/gps/gps/main/confirmquery/'
    resp = browser.open(respURL, reqParams).read()
    mapLat = 'N/A'
    mapLon = 'N/A'
    rLat = re.findall(r'maplat=.*\&', resp)
    if rLat:
        mapLat = rLat[0].split('&')[0].split('=')[1]
    rLon = re.findall(r'maplon=.*\&', resp)
    if rLon:
        mapLon = rLon[0].split
    print('[-] Lat: ' + mapLat + ', Lon: ' + mapLon)


def printNets():
    net = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" +\
        "\\NetworkList\\Signatures\\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print('\n[*] Networks You have Joined.')

    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            print('[+] ' + netName + ' ' + macAddr)
            CloseKey(netKey)
        except:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', dest='username', type=str,
        required=True, help='specify wigle username')
    parser.add_argument(
        '-p', dest='password', type=str,
        required=True, help='specify wigle password')
    options = parser.parse_args()

    username = options.username
    password = options.password

    printNets(username, password)


if __name__ == '__main__':
    main()
