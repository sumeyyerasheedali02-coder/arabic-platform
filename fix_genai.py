import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\files_extracted")

m = open("main.py", encoding="utf-8").read()

old = "from google import genai\n_genai_client = genai.Client(api_key=os.getenv(\"GOOGLE_API_KEY\"))"
new = "from google import genai\n_genai_client = None\ndef get_genai_client():\n    global _genai_client\n    if _genai_client is None:\n        _genai_client = genai.Client(api_key=os.getenv(\"GOOGLE_API_KEY\"))\n    return _genai_client"

m = m.replace(old, new)
m = m.replace("response = await _genai_client.aio.models.generate_content(", "response = await get_genai_client().aio.models.generate_content(")

open("main.py", "w", encoding="utf-8").write(m)

req = open("requirements.txt", encoding="utf-8").read()
if "email-validator" not in req:
    open("requirements.txt", "a").write("\nemail-validator==2.1.0\n")

print("Done!")
