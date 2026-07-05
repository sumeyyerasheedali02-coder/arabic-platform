import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import urllib.request, json

BASE = "https://adaptable-solace-production-e226.up.railway.app/api"

def fetch(url):
    try:
        r = urllib.request.urlopen(url, timeout=10)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:200]
    except Exception as e:
        return "ERR", str(e)[:200]

# اختبار 1: قائمة الوحدات
status, data = fetch(f"{BASE}/units")
print(f"GET /units : {status}")
if isinstance(data, list):
    print(f"  عدد الوحدات: {len(data)}")
    u1 = data[0]
    print(f"  أول وحدة: id={u1.get('id')}, رقم={u1.get('unit_number')}")
    
    # اختبار 2: دروس الوحدة الأولى
    status2, lessons = fetch(f"{BASE}/units/{u1['id']}/lessons")
    print(f"\nGET /units/{u1['id']}/lessons : {status2}")
    if isinstance(lessons, list):
        for L in lessons:
            print(f"  درس: type={L.get('lesson_type')}, id={L.get('id')}")
            # اختبار 3: حوارات كل درس
            status3, dials = fetch(f"{BASE}/lessons/{L['id']}/dialogues")
            print(f"    GET /lessons/{L['id']}/dialogues : {status3}")
            if isinstance(dials, list):
                print(f"      عدد الحوارات: {len(dials)}")