import ssl
import aiohttp
import asyncio
import json

    
def answer_rollcall_number(session, rollcall_id):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/answer_number_rollcall"

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
    
    data = {
            "deviceId": "7eba2081f77e5527",
            "numberCode": getNumber(session, rollcall_id)
    }
    print(f"Attempted to answer rollcall {rollcall_id} with number code {data['numberCode']}")
    session.put(url, headers=headers, data=json.dumps(data))

    if data['numberCode'] is None:
        print("No number code found for this rollcall.")
        return None
    else:
        print(f"Number code for rollcall {rollcall_id} is {data['numberCode']}")
        return data['numberCode']




    

def getNumber(session, rollcall_id):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/student_rollcalls"
    res = session.get(url)
    
    return res.json().get("number_code", None)
    pass
