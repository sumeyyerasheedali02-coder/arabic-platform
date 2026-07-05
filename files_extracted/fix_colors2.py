import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = r"C:\Users\SD\Desktop\arabic_platform\frontend\src\pages\LoginRegister.jsx"
content = open(PATH, encoding="utf-8").read()
fixes = 0

# قائمة الاستبدالات: (القديم، الجديد، الوصف)
REPLACEMENTS = [
    # خلفية الحقول: من داكن إلى فاتح
    ("background: '#1e2231'", "background: '#F8FAFC'", "خلفية الحقول"),
    # حدود الحقول: من داكن إلى رمادي واضح
    ("border: '1px solid #2a3045'", "border: '1.5px solid #CBD5E1'", "حدود الحقول"),
    # نص الحقول: من أبيض إلى داكن
    ("color: '#fff'", "color: '#1E293B'", "نص الحقول"),
    # التسميات: من رمادي باهت إلى داكن واضح
    ("color: '#94a3b8'", "color: '#374151'", "التسميات"),
    # النصوص الثانوية
    ("color: '#64748b'", "color: '#4A5568'", "نصوص ثانوية"),
    ("color: '#475569'", "color: '#6B7280'", "نصوص مساعدة"),
    # خلفية لوحة النموذج: من داكن إلى فاتح
    ("bg-dark-base", "bg-white", "خلفية اللوحة"),
    ("bg-dark-surface", "bg-white", "خلفية البطاقة"),
    # حدود البطاقة
    ("border-dark-border", "border-gray-200", "حدود البطاقة"),
    # العنوان من أبيض إلى كحلي
    ("text-white mt-3", "text-gray-800 mt-3", "عنوان الجوال"),
    ("text-white mb-6", "text-gray-800 mb-6", "عنوان النموذج"),
    # حدود الفوكس
    ("borderColor = '#4f6ef7'", "borderColor = '#3B82F6'", "لون الفوكس"),
    ("borderColor = '#2a3045'", "borderColor = '#CBD5E1'", "حدود بعد الفوكس"),
    # خلفية الخطأ
    ("background: 'rgba(239,68,68,.1)'", "background: '#FEF2F2'", "خلفية الخطأ"),
    ("border: '1px solid rgba(239,68,68,.3)'", "border: '1px solid #FECACA'", "حدود الخطأ"),
    ("color: '#f87171'", "color: '#DC2626'", "نص الخطأ"),
    # رابط الضيف
    ("textDecorationColor: 'rgba(100,116,139,.4)'", "textDecorationColor: '#93C5FD'", "خط الضيف"),
    # فاصل الضيف
    ("borderTop: '1px solid rgba(255,255,255,.07)'", "borderTop: '1px solid #E5E7EB'", "فاصل الضيف"),
    # خلفية حالة الموجود
    ("borderColor: emailState === 'existing' ? '#22c55e44'", "borderColor: emailState === 'existing' ? '#86EFAC'", "حدود موجود"),
    ("borderColor: emailState === 'new'      ? '#3b82f644'", "borderColor: emailState === 'new'      ? '#93C5FD'", "حدود جديد"),
]

for old, new, desc in REPLACEMENTS:
    count = content.count(old)
    if count > 0:
        content = content.replace(old, new)
        fixes += count
        print(f"  ✓ {desc}: {count}x")

if fixes > 0:
    open(PATH, "w", encoding="utf-8").write(content)
    print(f"\n✅ تم تطبيق {fixes} تحسين")
else:
    print("⚠️ لم يُعثر على أي من الألوان المتوقعة")