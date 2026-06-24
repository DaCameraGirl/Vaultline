<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — حوكمة وسائط تدريب الذكاء الاصطناعي" width="100%"/>
</p>

# Vaultline

<p align="center" dir="rtl">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-5eead4?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center" dir="rtl">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_الموقع_المباشر-5eead4?style=for-the-badge&labelColor=0f131a" alt="الموقع المباشر"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_مركز_المشاريع-131a26?style=for-the-badge&labelColor=0f131a" alt="مركز المشاريع"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

<div dir="rtl">

**حوكمة وسائط تدريب الذكاء الاصطناعي** — مصدر البيانات، مراقبة الجودة، الامتثال، وإصدارات غير قابلة للتغيير لبيانات تدريب الصوت والفيديو.

أثبت ما دخل في النموذج: كل مقطع متتبَّع، يمر عبر بوابة الجودة، وجاهز للإصدار.

> **الحالة:** موقع التسويق مباشر على GitHub Pages. **المنصة الكاملة** (API + وحدة التحكم + الاستيعاب) تعمل محلياً عبر اختصار سطح المكتب أو تُنشر عبر [DEPLOY.md](./DEPLOY.md).

## المستودع مقابل الموقع المباشر

| ماذا | الرابط |
|---|---|
| **مستودع GitHub** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **التسويق / الصفحة الرئيسية** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **المنصة الكاملة** (API + وحدة التحكم + الاستيعاب) | اختصار سطح المكتب أو [DEPLOY.md](./DEPLOY.md) |
| **مركز المشاريع** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

يعرض GitHub هذا الملف README. احفظ **الموقع المباشر** في المفضلة لرابط التسويق — فهو منفصل عن صفحة المستودع.

## أبرز الميزات

| الطبقة | الوظيفة |
|---|---|
| **API للمؤسسات** | FastAPI — استيعاب، رفع، مراقبة جودة، امتثال، إصدارات، تصدير تدقيق |
| **موقع التسويق** | واجهة المنتج المباشرة على `/site/index.html` عند تشغيل API |
| **وحدة تحكم العمليات** | لوحة تحكم على `/console/index.html` — الأصول، النسب، الإجراءات |
| **CLI** | `bench.py` لعمليات خط الأنابيب |
| **الفهرس** | سجل SQLite للمصدر + الجودة + الإصدارات |
| **الوصول للسوق** | `leads/target-accounts.csv`، `marketing/one-pager.md`، قوالب التواصل |
| **Docker** | `docker compose up` لنشر بأسلوب الإنتاج |
| **Render** | مخطط `render.yaml` لـ API مستضاف |

## التشغيل محلياً (المنصة الكاملة)

**الأسهل — انقر مرتين على `Vaultline` على سطح المكتب.**

الإعداد الأولي:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

أو:

```powershell
setup\Launch Vaultline.bat
```

**الروابط عند تشغيل الخادم:**

| الواجهة | الرابط |
|---|---|
| التسويق + API مباشر | http://localhost:8470/site/index.html |
| وحدة التحكم | http://localhost:8470/console/index.html |
| توثيق API | http://localhost:8470/docs |

التحقق من كل شيء:

```powershell
powershell -File setup/verify.ps1
```

إيقاف:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## من يشتري هذا

| القطاع | المشكلة |
|---|---|
| ذكاء الصوت (ASR/TTS) | تدقيقات الموافقة والجودة قبل تسليم النموذج |
| مختبرات الفيديو / متعددة الوسائط | مجموعات بيانات معيارية بنسب قابلة للتتبع |
| موردو الذكاء الاصطناعي للمؤسسات | استبيانات المشتريات حول حوكمة البيانات |

**المشتري:** نائب رئيس الهندسة · رئيس بيانات ML · مدير امتثال الذكاء الاصطناعي

## التسويق

1. افتح `leads/target-accounts.csv`
2. استخدم القوالب في `marketing/outreach-templates.md`
3. شارك الرابط المباشر: تسويق Pages + وحدة تحكم مستضافة أو عرض محلي
4. أرفق `marketing/one-pager.md` في مكالمات المؤسسات

راجع `marketing/CAMPAIGN.md` لخطة الـ 30 يوماً.

## مرجع API سريع

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## النشر في الإنتاج

راجع **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (تسويق)، Render (API)، أو Docker.

## هيكل المشروع

```text
Vaultline/
├── api/server.py           API للمؤسسات
├── marketing/              الصفحة الرئيسية + نصوص GTM (مصدر نشر Pages)
├── console/                لوحة تحكم العمليات
├── leads/                  الحسابات المستهدفة
├── workbench/              الفهرس، الجودة، الاستيعاب، التصدير
├── catalog/                سجل SQLite (محلي، gitignored)
├── releases/               حزم بيانات غير قابلة للتغيير
├── docs/assets/            SVG البطل في README
└── config/enterprise.yaml  إعدادات المنتج
```

## المساهمون

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — توجيه المنتج، GTM، الاختبار
- **Claude** — هيكل المنصة، API، وحدة التحكم، التسويق، حزمة النشر

## الترخيص

© 2026 Angela Hudson (DaCameraGirl). راجع [LICENSE](./LICENSE).

</div>