from scapy.all import rdpcap

def analyze_pcap(file_path):
    packets = rdpcap(file_path)
    for packet in packets:
        if packet.haslayer("IP"):
            src_ip = packet["IP"].src
            dst_ip = packet["IP"].dst
            print(f"Source IP: {src_ip} -> Destination IP: {dst_ip}")

# 예시 파일로 pcap을 불러와서 분석
analyze_pcap("example.pcap")
