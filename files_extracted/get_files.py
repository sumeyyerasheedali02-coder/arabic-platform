import urllib.request
base = "https://raw.githubusercontent.com/sumeyyerasheedali02-coder/arabic-platform/34dc4c8/"
files = [
    ("files_extracted/exercises_data.py", "exercises_data.py"),
    ("files_extracted/seed_database.py", "seed_database.py"),
]
for url_path, local in files:
    url = base + url_path
    try:
        urllib.request.urlretrieve(url, local)
        print(f"Downloaded: {local}")
    except Exception as e:
        print(f"Failed {local}: {e}")
