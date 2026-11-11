import json
try:
    from api.utils import generate_device_id
except ImportError:
    import secrets
    def generate_device_id() -> str:
        return secrets.token_hex(8)

def answer_rollcall_Radar(session, rollcall_id, device_id=None):
    url = f"https://iclass.tku.edu.tw/api/rollcall/{rollcall_id}/answer?api_version=1.1.2"

    headers = {
        "sec-ch-ua-platform": "\"Android\"",
        "accept-language": "zh-Hant",
        "sec-ch-ua": "\"Android WebView\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
        "sec-ch-ua-mobile": "?1",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": ("Mozilla/5.0 (Linux; Android 14; SM-A146P Build/UP1A.231005.007; wv) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/135.0.7049.111 "
                       "Mobile Safari/537.36 TronClass/googleplay"),
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "http://localhost",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "http://localhost/"
    }

    if not device_id:
        device_id = generate_device_id()

    payload = {
        "deviceId": device_id,
        "latitude": 25.174269373936202,
        "longitude": 121.45422774303604,
        "speed": None,
        "accuracy": 34.400001525878906,
        "altitude": 77.69999694824219,
        "altitudeAccuracy": None,
        "heading": None
    }

    print(f"Attempted to answer radar rollcall {rollcall_id} with deviceId: {device_id}")
    response = session.put(url, headers=headers, data=json.dumps(payload))
    return response
