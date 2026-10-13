# Arabiq Akademi — منصة تعلّم العربية

منصة لتعليم اللغة العربية للطلاب الأتراك (كلية الإلهيات، جامعة كارابوك) مبنية على سلسلة «العربية بين يديك»: 48 وحدة، حوارات ومفردات وقواعد، تمارين، مراجعة متباعدة (SM-2)، مساعد محادثة «مرشد»، ولوحة متابعة للأستاذ.

| الجزء | المجلد | التقنيات |
|---|---|---|
| الواجهة | [frontend/](frontend/) | React 19، Vite، React Router (HashRouter)، Axios |
| الخادم | [files_extracted/](files_extracted/) | FastAPI، SQLAlchemy (async)، Pydantic، JWT + bcrypt، Google Gemini |
| قاعدة البيانات | — | SQLite محلياً، PostgreSQL في الإنتاج |

## أين أجد ماذا؟

| أريد أن… | اقرأ |
|---|---|
| أفهم بنية المشروع وأين أعدّل كل ميزة | [PROJECT_MAP.md](PROJECT_MAP.md) |
| أشغّل الخادم، أدير المحتوى والترحيلات والحسابات | [files_extracted/README.md](files_extracted/README.md) |
| أشغّل الواجهة وأبنيها | [frontend/README.md](frontend/README.md) |
| أعدّل المحتوى التعليمي (وحدات، مفردات، تمارين) | [files_extracted/content/README.md](files_extracted/content/README.md) |
| أنشر نسخة جديدة | [DEPLOYMENT.md](DEPLOYMENT.md) |
| أعرف الإجراءات الأمنية المطلوبة مني | [SECURITY.md](SECURITY.md) |
| أعرف مصير السكربتات القديمة | [archive/legacy-scripts/README.md](archive/legacy-scripts/README.md) |

## تشغيل سريع

المتطلبات: Python 3.12 (نفس نسخة الـ Dockerfile) و Node.js 22.

```bash
# 1) الخادم — http://localhost:8000  (الوثائق التفاعلية: /docs)
cd files_extracted
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
copy .env.example .env            # ثم املأ SECRET_KEY (طريقة توليده مكتوبة داخل الملف)
uvicorn main:app --reload --port 8000

# 2) الواجهة — http://localhost:5173
cd frontend
npm ci
npm run dev
```

عند أول تشغيل على قاعدة فارغة يملأ الخادم المحتوى الأساسي تلقائياً (48 وحدة). لا حاجة لأي إعداد في الواجهة أثناء التطوير: طلبات `/api` تُحوَّل إلى `localhost:8000` عبر وسيط Vite.

## الفحوص

```bash
cd files_extracted
ruff check .          # فحص الكود
pytest -q             # 100 اختبار على قاعدة SQLite مؤقتة معزولة

cd frontend
npm run lint
npm test              # اختبارات المنطق الخالص (Node)
npm run build
```

الاختبارات لا تلمس أي قاعدة حقيقية أبداً: تُوجَّه إلى ملف مؤقت قبل استيراد التطبيق، ومزوّد الذكاء الاصطناعي مُستبدَل ببديل وهمي. نفس الفحوص تعمل تلقائياً على GitHub عند كل push (`.github/workflows/ci.yml`).

## قواعد عمل مهمة

- **لا تكتب مفاتيح أو كلمات مرور في أي ملف متتبَّع.** كل الإعدادات من متغيرات البيئة ([files_extracted/.env.example](files_extracted/.env.example)).
- **المحتوى يُعدَّل في ملفات [files_extracted/content/](files_extracted/content/) لا في قاعدة البيانات**، ولا تُكتب له سكربتات مؤقتة.
- **إعادة بناء المحتوى على قاعدة فيها طلاب تمسح نشاطهم.** الأداة ترفض ذلك ما لم تُعطَ تأكيداً صريحاً؛ اقرأ قسم «إدارة المحتوى» قبل استخدامها.
- حساب الأستاذ يُنشأ من الخادم بالأمر `python -m tools.teacher_accounts`، لا من صفحة التسجيل.
