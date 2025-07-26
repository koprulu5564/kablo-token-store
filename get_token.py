import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://tvheryerde.com",
    "Origin": "https://tvheryerde.com",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnYiOiJMSVZFIiwiaXBiIjoiMCIsImNnZCI6IjA5M2Q3MjBhLTUwMmMtNDFlZC1hODBmLTJiODE2OTg0ZmI5NSIsImNzaCI6IlRSS1NUIiwiZGN0IjoiM0VGNzUiLCJkaSI6ImE2OTliODNmLTgyNmItNGQ5OS05MzYxLWM4YTMxMzIxOGQ0NiIsInNnZCI6Ijg5NzQxZmVjLTFkMzMtNGMwMC1hZmNkLTNmZGFmZTBiNmEyZCIsInNwZ2QiOiIxNTJiZDUzOS02MjIwLTQ0MjctYTkxNS1iZjRiZDA2OGQ3ZTgiLCJpY2giOiIwIiwiaWRtIjoiMCIsImlhIjoiOjpmZmZmOjEwLjAuMC4yMDYiLCJhcHYiOiIxLjAuMCIsImFibiI6IjEwMDAiLCJuYmYiOjE3NDUxNTI4MjUsImV4cCI6MTc0NTE1Mjg4NSwiaWF0IjoxNzQ1MTUyODI1fQ.OSlafRMxef4EjHG5t6TqfAQC7y05IiQjwwgf6yMUS9E"
}

def fetch_token():
    url = "https://core-api.kablowebtv.com/api/channels"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json().get("data", [])
            if not data:
                print("Data boş geldi.")
                return

            # İlk içerikten wmsAuthSign token'ı al
            stream_url = data[0].get("streamUrl", "")
            if "wmsAuthSign=" not in stream_url:
                print("wmsAuthSign token bulunamadı.")
                return

            token = stream_url.split("wmsAuthSign=")[-1]
            with open("stream_token.txt", "w") as f:
                f.write(token)
            print("Token başarıyla kaydedildi.")
        except Exception as e:
            print(f"Token ayrıştırılamadı: {e}")
    else:
        print(f"API hatası: {response.status_code}")

if __name__ == "__main__":
    fetch_token()
