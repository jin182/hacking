import os
import re
import json
import requests
from datetime import datetime

# 로그 파일 경로 설정
LOG_FILE_PATH = '/var/log/syslog'

# 의심스러운 IP 패턴 정의
SUSPICIOUS_IP_PATTERNS = [
    r'192\.168\.1\.[0-9]+',  # 내부망 IP 예시
    r'10\.0\.[0-9]+\.[0-9]+'  # 또 다른 내부망 IP 예시
]

# 의심스러운 행동 패턴 정의
SUSPICIOUS_BEHAVIOR_PATTERNS = [
    r'Failed password for',
    r'authentication failure',
    r'connection refused'
]

# 알림을 위한 Webhook URL 설정 (예: Slack, Discord 등)
WEBHOOK_URL = 'https://example.com/webhook'

# 로그 분석 함수 정의
def analyze_logs():
    suspicious_activities = []
    
    # 로그 파일 읽기
    with open(LOG_FILE_PATH, 'r') as log_file:
        for line in log_file:
            # 의심스러운 IP 패턴 탐지
            for ip_pattern in SUSPICIOUS_IP_PATTERNS:
                if re.search(ip_pattern, line):
                    suspicious_activities.append({'type': 'suspicious_ip', 'log': line.strip()})
                    break
            
            # 의심스러운 행동 패턴 탐지
            for behavior_pattern in SUSPICIOUS_BEHAVIOR_PATTERNS:
                if re.search(behavior_pattern, line):
                    suspicious_activities.append({'type': 'suspicious_behavior', 'log': line.strip()})
                    break
    
    return suspicious_activities

# 대응 조치 함수 정의
def respond_to_incident(activities):
    for activity in activities:
        if activity['type'] == 'suspicious_ip':
            # 의심스러운 IP에 대해 차단 명령어 실행 (예: iptables 사용)
            ip = re.findall(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', activity['log'])
            if ip:
                os.system(f'sudo iptables -A INPUT -s {ip[0]} -j DROP')
                print(f"Blocked suspicious IP: {ip[0]}")
        
        # 의심스러운 행동에 대한 알림 전송
        send_alert(activity)

# 알림 전송 함수 정의
def send_alert(activity):
    headers = {'Content-Type': 'application/json'}
    data = {
        'text': f"Suspicious activity detected: {activity['log']}",
        'timestamp': datetime.now().isoformat()
    }
    response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Alert sent successfully.")
    else:
        print(f"Failed to send alert. Status Code: {response.status_code}")

# 메인 함수
def main():
    # 로그 분석
    activities = analyze_logs()
    
    # 침해사고 대응
    if activities:
        respond_to_incident(activities)
    else:
        print("No suspicious activities detected.")

if __name__ == "__main__":
    main()
