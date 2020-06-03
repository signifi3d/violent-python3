'''
    Changes:
        - dpkt requires reading files in binary mode so mode='rb' was
        added to the open function to avoid errors.
'''
import dpkt
import socket


def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print("[+] Src: " + src + " __> Dst: " + dst)
        except:
            pass


def main():
    f = open('geotest.pcap', mode='rb')
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)


if __name__ == '__main__':
    main()
