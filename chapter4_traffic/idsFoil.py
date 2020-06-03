import argparse
from scapy.all import *
from random import randint

def ddosTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) / ICMP(type=8, id=678) / Raw(load='1234')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / ICMP(type=0) / Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / UDP(dport=31335) / Raw(load='PONG')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / ICMP(type=0, id=456)
    send(pkt, iface=iface, count=count)


def exploitTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) /\
          UDP(dport=518) /\
          Raw(load='\x01\x03\x00\x00\x00\x00\x00\x01\x00\x01\x01\xE8')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst)/\
          UDP(dport=635) /\
          Raw(load='^\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F')
    send(pkt, iface=iface, count=count)


def scanTest(src, dst, iface, count):
    pkt = IP(src=src, dst=dst) /\
         UDP(dport=7) /\
         Raw(load='cybercop')
    send(pkt)
    pkt = IP(src=src, dst=dst) /\
          UDP(dport=10080) /\
          Raw(load='Amanda')
    send(pkt, iface=iface, count=count)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', dest='iface', type=str,
        default='eth0', help='specify network interface')
    parser.add_argument(
        '-s', dest='src', type=str,
        default='.'.join([str(randint(1,254)) for x in range(4)]),
        help='specify source address')
    parser.add_argument(
        '-t', dest='tgt', type=str,
        required=True, help='specify target address')
    parser.add_argument(
        '-c', dest='count', type=int,
        default=1, help='specify packet count')
    options = parser.parse_args()

    iface = options.iface
    src = options.src
    dst = options.tgt
    count = options.count

    ddosTest(src, dst, iface, count)
    exploitTest(src, dst, iface, count)
    scanTest(src, dst, iface, count)


if __name__ == '__main__':
    main()
