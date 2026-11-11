import time
import requests
import threading

def wait_for_rollcall(session: requests.Session, sec: int = 10, stop_event: threading.Event = None) -> dict:
    """
    Polls the iClass rollcall API until the specified rollcall_id is found or cancelled.
    
    Args:
        session (requests.Session): The session with proper headers set.
        sec (int): Polling interval in seconds.
        stop_event (threading.Event, optional): Event to signal cancellation.
    
    Returns:
        dict: A dictionary containing 'rollcall_id', 'source', and 'course_id', or None if timed out/cancelled.
    """
    url = 'https://iclass.tku.edu.tw/api/radar/rollcalls?api_version=1.1.0'
    failTime = 200
    failTimer = 0
    while True:
        if stop_event and stop_event.is_set():
            print("Rollcall waiting cancelled by user.")
            return None
        if (failTimer >= failTime):
            break
        try:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()
            rollcall_id = ""
            rollcalls = data.get('rollcalls', [])
            for rollcall in rollcalls:
                if rollcall.get('rollcall_id'):
                    course_id = rollcall.get('course_id')
                    print(f"Found rollcall: ID = {rollcall['rollcall_id']}, Source = {rollcall['source']}")
                    return {'rollcall_id': rollcall['rollcall_id'], 'source': rollcall['source'], 'course_id': course_id}
                
            print(f"Rollcall not found yet. Waiting {sec} seconds...")
            if stop_event:
                if stop_event.wait(timeout=sec):
                    print("Rollcall waiting cancelled by user during wait.")
                    return None
            else:
                time.sleep(sec)

        except Exception as e:
            print(f"Error occurred: {e}")
            failTimer = failTimer + 5
            if stop_event:
                if stop_event.wait(timeout=5):
                    return None
            else:
                time.sleep(5)
    return None
