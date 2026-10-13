# إصلاح صفحة Landing — ملخّص الفروقات الدقيقة

## السياق
المشروع: منصة "Arabiq Akademi" لتعليم العربية — جامعة كارابوك
Frontend: React + Vite على Vercel
Backend: FastAPI على Railway (لا تلمسه)
الملفات: frontend في `C:\Users\SD\Desktop\arabic_platform\frontend\`
ملفات التصميم الأصلي في `C:\Users\SD\Desktop\lugo\` (تحتوي login.tsx + index.tsx + styles.css + logo.png)
التصميم الأصلي المرجعي: https://arabian-steps-forward.lovable.app/

⚠️ قاعدة ثابتة: لا تغيير في جوهر المنصة الداخلي (التمارين، الحوارات، API). فقط التصميم البصري لصفحة Landing.

---

## الفروقات بين النسخة الحالية (المنشورة) والتصميم الأصلي

### 1. الشعار (Logo) — مشكلة حرجة
- **الحالي:** الشعار مكسور تماماً — تظهر أيقونة صورة تالفة (broken image icon) بجانب نص "Arabiq Akademi"
- **الأصلي:** شعار أنيق عبارة عن حرف "ع" عربي بخط ذهبي داخل دائرة منقّطة ذهبية مع زخارف نجمية حولها
- **الإصلاح:** ملف logo.png موجود في `src/assets/logo.png`. المشكلة إما:
  - الملف لم يُرفع إلى git (تحقق بـ `git ls-files | grep -i logo`)
  - حساسية الأحرف في Vercel (لينكس يفرّق بين logo.png و Logo.png)
  - طريقة الاستيراد خاطئة (يجب `import logo from "../assets/logo.png"` ثم `<img src={logo} />`)
  - **الحل الأضمن:** انسخ الشعار إلى `public/logo.png` واستخدمه كـ `<img src="/logo.png" />`

### 2. لون الخلفية — فرق ملحوظ
- **الحالي:** خلفية زرقاء فاتحة نسبياً (تقريباً `#1a3a6e` أو أفتح)
- **الأصلي:** خلفية كحلية عميقة داكنة جداً (تقريباً `#0B1426` إلى `#0F1B3D`)
- **الإصلاح:** خلفية قسم Hero يجب أن تستخدم التدرج الأصلي:
```css
background: linear-gradient(135deg, oklch(0.18 0.05 265) 0%, oklch(0.22 0.07 265) 50%, oklch(0.28 0.08 270) 100%);
/* أو بـ hex: */
background: linear-gradient(135deg, #0B1426 0%, #0F2044 50%, #162952 100%);
```

### 3. شارة "مدعوم بالذكاء الاصطناعي" — اختلاف في الشكل
- **الحالي:** شارة بخلفية شبه شفافة فاتحة ذات زوايا مستديرة كبيرة، النص داخلها واضح، أيقونة نجمة صغيرة ذهبية
- **الأصلي:** شارة بحدود ذهبية رفيعة (border فقط بدون تعبئة ثقيلة)، خلفية شبه شفافة داكنة جداً، أيقونة نجمتين متقاطعتين (✦) ذهبية
- **الإصلاح:**
```css
.ai-badge {
  border: 1px solid oklch(0.74 0.13 85); /* ذهبي #C9A84C */
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.85);
  border-radius: 9999px;
  padding: 8px 24px;
  font-size: 14px;
}
```

### 4. عنوان "Arabiq Akademi" — فرق في الخط
- **الحالي:** خط sans-serif عادي (ربما Cairo أو Inter)
- **الأصلي:** خط serif أنيق (Cormorant Garamond) بوزن خفيف، أكبر حجماً وأكثر أناقة
- **الإصلاح:**
```css
.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 400;
  color: white;
  letter-spacing: -0.02em;
}
```

