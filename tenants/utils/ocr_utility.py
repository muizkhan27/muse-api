import io

import environ
import requests

env = environ.Env(
  DEBUG=(bool, False)
)
environ.Env.read_env()


def get_json_from_ocr(file):
    temp_file = io.BytesIO(file.read()).getvalue()
    url = env('OCR_API_URL')
    params = {'access_token': env('OCR_API_KEY')}
    payload = {'type': 'taxform.us', 'lang': 'eng', 'retain': 'true'}
    files = [('', (file.name, temp_file))]
    response = requests.request('POST', url, params=params, headers={}, data=payload, files=files)
    return response.json()
