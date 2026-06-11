@echo off
echo ============================================
echo   WINDOWS 11 AI AGENT - O'RNATISH
echo ============================================
echo.

REM Python mavjudligini tekshirish
python --version >nul 2>&1
if errorlevel 1 (
    echo [XATO] Python topilmadi!
    echo Python'ni https://python.org saytidan yuklab o'rnating.
    echo O'rnatishda "Add Python to PATH" ni belgilang!
    echo.
    pause
    exit /b 1
)

echo [OK] Python topildi:
python --version
echo.

REM pip yangilash
echo [1/2] pip yangilanmoqda...
python -m pip install --upgrade pip
echo.

REM Kutubxonalarni o'rnatish
echo [2/2] Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt
echo.

echo ============================================
echo   O'RNATISH MUVAFFAQIYATLI YAKUNLANDI!
echo ============================================
echo.
echo Dasturni ishga tushirish uchun:
echo   python main.py
echo.
pause
