'''
    Notes:
        - GeoIP is deprecated now by GeoIP2. While MaxMind stlil provides
        its free City database, it has updated its system and makes use of
        a different file format. I have left the deprecated examples
        making use of pygeoip since it's still operable if you have the
        correct files, but I have also included updated versions of every
        example that makes use of it. Updated examples for any particular
        script can be found in a corresponding [scriptName]-updated.py file.
        You can go to https://dev.maxmind.com/geoip/geoip2/geolite2 to find
        out more about obtaining a newer style database.
    
    Changes:
        - Changed the pcap file open mode to binary to fit with changes made
        to the dpkt library.
'''
import dpkt
import socket
import geoip2.database
import argparse


gi = geoip2.database.Reader("/opt/GeoIP/GeoLite2-City.mmdb")


def retGeoStr(ip):
    try:
        rec = gi.city(ip)
        city = rec.city.name
        country = rec.country.iso_code

        if city != '':
            geoLoc = city + ", " + country
        else:
            geoLoc = country

        return geoLoc

    except Exception as e:
        return 'Unregistered'


def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)

            print("[+] Src: " + src + " --> Dst: " + dst)
            print(
                "[+] Src: " + retGeoStr(src) +\
                " --> Dst: " + retGeoStr(dst))

        except:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", dest="pcapFile", type=str,
        required=True, help="specify pcap filename")
    options = parser.parse_args()

    pcapFile = options.pcapFile
    f = open(pcapFile, mode='rb')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)


if __name__ == '__main__':
    main()
