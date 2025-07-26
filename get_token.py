import requests
from urllib.parse import urlparse, parse_qs

API_URL = "https://core-api.kablowebtv.com/api/channels"
TOKEN_FILE = "stream_token.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://tvheryerde.com",
    "Origin": "https://tvheryerde.com",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpY2giOiIwIiwiaWRtIjoiMCIsImlhIjoiOjpmZmZmOjEwLjAuMC4yMDYiLCJhcHYiOiIxLjAuMCIsImFibiI6IjEwMDAiLCJuYmYiOjE3NDUxNTI4MjUsImV4cCI6MTc0NTE1Mjg4NSwiaWF0IjoxNzQ1MTUyODI1fQ.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E"
}

def fetch_token():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    
    try:
        data = response.json()
    except Exception:
        raise Exception("JSON parse hatası")

    channels = data.get("Data", {}).get("AllChannels", [])
    if not channels:
        raise Exception("Kanal listesi boş")

    # İlk kanaldan token çekiyoruz
    stream_url = channels[0].get("StreamData", {}).get("HlsStreamUrl")
    if not stream_url:
        raise Exception("Stream URL bulunamadı")

    parsed = urlparse(stream_url)
    qs = parse_qs(parsed.query)
    token = qs.get("wmsAuthSign", [None])[0]
    if not token:
        raise Exception("Token bulunamadı")

    # Dosyaya yaz
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    print("Token başarıyla güncellendi.")

if __name__ == "__main__":
    fetch_token()
