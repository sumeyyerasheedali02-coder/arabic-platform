import urllib.request, json, urllib.error

# 1. فحص الصحة العامة
try:
    r = urllib.request.urlopen("https://adaptable-solace-production-e226.up.railway.app/", timeout=15)
    print(f"الصفحة الرئيسية: {r.status} ✅ (الخادم يعمل)")
except Exception as e:
    print(f"الصفحة الرئيسية: خطأ — {e}")

# 2. فحص الوحدات (endpoint يعمل سابقاً)
try:
    r = urllib.request.urlopen("https://adaptable-solace-production-e226.up.railway.app/api/units", timeout=15)
    data = json.loads(r.read().decode())
    print(f"الوحدات: {r.status} ✅ ({len(data)} وحدة)")
except Exception as e:
    print(f"الوحدات: خطأ — {e}")