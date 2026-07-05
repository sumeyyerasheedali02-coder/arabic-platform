import urllib.request, json
import urllib.error

try:
    r = urllib.request.urlopen("https://adaptable-solace-production-e226.up.railway.app/api/lessons/2233/dialogues", timeout=10)
    print("OK:", r.read().decode()[:500])
except urllib.error.HTTPError as e:
    print(f"حالة: {e.code}")
    print("المحتوى:", e.read().decode()[:500])