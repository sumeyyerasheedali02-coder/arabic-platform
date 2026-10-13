# الخادم (FastAPI)

## البنية

```
files_extracted/
├── main.py                  نقطة الدخول: يجمع الإعدادات ودورة الحياة و CORS والراوترات فقط
├── app/                     كود التشغيل
│   ├── config.py            كل متغيرات البيئة، تُقرأ مرة واحدة
│   ├── database.py          المحرك والجلسات و init_db
│   ├── models.py            نماذج الجداول
│   ├── schemas.py           نماذج الطلبات والاستجابات
│   ├── security.py          كلمات المرور، JWT، التحقق من الهوية والصلاحية
│   ├── migrations.py        تغييرات المخطط على القواعد الموجودة
│   ├── routers/             auth · content · exercises · progress · srs · chat · teacher
│   └── services/            answers (تصحيح) · exercise_categories · srs (SM-2) · ai (Gemini) · reporting
├── content/                 المحتوى التعليمي كبيانات خالصة (انظر content/README.md)
├── tools/                   أدوات سطر الأوامر: seed · migrate · teacher_accounts · content_report
├── tests/                   اختبارات API على قاعدة معزولة
├── seed_database.py         نقطة دخول قديمة آمنة (تستدعي tools.seed)
├── requirements.txt         اعتماديات الإنتاج (نسخ مثبّتة)
├── requirements-dev.txt     + pytest و ruff
└── Dockerfile               صورة الإنتاج (Python 3.12، المنفذ 8080)
```

القاعدة: الراوتر يتعامل مع HTTP فقط، والمنطق القابل لإعادة الاستخدام في `services/`، ولا شيء في `content/` يلمس قاعدة البيانات.

## الإعداد

```bash
python -m venv .venv
.venv\Scripts\activate                 # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```

استخدم Python 3.12. النسخ المثبّتة في `requirements.txt` لا تتوفر لها حزم جاهزة على 3.13 وما بعدها.

### متغيرات البيئة

كلها موثّقة في [.env.example](.env.example) وتُقرأ في [app/config.py](app/config.py).

| المتغير | مطلوب؟ | الوظيفة |
|---|---|---|
| `SECRET_KEY` | نعم في الإنتاج | مفتاح توقيع رموز الدخول. إن غاب استُخدم مفتاح مؤقت عشوائي (يسجّل الجميع خروجاً عند كل إعادة تشغيل) |
| `DATABASE_URL` | نعم في الإنتاج | الافتراضي SQLite محلي. عناوين `postgres://` تُحوَّل تلقائياً إلى asyncpg |
| `GOOGLE_API_KEY` | للمساعد | مفتاح Gemini. بدونه يجيب المساعد «غير مفعّل» |
| `TEACHER_EMAILS` | للوحة الأستاذ | عناوين الأساتذة مفصولة بفواصل |
| `CORS_ORIGINS` | اختياري | المواقع المسموح لها باستدعاء الـ API |
| `GEMINI_MODEL` | اختياري | اسم النموذج |
| `SEED_ON_EMPTY_DB` | اختياري | `true` (الافتراضي): تعبئة المحتوى الأساسي عند الإقلاع إن كانت القاعدة فارغة تماماً |
| `ENVIRONMENT` | اختياري | `production` يمنع الإقلاع دون `SECRET_KEY` حقيقي |
| `ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM` | اختياري | مدة الرمز (7 أيام) وخوارزمية التوقيع |

## واجهات الـ API

الوثائق التفاعلية على `/docs`. كل المسارات تحت `/api`.

| الطريقة | المسار | الصلاحية |
|---|---|---|
| POST | `/auth/register` · `/auth/login` | عام. الدخول بصيغة form (`username`, `password`) لا JSON |
| GET | `/auth/check-email` | عام |
| GET | `/auth/me` | مسجّل — يتحقق من الرمز ويعيد الاسم وصفة الأستاذ |
| GET | `/units` · `/units/{id}` · `/units/{id}/lessons` · `/units/{id}/vocabulary` · `/units/{id}/exercises` | عام |
| GET | `/lessons/{id}` · `/lessons/{id}/dialogues` · `/vocabulary/search?q=` | عام |
| POST | `/exercises/submit` | مسجّل — يصحّح ويحفظ الإجابة |
| GET / POST | `/me/progress` · `/me/progress/update` | مسجّل |
| GET / POST | `/me/srs/due` · `/me/srs/review` · `/me/srs/add-unit/{unit_id}` | مسجّل |
| POST | `/chat` | عام |
| GET | `/teacher/students` · `/teacher/units/stats` | أستاذ |

