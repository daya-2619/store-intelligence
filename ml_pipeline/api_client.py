import requests

from config import API_URL


def send_event(event):

    try:

        response = requests.post(
            API_URL,
            json=[event],
            timeout=10
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        return response.status_code

    except Exception as e:

        print("API Error:", e)

        return None