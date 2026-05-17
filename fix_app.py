import os
os.chdir(r"C:\Users\SD\Desktop\arabic_platform\frontend\src")
m = open("App.jsx", encoding="utf-8").read()
old = "          <Route path=\"*\"                  element={<Navigate to=\"/\" replace />} />"
new = "          <Route path=\"/chat\"              element={<AppLayout><ArabicChat /></AppLayout>} />\n          <Route path=\"*\"                  element={<Navigate to=\"/\" replace />} />"
m = m.replace(old, new)
open("App.jsx", "w", encoding="utf-8").write(m)
print("Done!")
