from pwn import *
import dpkt
import datetime
import urllib.parse
from collections import defaultdict

def analyze_packets(pcap):
    flag = ['X'] * 39
    request_data = defaultdict(dict)
    
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            continue
        ip = eth.data
        if not isinstance(ip.data, dpkt.tcp.TCP):
            continue
        tcp = ip.data
        
        if tcp.dport == 80 and len(tcp.data) > 0:
            try:
                http = dpkt.http.Request(tcp.data)
                payload = urllib.parse.unquote(http.uri)
                if http.method == 'POST':
                    request_data[tcp.sport]['time'] = timestamp
                    request_data[tcp.sport]['payload'] = payload
            except dpkt.dpkt.UnpackError:
                continue
                
        elif tcp.sport == 80 and len(tcp.data) > 0:
            if tcp.dport not in request_data:
                continue
            
            try:
                http = dpkt.http.Response(tcp.data)
                request_time = request_data[tcp.dport]['time']
                
                if timestamp - request_time >= 2.8:
                    payload = request_data[tcp.dport]['payload']
                    payload = payload[payload.find('LIMIT 1),') + 9:]
                    idx = int(payload[:payload.find(',')]) - 1
                    ch = chr(int(payload[payload.find('))=') + 3:payload.find(', SLEEP(3)')]))
                    flag[idx] = ch
                    print(f'\nFound!! flag[{idx}] : {ch}\nCurrent flag: {"".join(flag)}')
                
                del request_data[tcp.dport]
            except dpkt.dpkt.UnpackError:
                continue
    
    return ''.join(flag)

def main():
    pcap_file = '/Users/USER/Downloads/dump.pcap'
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        print('Flag:', analyze_packets(pcap))

if __name__ == '__main__':
    main()