لا توجد مسارات إدارية عبر HTTP: كل العمليات الإدارية من سطر الأوامر.

## الأدوات (`python -m tools.<name>`)

كلها تعمل على القاعدة المحددة في `DATABASE_URL`. **تأكد من قيمته قبل التشغيل.**

### `tools.seed` — المحتوى

```bash
python -m tools.seed                      # المحتوى الأساسي في قاعدة فارغة؛ لا يفعل شيئاً إن وُجد محتوى
python -m tools.seed --with-supplements   # + مجموعات التمارين الإضافية (المجموع 4056 تمريناً)
python -m tools.seed --supplements-only   # إضافة/إعادة بناء المجموعات الإضافية على محتوى موجود
python -m tools.seed --replace --yes-delete-student-activity
```

- الأمر الأخير **يحذف إجابات كل الطلاب وتقدّمهم وبطاقاتهم** (الحسابات تبقى)، لأنها تشير إلى صفوف المحتوى. لا يعمل بدون علم التأكيد.
- `--supplements-only` يتوقف إن كانت هناك إجابات مسجّلة على التمارين التي سيعيد بناءها؛ أضف `--yes-delete-affected-answers` فقط إن كان فقدانها مقبولاً.
- كل تشغيل معاملة واحدة: إن فشل شيء تبقى القاعدة كما كانت.

التفاصيل ومصادر المحتوى في [content/README.md](content/README.md).

### `tools.content_report` — ماذا في القاعدة؟

```bash
python -m tools.content_report [--units]
```

قراءة فقط (آمن على الإنتاج). يعرض الأعداد حسب النوع والتصنيف ونطاق الأرقام، ويقارنها بما تنتجه `tools.seed`، وينبّه إلى بقايا مثل سؤال التجربة `[تجربة]`.

### `tools.migrate` — مخطط القاعدة

```bash
python -m tools.migrate --status    # ما المطبَّق وما المعلّق
python -m tools.migrate             # إنشاء الجداول الناقصة وتطبيق الترحيلات المعلّقة
```

الخادم يفعل ذلك تلقائياً عند الإقلاع، فالتشغيل اليدوي اختياري. لا يحذف بيانات أبداً.

**لإضافة تغيير على جدول موجود** (فهرس، عمود): عدّله في `app/models.py` **و** أضف ترحيلاً جديداً في آخر قائمة `MIGRATIONS` في [app/migrations.py](app/migrations.py). `create_all` لا يعدّل الجداول الموجودة، فبدون الترحيل لن يصل التغيير إلى الإنتاج. القواعد مكتوبة أعلى ذلك الملف.

### `tools.teacher_accounts` — حسابات الأساتذة

```bash
python -m tools.teacher_accounts list
python -m tools.teacher_accounts create --email teacher@karabuk.edu.tr --name "الاسم"
python -m tools.teacher_accounts set-password --email teacher@karabuk.edu.tr
```

كلمة المرور تُطلب تفاعلياً (أو من متغير بيئة عبر `--password-env`). العناوين المدرجة في `TEACHER_EMAILS` لا يمكن تسجيلها من الواجهة العامة.

## الاختبارات

```bash
pytest -q                                   # SQLite مؤقتة
ruff check .
```

- `tests/_app.py` يوجّه `DATABASE_URL` إلى ملف مؤقت **قبل** استيراد التطبيق، ويتأكد `conftest.py` من ذلك قبل أي اختبار.
- كل اختبار يبدأ بمحتوى صغير ثابت (وحدتان) يُبنى في `conftest.py`.
- مزوّد Gemini لا يُستدعى أبداً: `fake_ai` يستبدله.
- للتشغيل على PostgreSQL أنشئ قاعدة خاصة بالاختبار يحتوي اسمها على `arabiq_test` (الاختبارات تمسح كل جداولها):

```bash
set TEST_DATABASE_URL=postgresql+asyncpg://user@localhost:5432/arabiq_test
pytest -q
```

## ملاحظات توافق

- bcrypt يُستخدم مباشرة لا عبر passlib (passlib 1.7.4 لا يعمل مع bcrypt 4 وما بعده).
- حقل `sub` في JWT نص دائماً (`str(student.id)`)؛ python-jose يشترط ذلك.
- الحوارات تُحمَّل مع سطورها بـ `selectinload`؛ التحميل الكسول غير ممكن في الجلسات غير المتزامنة.
- SQLite لا يفرض المفاتيح الخارجية افتراضياً، و PostgreSQL يفرضها: اختبر ما يحذف صفوفاً على PostgreSQL أيضاً.
