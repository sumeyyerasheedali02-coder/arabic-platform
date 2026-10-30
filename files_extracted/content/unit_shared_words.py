"""Shared Arabic-Turkish words for the «كلمات مشتركة» tab of each unit.

Pure data, no database access. Every unit lists the words of
`content.shared_words` that belong to the unit's topic, written as
"arabic=turkish" pairs and looked up in that audited dataset, so the usage
label and the false-friend note always come from one place. A pair that is
not in the dataset raises at import time, which keeps the two files in step.

Units are keyed by `unit_number` (1-48), never by database id.
"""
from content.shared_words import all_words

_UNIT_PAIRS = {
    # ── الكتاب الأول ──
    1: """سلام=selam | سلامة=selamet | عزيز=aziz | عزيزي=aziz | صديق=sadık | صداقة=sadakat
        | صحبة=sohbet | ضيافة=ziyafet | مسافر=misafir | مبارك=mübarek | احترام=ihtiram
        | محترم=muhterem | حرمة=hürmet | سعادة=saadet | عافية=afiyet | شكر=şükür
        | أستاذ=üstat | اسم=isim | إنسان=insan | حال=hal | أحوال=ahval | شخص=şahıs
        | شخصية=şahsiyet | لقاء=lika | مقابلة=mülakat | رحمة=rahmet | بركة=bereket
        | هوية=hüviyet | عنوان=unvan | طالب=talebe""",
    2: """عائلة=aile | أقرباء=akraba | قرابة=karabet | أب=eb | والد=valide | والدة=valide
        | أخت=uht | عم=amca | زوج=zevç | زوجة=zevce | طفل=tıfıl | يتيم=yetim | نسب=nesep
        | نسيب=nasip | نسل=nesil | أهل=ehil | جنين=cenin | ميراث=miras | وريث=varis
        | ورثة=verese | رحمة=rahmet | حنان=hanan | رأفة=re'fet | تربية=terbiye
        | عجوز=acuze | بالغ=baliğ | ولادة=veladet | مولود=mevlit""",
    3: """بناء=bina | بناية=bina | عمارة=imaret | منزل=menzil | مكان=mekân | محلة=mahalle
        | حديقة=hadika | بستان=bostan | باب=bab | حجرة=hücre | سقف=sakıf | قبة=kubbe
        | مفتاح=miftah | قفل=kilit | فرش=ferş | مفرش=mefruşat | ستار=setre | قنديل=kandil
        | مصباح=misbah | سراج=sirac | صندوق=sandık | إبريق=ibrik | فنجان=fincan | كأس=kâse
        | صحن=sahan | طبق=tabak | طنجرة=tencere | طاسة=tas | حوض=havuz | مجلس=meclis
        | مخزن=mahzen | قماش=kumaş | ترميم=tamir | تعمير=tamir | منقل=mangal | دائرة=daire""",
    4: """ساعة=saat | دقيقة=dakika | ثانية=saniye | يوم=yevm | يومية=yevmiye | أسبوع=usbu
        | زمان=zaman | دوام=devam | لحظة=lahza | تقويم=takvim | مرة=merre | دفعة=defa
        | راحة=rahat | تعب=tab | نشاط=neşat | برنامج=program | استراحة=istirahat
        | حاجة=hacat | لازم=lazım | ترتيب=tertip | نظام=nizam | فرح=ferah | أول=evvel
        | آخر=ahir | بداية=bidayet | نهاية=nihayet | تلفون=telefon | تلفزيون=televizyon
        | راديو=radyo | سيارة=seyyare""",
    5: """طعام=taam | غذاء=gıda | غذائي=gıdai | شربات=şerbet | شراب=şarap | سكر=şeker | قهوة=kahve
        | شاي=çay | لبن=leben | زيت=zeyt | زيتون=zeytin | ملح=melh | عسل=asel | حلوى=helva
        | حمص=humus | كباب=kebap | كفتة=köfte | شوربة=çorba | سلطة=salata | فطيرة=pide
        | طماطم=domates | برتقال=portakal | ليمون=limon | موز=muz | رمان=nar
        | بطاطا=patates | باذنجان=patlıcan | بندق=fındık | فستق=fıstık | سمسم=susam
        | طحينة=tahin | زعتر=zahter | زنجبيل=zencefil | كمون=kimyon | زعفران=safran
        | ريحان=reyhan | سفرة=sofra | صينية=sini | تنور=tandır | فرن=fırın | مربى=murabba
        | لقمة=lokma | محشي=mahşi""",
    6: """صلاة=salat | صلوات=salavat | مسجد=mescit | محراب=mihrap | منبر=minber | مئذنة=minare
        | أذان=ezan | مؤذن=müezzin | إمام=imam | قبلة=kıble | ركعة=rekât | سجدة=secde
        | سجود=sücud | تسليم=teslim | تسبيح=tesbih | دعاء=dua | طهارة=taharet | طاهر=tahir
        | نجاسة=necaset | نجس=necis | جنابة=cenabet | فرض=farz | واجب=vacip | سنة=sünnet
        | مكروه=mekruh | مباح=mubah | حرام=haram | حلال=helal | نية=niyet | فاتحة=Fatiha
        | سورة=sure | آية=ayet | آمين=amin | عبادة=ibadet | تلاوة=tilavet | تجويد=tecvid
        | جنازة=cenaze | إخلاص=ihlas | تقوى=takva | قرآن=Kur'an""",
    7: """مدرسة=medrese | مكتب=mektep | جامعة=camia | كلية=külliye | درس=ders | دفتر=defter
        | قلم=kalem | كتاب=kitap | مكتبة=kütüphane | طالب=talebe | تلميذ=tilmiz | معلم=muallim
        | مدرس=müderris | مدير=müdür | امتحان=imtihan | سؤال=sual | جواب=cevap | نجاح=necah
        | نتيجة=netice | علم=ilim | تعليم=talim | تربية=terbiye | فصل=fasıl | صف=saf
        | موضوع=mevzu | مسألة=mesele | مثال=misal | قاعدة=kaide | شرح=şerh | تاريخ=tarih
        | جغرافيا=coğrafya | رياضيات=riyaziyat | مناقشة=münakaşa | محاضرة=muhazara
        | تطبيق=tatbik | تجربة=tecrübe | برنامج=program | شهادة=şehadet | دبلوم=diploma
        | معلومة=malumat | عنوان=unvan | ملخص=mülahhas""",
    8: """مهندس=mühendis | طبيب=tabip | محاسب=muhasebeci | تاجر=tacir | مدير=müdür | رئيس=reis
        | مأمور=memur | وظيفة=vazife | وزير=vezir | وزارة=vezaret | شركة=şirket
        | مؤسسة=müessese | شريك=şerik | إدارة=idare | دائرة=daire | عامل=amil | خدمة=hizmet
        | عقد=akit | خبرة=hibre | مهارة=maharet | ماهر=mahir | صناعة=sanayi | صنعة=sanat
        | مصلحة=maslahat | تجارة=ticaret | ربح=ribh | أرباح=erbah | مسؤول=mesul
        | مسؤولية=mesuliyet | اجتماع=içtima | إجازة=icazet | تعاون=teavün | تدريب=tedrip
        | مقابلة=mülakat | مكتب=mektep | شرط=şart""",
    9: """سوق=suk | بازار=pazar | دكان=dükkân | تاجر=tacir | تجارة=ticaret | بيع=bey
        | مشتري=müşteri | شراء=şira | سعر=sa'r | ثمن=semen | قيمة=kıymet | نقد=nakit
        | نقدي=nakdi | مال=mal | فاتورة=fatura | شيك=çek | دينار=dinar | درهم=dirhem
        | ليرة=lira | ريال=riyal | دولار=dolar | يورو=avro | قرش=kuruş | حساب=hesap
        | مبلغ=meblağ | ضريبة=daribe | تقسيط=taksit | قسط=taksit | مصروف=masraf
        | نوع=nevi | كمية=kemiyet | لون=levn | قماش=kumaş | حرير=harir | ماركة=marka
        | موديل=model | مزاد=müzayede | طلب=talep | عرض=arz | حوالة=havale | ميزان=mizan
        | خسارة=hasar | ربح=ribh""",
    10: """هواء=hava | حرارة=hararet | حار=har | برد=berd | برودة=berudet | رياح=riyah
        | برق=berk | رعد=ra'd | صاعقة=saika | غبار=gubar | بخار=buhar | دخان=duhan
        | طوفان=tufan | فيضان=feyezan | زلزال=zelzele | موسم=mevsim | سماء=sema | شمس=şems
        | قمر=kamer | نور=nur | شعاع=şua | ماء=ma | طين=tin | تراب=turap | أفق=ufuk
        | هلال=hilal | كسوف=küsuf | خسوف=husuf | نجم=necm | طبيعة=tabiat | طبيعي=tabii
        | إقليم=iklim | فصل=fasıl""",
    11: """مدينة=medine | بلد=belde | بلدة=belde | مركز=merkez | ميدان=meydan | محلة=mahalle
        | ناحية=nahiye | منطقة=mıntıka | بلدية=belediye | شعب=şa'b | مواطن=vatandaş
        | وطن=vatan | وطني=vatani | مجتمع=cemiyet | جماعة=cemaat | أهل=ehil | زائر=ziyaretçi
        | زيارة=ziyaret | ضيافة=ziyafet | مسافر=misafir | غريب=garip | شخص=şahıs
        | إنسان=insan | سفارة=sefare(t) | سفير=sefir | ميناء=mina | مطار=matar | محطة=mahata
        | مقبرة=makbere | حديقة=hadika | سوق=suk | عمارة=imaret | بناية=bina | إسطنبول=İstanbul
        | أنقرة=Ankara | إزمير=İzmir | بورصة=Bursa""",
    12: """فن=fen | فنان=fennan | موسيقى=musiki | لحن=lahn | نغمة=nağme | عود=ud | نَاي=ney
        | طبل=tabl | دف=def | رقص=raks | مسرح=mesrah | سينما=sinema | فيلم=film | تمثيل=temsil
        | ممثل=mümessil | شعر=şiir | شاعر=şair | قصة=kıssa | حكاية=hikâye | رسام=ressam
        | صورة=suret | تصوير=tasvir | كاميرا=kamera | فوتوغرافيا=fotoğrafçılık
        | كتاب=kitap | مجلة=mecmua | كتابة=kitabet | خط=hat | إبداع=ibda | ديوان=divan
        | قصيدة=kaside | غزل=gazel | تلفزيون=televizyon | راديو=radyo | سفر=sefer
        | قهوة=kahve | شاي=çay | حديقة=hadika""",
    13: """سفر=sefer | سفينة=sefine | سفير=sefir | سفارة=sefare(t) | طائرة=tayyare | طيار=tayyar
        | مطار=matar | ميناء=mina | محطة=mahata | سيارة=seyyare | حافلة=kafile | قافلة=kafile
        | طريق=tarik | تذكرة=tezkere | زيارة=ziyaret | زائر=ziyaretçi | منزل=menzil
        | مسافر=misafir | هوية=hüviyet | جنسية=cinsiyet | تبعِيّة=tabiiyet | مرور=mürur
        | ممر=memerr | مرفأ=merfa | خريطة=harita | شرق=şark | غرب=garp | شمال=şimal
        | جَنوب=cenup | جهة=cihet | غربة=gurbet | بلد=belde | وطن=vatan | إسطنبول=İstanbul
        | أنقرة=Ankara | إزمير=İzmir | بورصة=Bursa | دبي=Dubai | أبو ظبي=Abu Dabi""",
    14: """حج=hac | حاج=hacı | عمرة=umre | كعبة=Kâbe | قبلة=kıble | مسجد=mescit | صلاة=salat
        | طهارة=taharet | فرض=farz | واجب=vacip | سنة=sünnet | دعاء=dua | ذكر=zikir
        | تسبيح=tesbih | توبة=tövbe | مغفرة=mağfiret | استغفار=istiğfar | غفران=gufran
        | رحمة=rahmet | بركة=bereket | مبارك=mübarek | عبادة=ibadet | نية=niyet | ثواب=sevap
        | صبر=sabır | تقوى=takva | ذنب=zenb | زيارة=ziyaret | مزار=mezar | هجرة=hicret
        | قافلة=kafile | سفر=sefer | ضيافة=ziyafet | صدقة=sadaka | زكاة=zekât
        | إيمان=iman | مؤمن=mümin | مسلم=Müslüman | إسلام=İslam | حشر=haşir | تلاوة=tilavet""",
    15: """طبيب=tabip | طب=tıp | طبية=tıbbi | دكتور=doktor | مريض=mariz | مرض=maraz | علاج=ilaç
        | دواء=deva | صحة=sıhhat | صحي=sıhhi | شفاء=şifa | عافية=afiyet | ألم=elem
        | وجع=veca | حمى=humma | جرح=cerh | جراح=cerrah | جراحة=cerrahi | عملية=ameliyat
        | عصب=asab | عضلة=adale | قلب=kalp | كبد=kebed | معدة=mide | صدر=sadır
        | حنجرة=hançere | جسم=cisim | بدن=beden | جلد=cilt | دم=dem | نبض=nabız
        | نفَس=nefes | ضعف=zaaf | ضعيف=zayıf | قوة=kuvvet | تعب=tab | سرطان=seretan
        | ميكروب=mikrop | فيروس=virüs | بكتيريا=bakteri | فيتامين=vitamin | وباء=veba
        | إسهال=ishal | قبض=kabız | ضماد=zımad | تشخيص=teşhis | نقاهة=nekahat | سلامة=selamet""",
    16: """عيد=ıyd | رمضان=Ramazan | صوم=savm | صيام=siyam | فطر=fıtır | ضيافة=ziyafet
        | زيارة=ziyaret | سفر=sefer | راحة=rahat | استراحة=istirahat | فرح=ferah | سرور=sürur
        | سعادة=saadet | مناسبة=münasebet | حلوى=helva | شربات=şerbet | سكر=şeker
        | مبارك=mübarek | مولد=mevlit | موسم=mevsim | إجازة=icazet | تقويم=takvim
        | أسبوع=usbu | يوم=yevm | شعبان=Şaban | رجب=Recep | شوال=Şevval | ذو الحجة=Zilhicce
        | محرم=Muharrem | قربان=kurban | صدقة=sadaka | زكاة=zekât | دعاء=dua | رحمة=rahmet""",
    # ── الكتاب الثاني ──
    17: """صحة=sıhhat | صحي=sıhhi | سلامة=selamet | عافية=afiyet | طب=tıp | طبيب=tabip
        | علاج=ilaç | دواء=deva | فيتامين=vitamin | بروتين=protein | كولسترول=kolesterol
        | هرمون=hormon | جسد=ceset | جسم=cisim | بدن=beden | ميكروب=mikrop | فيروس=virüs
        | غذاء=gıda | غذائي=gıdai | راحة=rahat | حياة=hayat | روح=ruh | نفسية=nefsi
        | روحي=ruhi | وهم=vehim | وسواس=vesvese | فوبيا=fobi | مرض=maraz | عضلة=adale
        | نشاط=neşat | سرطان=seretan | كريم=krem | معجون=macun | ضعف=zaaf | قوة=kuvvet
        | قوي=kavi | تشخيص=teşhis | شفاء=şifa | نقاهة=nekahat""",
    18: """راحة=rahat | استراحة=istirahat | فرح=ferah | سرور=sürur | سعادة=saadet | مسرح=mesrah
        | سينما=sinema | موسيقى=musiki | لحن=lahn | نغمة=nağme | غزل=gazel | رقص=raks
        | حديقة=hadika | بستان=bostan | قهوة=kahve | شاي=çay | فن=fen | فنان=fennan
        | ظريف=zarif | ظرافة=zarafet | لطيف=Latif | لطافة=letafet | لذيذ=leziz | لذّة=lezzet
        | صحبة=sohbet | صداقة=sadakat | مجلس=meclis | خيال=hayal | تخيل=tahayyül
        | كوميديا=komedi | دراما=drama | تراجيديا=trajedi | تلفزيون=televizyon
        | فيلم=film | صورة=suret | سفر=sefer""",
    19: """زوج=zevç | زوجة=zevce | عائلة=aile | أهل=ehil | نسب=nesep | نسيب=nasip | قرابة=karabet
        | أقرباء=akraba | حب=hubb | عشق=aşk | عاشق=âşık | معشوق=maşuk | محبة=muhabbet
        | محبوب=mahbup | وفاء=vefa | وفي=vefalı | صداقة=sadakat | صادق=sadık | رحمة=rahmet
        | حنان=hanan | عفة=iffet | عفيف=afif | حرمة=hürmet | احترام=ihtiram | رضا=rıza
        | ميراث=miras | ورثة=verese | وصي=vasi | كفالة=kefalet | كفيل=kefil | عقد=akit
        | شرط=şart | ولادة=veladet | مولود=mevlit | طفل=tıfıl | سعادة=saadet | أمل=emel
        | أمين=emin | شرف=şeref | كرامة=keramet | نصيحة=nasihat""",
    20: """مدينة=medine | مدني=medeni | مدنية=medeniyet | بلدية=belediye | بلدة=belde
        | مركز=merkez | ميدان=meydan | محلة=mahalle | طريق=tarik | مرور=mürur | سيارة=seyyare
        | حافلة=kafile | محطة=mahata | مطار=matar | ميناء=mina | مرفأ=merfa | سوق=suk
        | دكان=dükkân | بازار=pazar | عمارة=imaret | بناية=bina | بناء=bina | حديقة=hadika
        | مسجد=mescit | مكتبة=kütüphane | مدرسة=medrese | جامعة=camia | شرطة=şurta
        | ضابط=zabit | حكومة=hükümet | وزارة=vezaret | إدارة=idare | دائرة=daire
        | ولاية=vilayet | والي=vali | منطقة=mıntıka | ناحية=nahiye | نظام=nizam
        | انضباط=inzibat | تنظيم=tanzim | مواطن=vatandaş""",
    21: """علم=ilim | علوم=ulum | عالم=âlim | معرفة=marifet | فكرة=fikir | فكر=fikir
        | تفكير=tefekkür | عقل=akıl | عاقل=akil | ذكي=zeki | ذكاء=zekâ | فهم=fehim
        | ذهن=zihin | إدراك=idrak | نظرية=nazariye | نظري=nazari | تجربة=tecrübe
        | تحليل=tahlil | تحقيق=tahkik | دليل=delil | برهان=burhan | ملاحظة=mülahaza
        | تعليم=talim | تربية=terbiye | مدرسة=medrese | جامعة=camia | كلية=külliye
        | مكتبة=kütüphane | كتاب=kitap | قلم=kalem | دفتر=defter | امتحان=imtihan
        | نجاح=necah | شهادة=şehadet | جهل=cehalet | جاهل=cahil | نور=nur | تنوير=tenvir
        | منوّر=münevver | مجتهد=müçtehit | اجتهاد=içtihat | حكمة=hikmet""",
    22: """طبيب=tabip | جراح=cerrah | مهندس=mühendis | معلم=muallim | مدرس=müderris
        | أستاذ=üstat | محاسب=muhasebeci | تاجر=tacir | صراف=sarraf | رسام=ressam
        | ممثل=mümessil | مطرب=mutrip | عازف=azif | فنان=fennan | أديب=edip | شاعر=şair
        | كاتب=kâtip | مؤلف=müellif | مترجم=tercüman | ناشر=naşir | صحافي=sahafi
        | مفتي=müftü | إمام=imam | مؤذن=müezzin | ضابط=zabit | عسكري=askerî | طيار=tayyar
        | سفير=sefir | وزير=vezir | مدير=müdür | رئيس=reis | مأمور=memur | مفتش=müfettiş
        | وكيل=vekil | فلاح=fellah | عامل=amil | خادم=hademe | معمار=mimar | وظيفة=vazife""",
    23: """كلمة=kelime | جملة=cümle | حرف=harf | فعل=fiil | اسم=isim | فاعل=fail | مفعول=mef'ul
        | صفة=sıfat | ضمير=zamir | لغة=lügat | لسان=lisan | لهجة=lehçe | معجم=mu'cem
        | مفردات=müfredat | أصل=asıl | جذر=cezir | وزن=vezin | نقطة=nokta | فاصلة=fasıla
        | إملاء=imla | خط=hat | كتابة=kitabet | بلاغة=belagat | فصاحة=fesahat | أدب=edep
        | أدبيات=edebiyat | شعر=şiir | شاعر=şair | قافية=kafiye | قصيدة=kaside | ديوان=divan
        | مجاز=mecaz | تعبير=tabir | عبارة=ibare | معنى=mana | لفظ=lafız | ترجمة=tercüme
        | مترجم=tercüman | أسلوب=üslup | عربي=Arap | عربية=Arapça | نص=nas | مقال=makal
        | رسالة=risale | تأكيد=tekit | تكرار=tekrar | جمع=cem | مبني=mebni | معلوم=malum
        | مجهول=meçhul""",
    24: """مكافأة=mükâfat | نجاح=necah | تفوق=tefevvuk | متفوق=mütefevvik | ممتاز=mümtaz
        | تميز=temayüz | متميز=mümtaz | شهادة=şehadet | دبلوم=diploma | إبداع=ibda
        | اعتراف=itiraf | تقدير=takdir | احترام=ihtiram | شرف=şeref | عزة=izzet | كرامة=keramet
        | شهرة=şöhret | مشهور=meşhur | فن=fen | أدب=edep | علم=ilim | عالم=âlim
        | فيلسوف=filozof | فلسفة=felsefe | كيمياء=kimya | فيزياء=fizik | طب=tıp
        | سلام=selam | اقتصاد=iktisat | منافسة=münafese | انتخاب=intihap | منتخب=müntehap
        | ثواب=sevap | نصر=nusret | منصور=mansur | تاريخ=tarih""",
    25: """تكنولوجيا=teknoloji | تقنية=teknik | إنترنت=internet | كمبيوتر=kompüter | هاتف=hatif
        | تلفون=telefon | تلفزيون=televizyon | راديو=radyo | ساتلايت=satellit | ميديا=medya
        | إعلام=ilam | إعلان=ilan | خبر=haber | أخبار=ahbar | صحافة=sahafet | صحيفة=sahife
        | تواصل=tevassul | ارتباط=irtibat | عالم=âlem | كون=kâinat | حضارة=hazara
        | مدنية=medeniyet | لغة=lügat | ترجمة=tercüme | سفر=sefer | طائرة=tayyare
        | إيميل=e-mail | واي فاي=Wi-Fi | بيانات=beyan | موقع=mevki | لينك=link
        | أونلاين=online | ديجيتال=dijital | إلكتروني=elektronik | كاميرا=kamera
        | فيديو=video | روبوت=robot | ليزر=lazer | مودم=modem | سيرفر=server""",
    26: """نزاهة=nezahet | نزيه=nezih | نظيف=nezih | طهارة=taharet | طاهر=tahir | نجاسة=necaset
        | نجس=necis | صافي=safi | صفاء=sefa | نقي=naki | نقاء=neka | مُصفّى=musaffa
        | خالص=halis | ماء=ma | جسم=cisim | بدن=beden | جلد=cilt | ميكروب=mikrop
        | بكتيريا=bakteri | فيروس=virüs | صحة=sıhhat | صحي=sıhhi | وباء=veba | مرض=maraz
        | علاج=ilaç | غبار=gubar | تراب=turap | طين=tin | خراب=harap | بيئة=biat
        | ترتيب=tertip | تنظيم=tanzim | انتظام=intizam | منتظم=muntazam | لطافة=letafet
        | أدب=edep | إصلاح=ıslah | تصليح=ıslah | ترميم=tamir | تحذير=tahzir | نصيحة=nasihat
        | إهمال=ihmal | فساد=fesat | حوض=havuz | إبريق=ibrik | طاسة=tas""",
    27: """إسلام=İslam | مسلم=Müslüman | إيمان=iman | مؤمن=mümin | الله=Allah | رسول=resul
        | نبي=nebi | قرآن=Kur'an | آية=ayet | سورة=sure | حديث=hadis | سنة=sünnet
        | شريعة=şeriat | فقه=fıkıh | عقيدة=akide | عبادة=ibadet | صلاة=salat | زكاة=zekât
        | صوم=savm | حج=hac | دين=din | ملة=millet | أمة=ümmet | إخلاص=ihlas | تقوى=takva
        | توبة=tövbe | رحمة=rahmet | عدالة=adalet | حكمة=hikmet | ملائكة=melaike
        | جنة=cennet | جهنم=cehennem | آخرة=ahiret | قيامة=kıyamet | حشر=haşir | قبر=kabir
        | صراط=sırat | ثواب=sevap | عقاب=ikap | ذنب=zenb | حلال=helal | حرام=haram
        | فرض=farz | واجب=vacip | مفتي=müftü | فتوى=fetva | خليفة=halife | صحابة=sahabe
        | معجزة=mucize | رسالة=risalet""",
    28: """شباب=şebap | أمل=emel | آمال=emeller | عزم=azim | عزيمة=azimet | إرادة=irade
        | إصرار=ısrar | نشاط=neşat | قوة=kuvvet | قوي=kavi | حرية=hürriyet
        | استقلال=istiklal | مستقل=müstakil | مبدأ=mebde | مبادئ=mebadi | فكرة=fikir
        | فكر=fikir | خيال=hayal | أخلاق=ahlak | أدب=edep | احترام=ihtiram | صداقة=sadakat
        | زميل=zümre | رفيق=refik | جماعة=cemaat | جمعية=cemiyet | اجتماعي=içtimai
        | قومية=kavmiyet | وطن=vatan | وطني=vatani | تعليم=talim | مستقبل=müstakbel
        | تجربة=tecrübe | تحرر=tahrir | تغيير=tağyir | حزب=hizip | سياسة=siyaset""",
    29: """مصر=Mısır | سوريا=Suriye | لبنان=Lübnan | عراق=Irak | الأردن=Ürdün | فلسطين=Filistin
        | السعودية=Suudi Arabistan | اليمن=Yemen | عمان=Umman | الكويت=Kuveyt
        | البحرين=Bahreyn | الإمارات=Emirlikler | ليبيا=Libya | تونس=Tunus
        | الجزائر=Cezayir | المغرب=Mağrip | السودان=Sudan | إسطنبول=İstanbul
        | أنقرة=Ankara | أمة=ümmet | ملة=millet | خلافة=hilafet | خليفة=halife
        | سلطان=sultan | سلطنة=saltanat | دولة=devlet | جمهورية=cumhuriyet | إمارة=emirlik
        | أمير=emir | ولاية=vilayet | والي=vali | إقليم=iklim | وطن=vatan | شعب=şa'b
        | قوم=kavim | مدنية=medeniyet | حضارة=hazara | تاريخ=tarih | قرن=karn
        | عصر=asır | مذهب=mezhep | طائفة=taife | اتحاد=ittihat | اتفاق=ittifak
        | وحدة=vahdet | هجرة=hicret | شرق=şark | غرب=garp""",
    30: """أمين=emin | أمان=aman | ضابط=zabit | عسكر=asker | عسكري=askerî | جيش=ceyş
        | شرطة=şurta | قانون=kanun | قانوني=kanuni | قرار=karar | حكم=hüküm | حكومة=hükümet
        | دولة=devlet | محكمة=mahkeme | محاكمة=muhakeme | دعوى=dava | جريمة=cürüm
        | مجرم=mücrim | عقوبة=ukubet | جزاء=ceza | اتهام=itham | متهم=müttehem
        | شاهد=şahit | دليل=delil | إثبات=ispat | اعتراف=itiraf | عدالة=adalet | عادل=adil
        | ظلم=zulüm | ظالم=zalim | مظلوم=mazlum | حق=hak | حقوق=hukuk | حماية=himaye
        | خوف=havf | احتياط=ihtiyat | إنذار=inzar | تحذير=tahzir | انضباط=inzibat
        | نظام=nizam | استقرار=istikrar | سلامة=selamet | حصار=hisar | سياسة=siyaset
        | معاهدة=muahede | مخابرات=muhaberat | تفتيش=teftiş | مفتش=müfettiş | رقابة=rakabe
        | رقيب=rakip | قائد=kaid | قيادة=kıyadet""",
    31: """بيئة=biat | طبيعة=tabiat | طبيعي=tabii | هواء=hava | ماء=ma | تراب=turap | طين=tin
        | غبار=gubar | دخان=duhan | بخار=buhar | غاز=gaz | كربون=karbon | أكسجين=oksijen
        | نيتروجين=nitrojen | هيدروجين=hidrojen | مادة=madde | عنصر=unsur | عناصر=anasır
        | كيمياء=kimya | كيميائي=kimyevi | بلاستيك=plastik | معدن=maden | حديد=hadid
        | نحاس=nühas | وباء=veba | مرض=maraz | ضرر=zarar | مضر=muzır | فساد=fesat
        | خراب=harap | أثر=eser | آثار=asar | تأثير=tesir | مؤثر=müessir | سبب=sebep
        | نتيجة=netice | حرارة=hararet | نبات=nebat | نباتات=nebatat | حيوان=hayvan
        | حشرة=haşere | زراعة=ziraat | محصول=mahsul | بحر=bahir | نهر=nehir
        | بحيرة=bahire | ساحل=sahil | جبل=cebel | أرض=arz""",
    32: """طاقة=takat | قوة=kuvvet | قدرة=kudret | نار=nar | نيران=niran | نور=nur
        | حرارة=hararet | إلكترون=elektron | إلكتروني=elektronik | نيوترون=nötron
        | بروتون=proton | ذرة=zerre | عنصر=unsur | يورانيوم=uranyum | راديوم=radyum
        | هيدروجين=hidrojen | كربون=karbon | غاز=gaz | بخار=buhar | ماء=ma | معدن=maden
        | حديد=hadid | نحاس=nühas | ذهب=zehep | فضة=fıdda | موتور=motor | ماكينة=makine
        | ميكانيك=mekanik | آلة=alet | جهاز=cihaz | أمبير=amper | فولت=volt | واط=vat
        | كيلوواط=kilovat | هرتز=hertz | تكنولوجيا=teknoloji | تقنية=teknik
        | فيزياء=fizik | نظرية=nazariye | تجربة=tecrübe | معادلة=muadele | ميزان=mizan
        | كتلة=kütle | حجم=hacim | مساحة=mesaha | مسافة=mesafe | سطح=satıh | نسبة=nispet
        | شمس=şems | بركان=volkan | ليزر=lazer""",
    # ── الكتاب الثالث ──
    33: """قرآن=Kur'an | معجزة=mucize | آية=ayet | سورة=sure | مصحف=mushaf | تلاوة=tilavet
        | تجويد=tecvid | تفسير=tefsir | حديث=hadis | بلاغة=belagat | فصاحة=fesahat
        | بليغ=beliğ | كتاب=kitap | رسالة=risalet | رسول=resul | نبي=nebi | حكمة=hikmet
        | بيان=beyan | أبد=ebed | أبدي=ebedi | أزل=ezel | أزلي=ezeli | إلهي=ilahi
        | إله=ilah | الله=Allah | رحمان=Rahman | رحيم=Rahim | حفظ=hıfz | حافظ=hafız
        | يقين=yakin | إيمان=iman | عقيدة=akide | شريعة=şeriat | حلال=helal | حرام=haram
        | فاتحة=Fatiha | ياسين=Yasin | خاتمة=hatime | نور=nur | برهان=burhan
        | دليل=delil | حقيقة=hakikat | إنسان=insan""",
    34: """يوم=yevm | ساعة=saat | دقيقة=dakika | دوام=devam | درس=ders | مدرسة=medrese
        | تلميذ=tilmiz | معلم=muallim | كتاب=kitap | دفتر=defter | قلم=kalem | امتحان=imtihan
        | واجب=vacip | صديق=sadık | زميل=zümre | أب=eb | والدة=valide | عائلة=aile
        | منزل=menzil | طعام=taam | غذاء=gıda | شاي=çay | قهوة=kahve | راحة=rahat
        | تعب=tab | نشاط=neşat | برنامج=program | ترتيب=tertip | نظام=nizam | زمان=zaman
        | لحظة=lahza | أول=evvel | آخر=ahir | نهاية=nihayet | بداية=bidayet
        | تلفزيون=televizyon | كمبيوتر=kompüter | إنترنت=internet | هاتف=hatif
        | سيارة=seyyare | حافلة=kafile | طريق=tarik | صلاة=salat | أذان=ezan | مسجد=mescit
        | دعاء=dua""",
    35: """مسلم=Müslüman | إسلام=İslam | أمة=ümmet | ملة=millet | جماعة=cemaat | جمعية=cemiyet
        | مجتمع=cemiyet | شعب=şa'b | قوم=kavim | قومية=kavmiyet | وطن=vatan | مواطن=vatandaş
        | جنسية=cinsiyet | هوية=hüviyet | حقوق=hukuk | حق=hak | حرية=hürriyet
        | عدالة=adalet | مساواة=müsavat | ظلم=zulüm | مظلوم=mazlum | هجرة=hicret
        | مهاجر=muhacir | غربة=gurbet | غريب=garip | دولة=devlet | حكومة=hükümet
        | قانون=kanun | دين=din | مذهب=mezhep | طائفة=taife | عقيدة=akide | عبادة=ibadet
        | مسجد=mescit | مدرسة=medrese | لغة=lügat | لسان=lisan | حضارة=hazara
        | تاريخ=tarih | اتحاد=ittihat | وحدة=vahdet | استقلال=istiklal | صبر=sabır
        | تعاون=teavün | سياسة=siyaset | ديمقراطية=demokrasi""",
    36: """سنة=sünnet | حديث=hadis | رسول=resul | نبي=nebi | صحابة=sahabe | رواية=rivayet
        | سند=senet | صحيح=sahih | ثابت=sabit | أخلاق=ahlak | أدب=edep | آداب=edep
        | حكمة=hikmet | رحمة=rahmet | أمانة=emanet | أمين=emin | صادق=sadık | صدْق=sıdk
        | صبر=sabır | تقوى=takva | إخلاص=ihlas | عبادة=ibadet | صلاة=salat | صوم=savm
        | زكاة=zekât | حج=hac | فقه=fıkıh | فتوى=fetva | مفتي=müftü | إمام=imam
        | شيخ=şeyh | عالم=âlim | علم=ilim | فرض=farz | واجب=vacip | مكروه=mekruh
        | مباح=mubah | تفسير=tefsir | شرح=şerh | تصديق=tasdik | توبة=tövbe
        | مغفرة=mağfiret | ذكر=zikir | دعاء=dua | بركة=bereket | مبارك=mübarek
        | هجرة=hicret | مولد=mevlit""",
    37: """طفل=tıfıl | كتاب=kitap | مكتبة=kütüphane | قصة=kıssa | حكاية=hikâye | رواية=rivayet
        | مجلة=mecmua | صحيفة=sahife | صفحة=sayfa | ورقة=varak | حرف=harf | كلمة=kelime
        | جملة=cümle | خط=hat | كتابة=kitabet | قلم=kalem | دفتر=defter | رسم=resim
        | رسام=ressam | صورة=suret | خيال=hayal | تخيل=tahayyül | فكرة=fikir | فهم=fehim
        | ذهن=zihin | ذكاء=zekâ | ذكي=zeki | تعليم=talim | تربية=terbiye | مدرسة=medrese
        | معلم=muallim | تلميذ=tilmiz | والدة=valide | عائلة=aile | فرح=ferah | سرور=sürur
        | معرفة=marifet | علم=ilim | معلومة=malumat | عنوان=unvan | مؤلف=müellif
        | ناشر=naşir | طباعة=tab | مطبعة=matbaa | نسخة=nüsha | تلفزيون=televizyon
        | كمبيوتر=kompüter""",
    38: """هجرة=hicret | مهاجر=muhacir | هجر=hicr | هجران=hicran | غربة=gurbet | غريب=garip
        | وطن=vatan | وطني=vatani | عقل=akıl | فكر=fikir | عالم=âlim | علم=ilim
        | علوم=ulum | مهندس=mühendis | طبيب=tabip | دكتور=doktor | بحث=bahis | تعليم=talim
        | جامعة=camia | شهادة=şehadet | خبرة=hibre | مهارة=maharet | ماهر=mahir
        | اقتصاد=iktisat | اقتصادي=iktisadi | مال=mal | عمل=amel | وظيفة=vazife
        | فرصة=fırsat | حاجة=hacat | فقير=fakir | دولة=devlet | حكومة=hükümet
        | سياسة=siyaset | تقنية=teknik | تكنولوجيا=teknoloji | حضارة=hazara
        | مدنية=medeniyet | مستقبل=müstakbel | أمل=emel | خسارة=hasar | ضرر=zarar
        | ضياع=ziya | ضائع=zayi | رجوع=rücu | رجعة=ricat | انتقال=intikal | سفر=sefer
        | اختيار=ihtiyar | اضطرار=ıztırar | مضطر=muztar | إصلاح=ıslah""",
    39: """راحة=rahat | استراحة=istirahat | تعب=tab | إرهاق=irhak | صحة=sıhhat | صحي=sıhhi
        | مرض=maraz | علاج=ilaç | دواء=deva | طبيب=tabip | طب=tıp | نفس=nefis
        | نفسية=nefsi | روح=ruh | روحي=ruhi | أعصاب=asabi | عصبي=asabi | عصب=asab
        | وسواس=vesvese | وهم=vehim | فوبيا=fobi | خوف=havf | رؤيا=rüya | رؤية=rüya
        | خيال=hayal | تخيل=tahayyül | يوم=yevm | ساعة=saat | زمان=zaman | نشاط=neşat
        | عقل=akıl | ذهن=zihin | تفكير=tefekkür | سرور=sürur | سعادة=saadet
        | فيتامين=vitamin | هرمون=hormon | غذاء=gıda | ضعف=zaaf | قوة=kuvvet
        | عافية=afiyet | شفاء=şifa | سلامة=selamet | نقاهة=nekahat | جسم=cisim | بدن=beden""",
    40: """ظريف=zarif | ظرافة=zarafet | نادر=nadir | ندرة=nedret | عجيب=acayip | عجب=acep
        | غريب=garip | غرابة=garabet | أعجوبة=acube | حكاية=hikâye | قصة=kıssa
        | رواية=rivayet | خبر=haber | أخبار=ahbar | حادثة=hadise | حوادث=havadis
        | فرح=ferah | سرور=sürur | مِزاج=mizaç | مزاجي=mizaçlı | لطيف=Latif | لطافة=letafet
        | لطف=lütuf | ذكي=zeki | ذكاء=zekâ | حكمة=hikmet | فكرة=fikir | خيال=hayal
        | عقل=akıl | جنون=cinnet | مجنون=mecnun | حيرة=hayret | حيران=hayran
        | مجلس=meclis | صحبة=sohbet | محاورة=muhavere | مناقشة=münakaşa | أسلوب=üslup
        | عبارة=ibare | مثال=misal | خطاب=hitap | شعر=şiir | مقال=makal | تعبير=tabir
        | مجاز=mecaz""",
    41: """مساواة=müsavat | متساوٍ=müsavi | عدل=adalet | عدالة=adalet | عادل=adil | حق=hak
        | حقوق=hukuk | حقيقة=hakikat | حر=hür | حرية=hürriyet | ظلم=zulüm | ظالم=zalim
        | مظلوم=mazlum | قانون=kanun | قانوني=kanuni | دولة=devlet | حكومة=hükümet
        | شعب=şa'b | مواطن=vatandaş | أصل=asıl | نسب=nesep | شرف=şeref | كرامة=keramet
        | إنسان=insan | إنسانية=insaniyet | إنساني=insani | بشر=beşer | فقير=fakir
        | أمير=emir | سلطان=sultan | عبد=abd | حاكم=hâkim | محكوم=mahkûm | رئيس=reis
        | قوم=kavim | أمة=ümmet | إسلام=İslam | دين=din | تقوى=takva | فضل=fazl
        | فضيلة=fazilet | إنصاف=insaf | منصف=munsif | سلام=selam | اتفاق=ittifak
        | ميزان=mizan | قاعدة=kaide | مبدأ=mebde | مبادئ=mebadi | أساس=esas
        | ديمقراطية=demokrasi""",
    42: """حيوان=hayvan | حيواني=hayvani | رحمة=rahmet | رأفة=re'fet | رفيق=refik | رعاية=riayet
        | حماية=himaye | محمية=mahmi | حقوق=hukuk | حق=hak | عذاب=azap | ظلم=zulüm
        | غذاء=gıda | طعام=taam | ماء=ma | نبات=nebat | عسل=asel | نحلة=nahil | فيل=fil
        | غزال=gazal | زرافة=zürafa | نمر=nemr | عقرب=akrep | جرادة=cerade | حشرة=haşere
        | فلاح=fellah | زراعة=ziraat | طبيعة=tabiat | بيئة=biat | كائن=kâin
        | كائنات=kâinat | مخلوق=mahluk | مخلوقات=mahlukat | خالق=Hâlık | خَلْق=halk
        | فطرة=fıtrat | غريزة=garize | ذنب=zenb | ثواب=sevap | صدقة=sadaka | أخلاق=ahlak
        | أدب=edep""",
    43: """مثال=misal | حكمة=hikmet | حكيم=hakim | عبارة=ibare | معنى=mana | لفظ=lafız
        | أسلوب=üslup | بلاغة=belagat | بليغ=beliğ | فصاحة=fesahat | مجاز=mecaz
        | تشبيه=teşbih | تعبير=tabir | كلمة=kelime | جملة=cümle | شعر=şiir | بيت شعر=beyit
        | قافية=kafiye | أدب=edep | أدبيات=edebiyat | لغة=lügat | لسان=lisan | لهجة=lehçe
        | عربي=Arap | تجربة=tecrübe | خبرة=hibre | عقل=akıl | فكر=fikir | نصيحة=nasihat
        | توصية=tavsiye | ذكي=zeki | ذكاء=zekâ | صبر=sabır | صدْق=sıdk | عدل=adalet
        | قناعة=kanaat | كرم=kerem | حسرة=hasret | أصل=asıl | تاريخ=tarih | قديم=kadim
        | ماضي=mazi | رواية=rivayet | حكاية=hikâye""",
    44: """زوج=zevç | زوجة=zevce | نزاع=niza | خلاف=hilaf | اختلاف=ihtilaf | خصومة=husumet
        | عناد=inat | غضب=gazap | غم=gam | حزن=hüzün | كدر=keder | صبر=sabır
        | إصلاح=ıslah | رضا=rıza | حب=hubb | محبة=muhabbet | وفاء=vefa | عشق=aşk
        | عاشق=âşık | قلب=kalp | احترام=ihtiram | حرمة=hürmet | عفة=iffet | خيانة=hıyanet
        | خائن=hain | ظلم=zulüm | عدل=adalet | حق=hak | حقوق=hukuk | نصيحة=nasihat
        | مشكل=müşkül | صعوبة=müşkülat | صعب=sa'b | سهل=sehl | اتفاق=ittifak
        | محكمة=mahkeme | دعوى=dava | قانون=kanun | شريعة=şeriat | شرعي=şer'i
        | عائلة=aile | أهل=ehil | طفل=tıfıl | يتيم=yetim""",
    45: """أب=eb | والد=valide | والدة=valide | أهل=ehil | عائلة=aile | طفل=tıfıl | يتيم=yetim
        | تربية=terbiye | تعليم=talim | أدب=edep | احترام=ihtiram | حرمة=hürmet
        | رحمة=rahmet | حنان=hanan | رأفة=re'fet | محبة=muhabbet | حب=hubb
        | نصيحة=nasihat | توجيه=tevcih | شباب=şebap | عمر=ömür | نسل=nesil
        | عجوز=acuze | بالغ=baliğ | ميراث=miras | وراثي=irsi | وصي=vasi | كرامة=keramet
        | عزيز=aziz | صداقة=sadakat | صديق=sadık | محاورة=muhavere | محاضرة=muhazara
        | مناقشة=münakaşa | خلاف=hilaf | اختلاف=ihtilaf | صبر=sabır | حكمة=hikmet""",
    46: """ماء=ma | بحر=bahir | بحيرة=bahire | نهر=nehir | وادي=vadi | ساحل=sahil | شاطئ=şat
        | جزيرة=cezire | طوفان=tufan | فيضان=feyezan | بخار=buhar | هيدروجين=hidrojen
        | أكسجين=oksijen | نبات=nebat | زراعة=ziraat | زراعي=zirai | محصول=mahsul
        | غذاء=gıda | حياة=hayat | حيّ=hayy | طين=tin | تراب=turap | صحراء=sahra | أرض=arz
        | حوض=havuz | إبريق=ibrik | شراب=şarap | شربات=şerbet | صحة=sıhhat | نقي=naki
        | نقاء=neka | صافي=safi | طاهر=tahir | معدن=maden | ملح=melh | كيمياء=kimya
        | حرارة=hararet | برودة=berudet | برد=berd | حجم=hacim | كمية=kemiyet
        | قياس=kıyas | أصل=asıl | بيئة=biat | طاقة=takat | حيوان=hayvan""",
    47: """وصي=vasi | وصاية=vesayet | توصية=tavsiye | نصيحة=nasihat | أب=eb | والد=valide
        | والدة=valide | طفل=tıfıl | أخلاق=ahlak | أدب=edep | آداب=edep | تقوى=takva
        | إيمان=iman | صلاة=salat | صدْق=sıdk | أمانة=emanet | أمين=emin | عدل=adalet
        | صبر=sabır | حكمة=hikmet | قناعة=kanaat | كرم=kerem | شكر=şükür | حياء=haya
        | عفة=iffet | شرف=şeref | كرامة=keramet | احترام=ihtiram | علم=ilim | عمل=amel
        | خبرة=hibre | تجربة=tecrübe | مال=mal | ميراث=miras | ورثة=verese | وريث=varis
        | عهد=ahit | وعد=vait | وفاء=vefa | خدمة=hizmet | رحمة=rahmet | مغفرة=mağfiret
        | توبة=tövbe | ذنب=zenb""",
    48: """يوم=yevm | يومية=yevmiye | ساعة=saat | دقيقة=dakika | زمان=zaman | تاريخ=tarih
        | تقويم=takvim | أسبوع=usbu | مدرسة=medrese | جامعة=camia | طالب=talebe
        | معلم=muallim | صديق=sadık | عائلة=aile | أهل=ehil | سفر=sefer | سيارة=seyyare
        | حافلة=kafile | تلفون=telefon | كمبيوتر=kompüter | إنترنت=internet | كتاب=kitap
        | مجلة=mecmua | صحيفة=sahife | فيلم=film | تلفزيون=televizyon | موسيقى=musiki
        | طعام=taam | قهوة=kahve | شاي=çay | حلوى=helva | مسجد=mescit | صلاة=salat
        | عيد=ıyd | مذكرة=tezkere | ذكرى=tezkire | خاطرة=hatıra | خاطر=hatır
        | حكاية=hikâye | قصة=kıssa | كتابة=kitabet | خط=hat | ورقة=varak | دفتر=defter""",
}


def _lookup():
    by_pair = {}
    for word in all_words():
        by_pair.setdefault((word["ar"], word["tr"]), word)
    return by_pair


def _build():
    by_pair = _lookup()
    units = {}
    for number, text in _UNIT_PAIRS.items():
        words, seen = [], set()
        for entry in text.split("|"):
            ar, _, tr = (part.strip() for part in entry.partition("="))
            if (ar, tr) not in by_pair:
                raise ValueError(f"unit {number}: «{ar}={tr}» is not in content.shared_words")
            if (ar, tr) in seen:
                raise ValueError(f"unit {number}: «{ar}={tr}» is listed twice")
            seen.add((ar, tr))
            word = by_pair[(ar, tr)]
            words.append({
                "ar": word["ar"], "tr": word["tr"],
                "usage": word["usage"], "note": word["note"],
            })
        units[number] = words
    return units


UNIT_SHARED_WORDS = _build()
