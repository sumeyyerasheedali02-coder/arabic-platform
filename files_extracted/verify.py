import urllib.request, json, urllib.error, time

url = "https://adaptable-solace-production-e226.up.railway.app/api/lessons/2233/dialogues"
try:
    r = urllib.request.urlopen(url, timeout=15)
    data = json.loads(r.read().decode())
    print(f"✅ الحالة: {r.status}")
    print(f"✅ عدد الحوارات: {len(data)}")
    if data:
        print(f"✅ أول حوار: {data[0].get('title_ar')} ({len(data[0].get('lines', []))} سطر)")
        print("\n🎉 الحوارات تعمل الآن!")
except urllib.error.HTTPError as e:
    print(f"⏳ الحالة: {e.code} — قد تحتاج Railway وقتاً أطول. انتظري دقيقة وأعيدي التشغيل.")
except Exception as e:
    print(f"خطأ: {e}")