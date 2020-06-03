'''
    Changes:
        - Fixed indentation error of except: statement in plotIPs function
'''
import dpkt
import socket
import geoip2.database
import argparse


gi = geoip2.database.Reader("/opt/GeoIP/GeoLite2-City.mmdb")


def retKML(ip):
    rec = gi.city(ip)

    try:
        longitude = rec.location.longitude
        latitude = rec.location.latitude

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
