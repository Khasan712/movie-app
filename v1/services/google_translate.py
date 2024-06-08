import requests
from django.conf import settings


def google_translate_text(target, message: str):
    try:

        url = settings.RAPID_API_GOOGLE_TRANSLATE

        payload = {
            "q": str(message),
            "source": "uz",
            "target": target,
            "format": "text"
        }
        headers = {
            "x-rapidapi-key": settings.X_RAPIDAPI_KEY,
            "x-rapidapi-host": settings.X_RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            data = res.json()
            message = data['data']['translations'][0]['translatedText']
    except Exception as ex:
        print(str(ex))

    return message
