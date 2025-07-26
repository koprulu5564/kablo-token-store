import requests
from urllib.parse import urlparse, parse_qs

API_URL = "https://core-api.kablowebtv.com/api/channels"
TOKEN_FILE = "token.txt"
HEADERS = {
    "User-Agent": "...",        # senin verdiğin tam değer
    "Referer": "...",
    "Origin": "...",
    "Authorization": "Bearer eyJh...tam JWT burada"
}

resp = requests.get(API_URL, headers=HEADERS, timeout=30)
resp.raise_for_status()
data = resp.json()
channels = data.get("Data", {}).get("AllChannels", [])
if not channels:
    raise Exception("Kanal bulunamadı")
hls = channels[0]["StreamData"]["HlsStreamUrl"]
pt = parse_qs(urlparse(hls).query).get("wmsAuthSign")
if not pt:
    raise Exception("Token param bulunamadı")
token = pt[0]
with open(TOKEN_FILE, "w") as f:
    f.write(token)
print("Token alındı:", token)
