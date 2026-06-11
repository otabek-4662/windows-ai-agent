# 🤖 Windows 11 AI Desktop Agent

**Kompyuteringizni matn orqali boshqaring!**

Bu dastur sizga Windows 11 kompyuteringizni chat orqali boshqarish imkonini beradi. O'zbek va ingliz tillarida buyruqlarni tushunadi.

---

## 📋 Imkoniyatlari

| # | Funksiya | Misol |
|---|----------|-------|
| 1 | Wallpaper o'zgartirish | `wallpaper C:\rasm.jpg` |
| 2 | Ovoz boshqarish | `ovozni 50% ga qo'y` |
| 3 | Yorqinlik boshqarish | `yorqinlik 70%` |
| 4 | Ilovalarni ochish | `chrome och` |
| 5 | Ilovalarni yopish | `telegram yop` |
| 6 | Fayllarni ochish | `fayl och C:\doc.pdf` |
| 7 | Papka ochish/yaratish | `papka yarat C:\yangi` |
| 8 | Skrinshot olish | `skrinshot ol` |
| 9 | Sayt ochish | `sayt och google.com` |
| 10 | Google qidirish | `google qidir python` |
| 11 | YouTube qidirish | `youtube qidir music` |
| 12 | Wi-Fi boshqarish | `wifi holati` |
| 13 | Tizim ma'lumoti | `tizim haqida` |
| 14 | Batareya holati | `batareya` |
| 15 | Vaqtni ko'rsatish | `soat nechchi` |
| 16 | Clipboard | `nusxala "matn"` |
| 17 | Axlat qutisi | `axlat qutisini bo'shat` |
| 18 | Ekranni qulflash | `ekranni qulfla` |
| 19 | Uxlash rejimi | `uxla` |
| 20 | Qayta ishga tushirish | `restart` |
| 21 | O'chirish | `kompyuterni o'chir` |

---

## 🚀 O'rnatish

### Talab qilinadigan dasturlar:

1. **Python 3.8+** — [python.org](https://python.org) dan yuklab oling
   - O'rnatishda **"Add Python to PATH"** ni albatta belgilang ✅

### O'rnatish qadamlari:

#### 1-usul: Avtomatik (tavsiya etiladi)

```
install.bat ni ikki marta bosing
```

#### 2-usul: Qo'lda

Terminal (CMD) ochib, quyidagilarni yozing:

```bash
cd windows-ai-agent
pip install -r requirements.txt
```

---

## ▶️ Ishga tushirish

#### 1-usul: Bat fayl orqali

```
start.bat ni ikki marta bosing
```

#### 2-usul: Terminalda

```bash
cd windows-ai-agent
python main.py
```

---

## 📖 Foydalanish

```
==================================================
   WINDOWS 11 AI DESKTOP AGENT
   Kompyuteringizni matn orqali boshqaring!
==================================================

🤖 Siz > notepad och
💬 Agent > 'notepad' ilovasi ochildi.

🤖 Siz > ovozni 30% ga qo'y
💬 Agent > Ovoz balandligi 30% ga o'rnatildi.

🤖 Siz > skrinshot ol
💬 Agent > Skrinshot saqlandi: C:\Users\...\Desktop\screenshot_20240101_120000.png

🤖 Siz > exit
💬 Agent > Xayr! Yaxshi kun tilerman! 👋
```

---

## 📂 Loyiha tuzilmasi

```
windows-ai-agent/
├── main.py              # Asosiy fayl (entry point)
├── system_controller.py # Tizimni boshqarish funksiyalari
├── command_parser.py    # Buyruqlarni tahlil qilish (NLP)
├── chat_interface.py    # Chat interfeysi
├── requirements.txt     # Kerakli kutubxonalar
├── install.bat          # Avtomatik o'rnatish
├── start.bat            # Tez ishga tushirish
└── README.md            # Hujjat (shu fayl)
```

---

## ⚙️ Texnik ma'lumotlar

| Texnologiya | Maqsadi |
|-------------|---------|
| Python 3.8+ | Asosiy dasturlash tili |
| pycaw | Windows ovoz boshqarish |
| screen-brightness-control | Yorqinlik boshqarish |
| Pillow | Skrinshot olish |
| psutil | Tizim ma'lumotlari |
| ctypes | Windows API bilan ishlash |
| subprocess | Tizim buyruqlarini bajarish |

---

## 🔧 Muammolarni hal qilish

### "Python topilmadi" xatosi
- Python'ni qayta o'rnating va **"Add to PATH"** ni belgilang
- Yoki to'liq yo'lni ko'rsating: `C:\Python312\python.exe main.py`

### "pycaw o'rnatilmadi" xatosi
```bash
pip install pycaw comtypes
```

### Ovoz ishlamayapti
- `pycaw` va `comtypes` o'rnatilganligini tekshiring
- Administrator sifatida ishga tushiring

### Yorqinlik ishlamayapti
- Bu funksiya faqat noutbuklarda ishlaydi
- Desktop kompyuterlarda monitor sozlamalari orqali o'zgartiring

---

## 🔒 Xavfsizlik

- **Fayl o'chirish** — tasdiqlash so'raydi
- **Kompyuter o'chirish** — 30 soniya kutish vaqti, bekor qilish mumkin
- **Restart** — 30 soniya kutish vaqti

---

## 📄 Litsenziya

Bu loyiha ochiq manba (open source) hisoblanadi.

---

**Savollar bo'lsa, dasturda `yordam` buyrug'ini yozing! 😊**
