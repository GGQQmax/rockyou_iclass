import time
import hashlib


def to_base36(n):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0: return "0"
    result = ""
    while n > 0:
        n, remainder = divmod(n, 36)
        result = chars[remainder] + result
    return result

def from_base36(s):
    return int(s, 36)

def Getqrcode(course_id, rollcall_id, timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    signature ="" #TODO: Implement signature generation logic based on the observed pattern

    return f"/j?p=0~{to_base36(course_id)}!3~{timestamp}{signature}!4~{to_base36(rollcall_id)}"

def answer_rollcall_qr_code(session, rollcall_id, course_id):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/answer_qr_code_rollcall" #not sure if this is the correct endpoint, please verify
    
    headers = {
        "host": "iclass.tku.edu.tw",
        "sec-ch-ua-platform": "\"Android\"",
        "accept-language": "zh-Hant",
        "sec-ch-ua": "\"Android WebView\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Linux; Android 14; SM-A146P Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.111 Mobile Safari/537.36 TronClass/googleplay",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "http://localhost",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "http://localhost/",
        "accept-encoding": "gzip, deflate, br, zstd",
        "priority": "u=1, i"
    }

    response = session.put(url, headers=headers, data=Getqrcode(course_id, rollcall_id))
    return response

if __name__ == "__main__":
    course_id = 259870
    rollcall_id = 1159470
    print(Getqrcode(course_id, rollcall_id,timestamp=1778655489))