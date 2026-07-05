import sys, os, shutil
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = r"C:\Users\SD\Desktop\arabic_platform\frontend"

# 1. نسخ الشعار
src_logo = r"C:\Users\SD\Desktop\lugo\logo.png"
dst_logo = os.path.join(BASE, "src", "assets", "logo.png")
os.makedirs(os.path.dirname(dst_logo), exist_ok=True)
shutil.copy2(src_logo, dst_logo)
print("✓ 1. نُسخ logo.png إلى src/assets/")

# 2. إضافة خطوط Google إلى index.html
html_path = os.path.join(BASE, "index.html")
html = open(html_path, encoding="utf-8").read()
font_link = '<link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;600;700;800&family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
if "Cairo" not in html:
    html = html.replace("</head>", f"    {font_link}\n  </head>")
    open(html_path, "w", encoding="utf-8").write(html)
    print("✓ 2. أُضيفت خطوط Google إلى index.html")
else:
    print("✓ 2. الخطوط موجودة مسبقاً")

# 3. إضافة CSS variables إلى index.css
css_path = os.path.join(BASE, "src", "index.css")
css = open(css_path, encoding="utf-8").read() if os.path.exists(css_path) else ""
NEW_CSS = """
/* ═══ Arabiq Akademi Design Tokens ═══ */
:root {
  --aq-navy: #0F2044;
  --aq-navy-light: #1a3a6e;
  --aq-navy-mid: #2a5298;
  --aq-gold: #C9A84C;
  --aq-gold-light: #D4B96A;
  --aq-ivory: #FAF8F3;
  --aq-card: #FFFFFF;
  --aq-border: #E8E0D0;
  --aq-text: #1a2332;
  --aq-text-muted: #6B7A8D;
  --aq-gradient-hero: linear-gradient(135deg, #0F2044 0%, #1a3a6e 50%, #2a5298 100%);
  --aq-gradient-gold: linear-gradient(135deg, #C9A84C 0%, #D4B96A 100%);
  --aq-gradient-royal: linear-gradient(135deg, #0F2044 0%, #1a3a6e 100%);
  --aq-shadow-elegant: 0 20px 50px -20px rgba(15,32,68,0.35);
  --aq-shadow-gold: 0 10px 30px -10px rgba(201,168,76,0.5);
  --aq-font-arabic: 'Cairo', 'Amiri', sans-serif;
  --aq-font-display: 'Cormorant Garamond', 'Cairo', serif;
  --aq-font-sans: 'Inter', 'Cairo', sans-serif;
}
@keyframes aq-pulse-node {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}
@keyframes aq-float-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
@keyframes aq-fade-in {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes aq-spin {
  to { transform: translateY(-50%) rotate(360deg); }
}
"""
if "--aq-navy" not in css:
    css += NEW_CSS
    open(css_path, "w", encoding="utf-8").write(css)
    print("✓ 3. أُضيفت Design Tokens إلى index.css")
else:
    print("✓ 3. التوكنات موجودة مسبقاً")

print("\n✅ البنية التحتية جاهزة!")