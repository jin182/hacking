from pwn import *
import dpkt
import datetime
import urllib.parse

def analyze_packets(pcap):
    flag = ['X'] * 39
    post_sent = False
    payload = ''
    request_time = 0
    
    for timestamp, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        if not isinstance(eth.data, dpkt.ip.IP):
            continue
        ip = eth.data
        if not isinstance(ip.data, dpkt.tcp.TCP):
            continue
        tcp = ip.data
        
        if not post_sent and tcp.dport == 80 and len(tcp.data) > 0:
            time = datetime.datetime.utcfromtimestamp(timestamp)
            print(f'Timestamp: {time} ({timestamp})')
            request_time = timestamp
            
            try:
                http = dpkt.http.Request(tcp.data)
                payload = urllib.parse.unquote(http.uri)
                print(f'-- request --\n {http.method} {payload}\n')
                if http.method == 'POST':
                    post_sent = True
            except dpkt.dpkt.UnpackError:
                continue
                
        elif post_sent and tcp.sport == 80 and len(tcp.data) > 0:
            response_time = timestamp
            
            try:
                http = dpkt.http.Response(tcp.data)
                print(f'-- response --\n{http.status}')
                
                if response_time - request_time >= 2.8:
                    payload = payload[payload.find('LIMIT 1),') + 9:]
                    idx = int(payload[:payload.find(',')]) - 1
                    ch = chr(int(payload[payload.find('))=') + 3:payload.find(', SLEEP(3)')]))
                    flag[idx] = ch
                    print(f'\n\nFound!!\n\n flag[{idx}] : {ch}\n\ncurrent flag : {"".join(flag)}')
                    sleep(0.1)
            except dpkt.dpkt.UnpackError:
                continue
            
            post_sent = False
    
    return ''.join(flag)

def main():
    pcap_file = '/Users/USER/Downloads/dump.pcap'
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        print('flag : ' + analyze_packets(pcap))

if __name__ == '__main__':
    main()​
