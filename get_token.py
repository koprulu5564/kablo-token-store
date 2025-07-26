import requests
from urllib.parse import urlparse, parse_qs

API_URL = "https://core-api.kablowebtv.com/api/channels"
TOKEN_FILE = "stream_token.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://tvheryerde.com",
    "Origin": "https://tvheryerde.com",
    "Authorization": "Bearer eyJhbGci...tüm oturum JWT burada olacak..."
}

def fetch_token():
    resp = requests.get(API_URL, headers=HEADERS, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"API error: {resp.status_code}")

    data = resp.json()
    channels = data.get("Data", {}).get("AllChannels", [])
    if not channels:
        raise Exception("Kanal listesi boş.")

    hls = channels[0].get("StreamData", {}).get("HlsStreamUrl")
    if not hls:
        raise Exception("Stream URL yok.")

    token = parse_qs(urlparse(hls).query).get("wmsAuthSign", [None])[0]
    if not token:
        raise Exception("Token bulunamadı.")

    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    print("✅ Token güncellendi:", token)

if __name__ == "__main__":
    fetch_token()
