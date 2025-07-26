import requests
import json

API_URL = "https://core-api.kablowebtv.com/api/channels"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://tvheryerde.com",
    "Origin": "https://tvheryerde.com",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpY2giOiIwIiwiaWRtIjoiMCIsImlhIjoiOjpmZmZmOjEwLjAuMC4yMDYiLCJhcHYiOiIxLjAuMCIsImFibiI6IjEwMDAiLCJuYmYiOjE3NDUxNTI4MjUsImV4cCI6MTc0NTE1Mjg4NSwiaWF0IjoxNzQ1MTUyODI1fQ.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E"
}

def fetch_token():
    resp = requests.get(API_URL, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception(f"API error: {resp.status_code}")

    data = resp.json()
    try:
        # İlk çalışan kanalın stream URL'sinden token'ı al
        channels = data["Data"]["AllChannels"]
        for ch in channels:
            url = ch["StreamData"]["HlsStreamUrl"]
            if "wmsAuthSign=" in url:
                token = url.split("wmsAuthSign=")[1]
                with open("token.txt", "w") as f:
                    f.write(token)
                print("Token başarıyla yazıldı.")
                return
        raise Exception("Token bulunamadı.")
    except Exception as e:
        raise Exception(f"Veri ayrıştırma hatası: {e}")

if __name__ == "__main__":
    fetch_token()
