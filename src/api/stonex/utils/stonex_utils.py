import requests

def send_request(method: str, url: str, path: str, json: dict=None, params: dict=None):
    url = "https://" + url + path
    response = requests.request(
        method=method,
        url=url,
        params=params,
        json=json,
        timeout=120
    )
    response_code = response.status_code
    
    if response_code == 200:
        return response_code, response.json()
    else:
        return response_code, None
    
