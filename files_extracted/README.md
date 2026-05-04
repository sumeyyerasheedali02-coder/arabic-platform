# منصة العربية بين يديك — Arabic Learning Platform

## هيكل المشروع

```
arabic_platform/
├── main.py              ← تطبيق FastAPI الرئيسي (جميع الـ API routes)
├── database.py          ← نماذج قاعدة البيانات SQLAlchemy
├── auth.py              ← نظام المصادقة JWT
├── schemas.py           ← نماذج Pydantic للبيانات
├── srs.py               ← خوارزمية SM-2 للحفظ الذكي
├── seed_database.py     ← تعبئة قاعدة البيانات بالمحتوى
├── requirements.txt     ← المكتبات المطلوبة
├── .env                 ← متغيرات البيئة (لا ترفعه على GitHub)
└── data/
    └── unit_1.py        ← بيانات الوحدة الأولى من الكتاب
```

---

## إعداد البيئة (خطوة بخطوة)

### 1. تثبيت Python 3.11+
```bash
python --version   # تأكد أنها 3.11 أو أحدث
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
عدّل ملف `.env` وضع مفتاح Anthropic API الخاص بك:
```env
SECRET_KEY=اكتب-مفتاحاً-عشوائياً-طويلاً-هنا
ANTHROPIC_API_KEY=sk-ant-...
```

احصل على مفتاح Anthropic من: https://console.anthropic.com

### 5. تعبئة قاعدة البيانات
```bash
python seed_database.py
```
هذا ينشئ `arabic_platform.db` ويملأها بمحتوى الوحدة الأولى.

### 6. تشغيل الخادم
```bash
python main.py
# أو
uvicorn main:app --reload --port 8000
```

### 7. اختبار الـ API
افتح المتصفح على:
- **الوثائق التفاعلية:** http://localhost:8000/docs
- **الوثائق البديلة:** http://localhost:8000/redoc

---

## نقاط الـ API الرئيسية

### المصادقة
| Method | Endpoint              | الوظيفة              |
|--------|-----------------------|----------------------|
| POST   | /api/auth/register    | تسجيل طالب جديد     |
| POST   | /api/auth/login       | تسجيل الدخول         |

### المحتوى
| Method | Endpoint                          | الوظيفة              |
|--------|-----------------------------------|----------------------|
| GET    | /api/units                        | جميع الوحدات         |
| GET    | /api/units/{id}/lessons           | دروس الوحدة          |
| GET    | /api/units/{id}/vocabulary        | مفردات الوحدة        |
| GET    | /api/lessons/{id}/dialogues       | حوارات الدرس         |
| GET    | /api/units/{id}/exercises         | تمارين الوحدة        |

### التفاعل
| Method | Endpoint                          | الوظيفة              |
|--------|-----------------------------------|----------------------|
| POST   | /api/exercises/submit             | إرسال إجابة تمرين   |
| POST   | /api/chat                         | محادثة مع الذكاء AI  |
| GET    | /api/me/progress                  | تقدم الطالب          |
| GET    | /api/me/srs/due                   | بطاقات SRS للمراجعة  |
| POST   | /api/me/srs/review                | تسجيل مراجعة بطاقة  |

### لوحة الأستاذ
| Method | Endpoint                          | الوظيفة              |
|--------|-----------------------------------|----------------------|
| GET    | /api/teacher/students             | جميع الطلاب وتقدمهم |
| GET    | /api/teacher/units/stats          | إحصائيات الوحدات    |

---

## اختبار سريع بـ curl

```bash
# تسجيل طالب
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"أحمد يلدز","email":"ahmed@example.com","password":"123456"}'

# الحصول على الوحدات
curl http://localhost:8000/api/units

# الحصول على مفردات الوحدة الأولى
curl http://localhost:8000/api/units/1/vocabulary
```

---

## الخطوة التالية: الواجهة الأمامية

بعد تشغيل الخادم، الخطوة التالية هي بناء الواجهة بـ React.js.
مجلد الواجهة سيكون: `arabic_platform_frontend/`

---

## إضافة وحدات جديدة من الكتاب

1. أنشئ ملف `data/unit_2.py` بنفس هيكل `unit_1.py`
2. أضف الوحدة في `seed_database.py`
3. شغّل السكريبت مجدداً

---

## التقنيات المستخدمة

- **Backend:** FastAPI + SQLAlchemy + SQLite (أو PostgreSQL في الإنتاج)
- **Auth:** JWT (python-jose) + bcrypt (passlib)
- **AI:** Anthropic Claude API
- **SRS:** خوارزمية SM-2
- **Frontend (قادم):** React.js + Tailwind CSS
