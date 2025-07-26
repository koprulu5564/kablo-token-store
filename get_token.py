import requests
import json
import time
import re
import os

TOKEN_FILE = 'stream_token.txt'
API_URL = "https://core-api.kablowebtv.com/api/channels"
STATIC_BEARER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # (kısaltıldı)
HEADERS = {
    "Authorization": f"Bearer {STATIC_BEARER}"
}

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            try:
                data = json.load(f)
                if 'token' in data and 'expiry' in data and time.time() < data['expiry']:
                    return data['token']
            except json.JSONDecodeError:
                pass
    return None

def save_token(token, expiry):
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'token': token, 'expiry': expiry}, f)

def fetch_new_token():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    data = response.json()
    
    try:
        sample_url = data['Data']['AllChannels'][0]['StreamData']['HlsStreamUrl']
        match = re.search(r'wmsAuthSign=([^&]+)', sample_url)
        if match:
            token = match.group(1)
            expiry = time.time() + 6 * 60 * 60  # 6 saat
            save_token(token, expiry)
            print("Yeni token kaydedildi.")
        else:
            raise ValueError("wmsAuthSign bulunamadı.")
    except Exception as e:
        print("Token çekme hatası:", str(e))

def main():
    token = load_token()
    if token is None:
        fetch_new_token()
    else:
        print("Token geçerli, yenileme gerekmedi.")

if __name__ == '__main__':
    main()