### 5. زر "ابدأ الآن" — فرق في الحجم والشكل
- **الحالي:** زر كبير عريض جداً بزوايا مستديرة كبيرة، لون ذهبي فاتح
- **الأصلي:** زر أصغر وأكثر أناقة، لون ذهبي غني (gradient)، زوايا مستديرة متوسطة، مع سهم ←
- **الإصلاح:**
```css
.cta-button {
  background: linear-gradient(135deg, #C9A84C 0%, #DCC06A 100%);
  color: #0F2044;
  padding: 14px 40px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}
.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px -10px rgba(201, 168, 76, 0.5);
}
```

### 6. قسم الإحصائيات (48 وحدة، 1000+ مفردة...) — فرق في الخط والخلفية
- **الحالي:** الأرقام بخط sans-serif، خلفية أفتح نسبياً بخط فاصل أعلى
- **الأصلي:** الأرقام بخط serif (Cormorant Garamond) أنيق، خلفية داكنة تندمج مع Hero، خط فاصل ذهبي رفيع أعلى القسم
- **الإصلاح:**
```css
.stats-section {
  background: linear-gradient(to bottom, #0F2044, #0B1426);
  border-top: 1px solid rgba(201, 168, 76, 0.3); /* خط ذهبي رفيع */
  padding: 3rem 0;
}
.stat-number {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.5rem;
  font-weight: 600;
  color: white;
}
.stat-label {
  font-family: 'Cairo', sans-serif;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}
```

### 7. نص "Arabiq Akademi" في الشريط العلوي
- **الحالي:** يظهر كنص عادي بجانب أيقونة الصورة المكسورة
- **الأصلي:** يظهر الشعار (صورة الحرف ع) بشكل صحيح فوق الشارة مباشرة، بدون نص "Arabiq Akademi" منفصل في الأعلى — الاسم يظهر كعنوان كبير في الوسط فقط

---

## التوجيه (Routing) — مطلوب أيضاً
في App.tsx، المسار "/" يجب أن يوجّه إلى /landing:
```jsx
<Route path="/" element={
  localStorage.getItem("token")
    ? <Navigate to="/lessons" replace />
    : <Navigate to="/landing" replace />
} />
```

---

## الخطوط المطلوبة (في index.html)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
```

---

## نظام الألوان الأصلي الكامل (styles.css من التصميم المرجعي)
```css
:root {
  --background: oklch(0.975 0.012 85);       /* #F9F7F2 عاجي دافئ */
  --foreground: oklch(0.18 0.04 270);        /* #0F1A3A كحلي داكن */
  --primary: oklch(0.22 0.06 265);           /* #0F2044 كحلي عميق */
  --primary-foreground: oklch(0.98 0.012 85); /* #FBF9F4 أبيض دافئ */
  --accent: oklch(0.74 0.13 85);             /* #C9A84C ذهبي */
  --accent-glow: oklch(0.84 0.11 88);        /* #DCC06A ذهبي فاتح */
  --card: oklch(0.99 0.006 85);              /* #FEFCF8 أبيض البطاقات */
  --border: oklch(0.88 0.02 85);             /* #E0DCD3 حدود دافئة */
  --muted-foreground: oklch(0.45 0.03 265);  /* #5C6078 نص ثانوي */

  --gradient-hero: linear-gradient(135deg, oklch(0.18 0.05 265) 0%, oklch(0.22 0.07 265) 50%, oklch(0.28 0.08 270) 100%);
  --gradient-gold: linear-gradient(135deg, oklch(0.74 0.13 85) 0%, oklch(0.84 0.11 88) 100%);
}
```

---

## ملخّص سريع — 7 أشياء تحتاج إصلاح

| # | المشكلة | الأولوية |
|---|---------|----------|
| 1 | الشعار مكسور (broken image) | 🔴 حرجة |
| 2 | الخلفية فاتحة (يجب أن تكون كحلية داكنة جداً) | 🔴 حرجة |
| 3 | خط العنوان sans بدل serif (Cormorant Garamond) | 🟡 متوسطة |
| 4 | شارة AI مختلفة الشكل (حدود بدل تعبئة) | 🟡 متوسطة |
| 5 | الزر كبير جداً ولونه فاتح | 🟡 متوسطة |
| 6 | أرقام الإحصائيات بخط sans بدل serif | 🟢 تجميلية |
| 7 | "/" لا يوجّه إلى /landing | 🔴 حرجة |
