'''
    Note:
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
        - Fixed indentation error of except statement in plotIPs function
'''
import dpkt
import socket
import pygeoip
import argparse


gi = pygeoip.GeoIP("/opt/GeoIP/Geo.dat")


def retKML(ip):
    rec = gi.record_by_name(ip)

    try:
        longitude = rec['longitude']
        latitude = rec['latitude']

        kml = (
                "<Placemark>\n"
                "<name>%s</name>\n"
                "<Point>\n"
                "<coordinates>%6f,%6f</coordinates\n"
                "</Point>\n"
                "</Placemark>\n"
              )%(ip, longitude, latitude)
        
        return kml

    except:
        return ''


def plotIPs(pcap):
    kmlPts = ''

    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            srcKML = retKML(src)
            dst = socket.inet_ntoa(ip.dst)
            dstKML = retKML(dst)
            kmlPts = kmlPts + srcKML + dstKML
        
        except:
            pass
    
    return kmlPts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", dest="pcapFile", type=str,
        required=True, help="specify pcap filename")
    options = parser.parse_args()

    pcapFile = options.pcapFile
    f = open(pcapFile, mode="rb")
    pcap = dpkt.pcap.Reader(f)

    kmlHeader = "<?xml version='1.0' encoding='UTF-8'?>\
                \n<kml xmlns='http://www.opengis.net/kml/2.2'>\n<Document>\n"
    kmlFooter = "</Document>\n</kml>\n"
    kmlDoc = kmlHeader + plotIPs(pcap) + kmlFooter
    print(kmlDoc)


if __name__ == '__main__':
    main()
