import requests
from api.auth_module import Authenticator
from api.getrollcall import wait_for_rollcall
from sendRadar import answer_rollcall_Radar
from sendNum import answer_rollcall_number
from sendQRcode import answer_rollcall_qr_code

def main(stop_event=None):
    if stop_event and stop_event.is_set():
        return {"cancelled": True}

    print("🔐 Logging in...")
    auth = Authenticator()
    session = auth.perform_auth()

    if stop_event and stop_event.is_set():
        return {"cancelled": True}

    session.headers.update({
        'sec-ch-ua-platform': '"Android"',
        'accept-language': 'zh-Hant',
        'sec-ch-ua': '"Android WebView";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Linux; Android 14; SM-A146P Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.111 Mobile Safari/537.36 TronClass/googleplay',
        'accept': 'application/json, text/plain, */*',
        'origin': 'http://localhost',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'priority': 'u=1, i'
    })

    rollcall = wait_for_rollcall(session, stop_event=stop_event)
    if stop_event and stop_event.is_set():
        return {"cancelled": True}

    if (rollcall==None):
        return None
    
    rollcall_id = rollcall['rollcall_id']
    source = rollcall['source']
    course_id = rollcall['course_id']

    print(f"Returned: rollcall_id={rollcall_id}, source={source}, course_id={course_id}")

    if source == "number":
        data = answer_rollcall_number(session, rollcall_id)
        print(data)
        return {"success": True, "source": source, "rollcall_id": rollcall_id, "data": data}

    elif source == "radar":
        resp = answer_rollcall_Radar(session, rollcall_id)
        print(resp.text)
        return {"success": True, "source": source, "rollcall_id": rollcall_id, "data": resp.text}

    elif source == "qrcode":
        resp = answer_rollcall_qr_code(session, rollcall_id, course_id) # Still testing, not sure if it works
        print(resp)
        return {"success": True, "source": source, "rollcall_id": rollcall_id, "data": str(resp)}

    return {"success": False, "source": source, "rollcall_id": rollcall_id, "error": f"Unknown source: {source}"}

if __name__ == "__main__":
    main()

