import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform")

content = "import axios from 'axios'\n\nconst API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8003'\n\nconst api = axios.create({\n  baseURL: `${API_URL}/api`,\n})\n\napi.interceptors.request.use((config) => {\n  const token = localStorage.getItem('token')\n  if (token) {\n    config.headers.Authorization = `Bearer ${token}`\n  }\n  return config\n})\n\nexport default api\n"

open(r"frontend\src\api\client.js", "w", encoding="utf-8").write(content)
print("client.js FIXED")

m = open(r"files_extracted\main.py", encoding="utf-8").read()
m = m.replace('allow_origins=["*"],   # \u0641\u064a \u0627\u0644\u0625\u0646\u062a\u0627\u062c: \u0636\u0639 \u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u0648\u0627\u062c\u0647\u0629 \u0627\u0644\u0623\u0645\u0627\u0645\u064a\u0629 \u0641\u0642\u0637', 'allow_origins=["https://arabic-platform-flame.vercel.app","http://localhost:5173","http://localhost:8003"],')
open(r"files_extracted\main.py", "w", encoding="utf-8").write(m)
print("main.py FIXED")

os.system("git add files_extracted/main.py frontend/src/api/client.js")
os.system('git commit -m "fix: baseURL and CORS"')
os.system("git push")
print("DONE!")
