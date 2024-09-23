#!/usr/bin/env python3

# 0x00 ~ 0xFF 까지의 16진수 값을 리스트로 생성
hex_list = [(hex(i)[2:].zfill(2).upper()) for i in range(256)]

# 암호화된 파일 읽기
with open('/Users/USER/암호와 해킹/encfile', 'r', encoding='utf-8') as f:
    enc_s = f.read()

# 암호화된 데이터를 두 글자씩 잘라서 리스트로 변환
enc_list = [enc_s[i:i+2] for i in range(0, len(enc_s), 2)]

# 복호화 리스트 생성
dec_list = list(range(len(enc_list)))

# 복호화 과정 (암호화할 때 128을 더했으므로 복호화는 128을 빼는 과정)
for i in range(len(enc_list)):
    hex_b = enc_list[i]
    index = hex_list.index(hex_b)
    dec_list[i] = hex_list[(index - 128) % len(hex_list)]

# 복호화된 데이터 바이너리로 변환
dec_bytes = bytes([int(b, 16) for b in dec_list])

# 복호화된 데이터를 파일로 저장
with open('decfile.png', 'wb') as f:
    f.write(dec_bytes)
