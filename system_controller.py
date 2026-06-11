"""
System Controller Module
========================
Windows 11 tizimini boshqarish uchun barcha funksiyalar.

Imkoniyatlari:
- Wallpaper o'zgartirish
- Ovoz balandligini boshqarish (oshirish, kamaytirish, o'chirish)
- Yorqinlikni boshqarish
- Ilovalarni ochish va yopish
- Fayllarni ochish
- Skrinshot olish
- Tizim ma'lumotlari
- Kompyuterni o'chirish/restart/uxlash
- Wi-Fi boshqarish
- Papka ochish
- Clipboard boshqarish
"""

import subprocess
import os
import sys
import ctypes
import datetime
import platform
import shutil


class SystemController:
    """Windows 11 tizimini boshqaruvchi asosiy klass"""

    def __init__(self):
        self.is_windows = platform.system() == "Windows"

    # ==========================================
    # WALLPAPER
    # ==========================================

    def set_wallpaper(self, image_path):
        """Wallpaperni o'zgartirish"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        if not os.path.exists(image_path):
            return f"Xato: Fayl topilmadi - {image_path}"

        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff')
        if not image_path.lower().endswith(valid_extensions):
            return f"Xato: Fayl rasm formatida emas. Qo'llab-quvvatlanadigan formatlar: {valid_extensions}"

        try:
            SPI_SETDESKWALLPAPER = 0x0014
            SPIF_UPDATEINIFILE = 0x01
            SPIF_SENDCHANGE = 0x02

            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, image_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )

            if result:
                return f"Wallpaper muvaffaqiyatli o'zgartirildi: {image_path}"
            else:
                return "Xato: Wallpaperni o'zgartirib bo'lmadi."
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # OVOZ BOSHQARISH (VOLUME)
    # ==========================================

    def set_volume(self, level):
        """Ovoz balandligini foizda o'rnatish (0-100)"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            level = max(0, min(100, level))
            scalar_volume = level / 100.0
            volume.SetMasterVolumeLevelScalar(scalar_volume, None)

            return f"Ovoz balandligi {level}% ga o'rnatildi."
        except ImportError:
            try:
                vol_level = int(level * 655.35)
                subprocess.run(['nircmd', 'setsysvolume', str(vol_level)], capture_output=True)
                return f"Ovoz balandligi {level}% ga o'rnatildi."
            except FileNotFoundError:
                return "Xato: Ovoz boshqarish uchun 'pycaw' kutubxonasi kerak. 'pip install pycaw' buyrug'ini ishga tushiring."

    def mute_volume(self):
        """Ovozni o'chirish (mute)"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)

            return "Ovoz o'chirildi (mute)."
        except ImportError:
            try:
                subprocess.run(['nircmd', 'mutesysvolume', '1'], capture_output=True)
                return "Ovoz o'chirildi (mute)."
            except FileNotFoundError:
                return "Xato: 'pycaw' kutubxonasi kerak."

    def unmute_volume(self):
        """Ovozni yoqish (unmute)"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(0, None)

            return "Ovoz yoqildi (unmute)."
        except ImportError:
            try:
                subprocess.run(['nircmd', 'mutesysvolume', '0'], capture_output=True)
                return "Ovoz yoqildi (unmute)."
            except FileNotFoundError:
                return "Xato: 'pycaw' kutubxonasi kerak."

    def increase_volume(self, amount=10):
        """Ovozni oshirish"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            current = volume.GetMasterVolumeLevelScalar()
            new_level = min(1.0, current + amount / 100.0)
            volume.SetMasterVolumeLevelScalar(new_level, None)

            return f"Ovoz oshirildi: {int(new_level * 100)}%"
        except ImportError:
            return "Xato: 'pycaw' kutubxonasi kerak."

    def decrease_volume(self, amount=10):
        """Ovozni kamaytirish"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        try:
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            from comtypes import CLSCTX_ALL
            from ctypes import cast, POINTER

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))

            current = volume.GetMasterVolumeLevelScalar()
            new_level = max(0.0, current - amount / 100.0)
            volume.SetMasterVolumeLevelScalar(new_level, None)

            return f"Ovoz kamaytirildi: {int(new_level * 100)}%"
        except ImportError:
            return "Xato: 'pycaw' kutubxonasi kerak."

    # ==========================================
    # YORQINLIK (BRIGHTNESS)
    # ==========================================

    def set_brightness(self, level):
        """Yorqinlikni o'rnatish (0-100)"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        level = max(0, min(100, level))

        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return f"Yorqinlik {level}% ga o'rnatildi."
        except ImportError:
            try:
                subprocess.run(
                    ['powershell', '-Command',
                     f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})'],
                    capture_output=True
                )
                return f"Yorqinlik {level}% ga o'rnatildi."
            except Exception as e:
                return f"Xato: {str(e)}"

    def increase_brightness(self, amount=10):
        """Yorqinlikni oshirish"""
        try:
            import screen_brightness_control as sbc
            current = sbc.get_brightness()[0]
            new_level = min(100, current + amount)
            sbc.set_brightness(new_level)
            return f"Yorqinlik oshirildi: {new_level}%"
        except ImportError:
            try:
                result = subprocess.run(
                    ['powershell', '-Command',
                     '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'],
                    capture_output=True, text=True
                )
                current = int(result.stdout.strip())
                new_level = min(100, current + amount)
                subprocess.run(
                    ['powershell', '-Command',
                     f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_level})'],
                    capture_output=True
                )
                return f"Yorqinlik oshirildi: {new_level}%"
            except Exception as e:
                return f"Xato: {str(e)}"

    def decrease_brightness(self, amount=10):
        """Yorqinlikni kamaytirish"""
        try:
            import screen_brightness_control as sbc
            current = sbc.get_brightness()[0]
            new_level = max(0, current - amount)
            sbc.set_brightness(new_level)
            return f"Yorqinlik kamaytirildi: {new_level}%"
        except ImportError:
            try:
                result = subprocess.run(
                    ['powershell', '-Command',
                     '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness'],
                    capture_output=True, text=True
                )
                current = int(result.stdout.strip())
                new_level = max(0, current - amount)
                subprocess.run(
                    ['powershell', '-Command',
                     f'(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_level})'],
                    capture_output=True
                )
                return f"Yorqinlik kamaytirildi: {new_level}%"
            except Exception as e:
                return f"Xato: {str(e)}"

    # ==========================================
    # ILOVALAR (APPLICATIONS)
    # ==========================================

    def open_application(self, app_name):
        """Ilovani ochish"""
        app_map = {
            'notepad': 'notepad.exe',
            'bloknot': 'notepad.exe',
            'calculator': 'calc.exe',
            'kalkulyator': 'calc.exe',
            'paint': 'mspaint.exe',
            'cmd': 'cmd.exe',
            'terminal': 'wt.exe',
            'powershell': 'powershell.exe',
            'explorer': 'explorer.exe',
            'fayl menejeri': 'explorer.exe',
            'task manager': 'taskmgr.exe',
            'sozlamalar': 'ms-settings:',
            'settings': 'ms-settings:',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'brave': 'brave.exe',
            'opera': 'opera.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'outlook': 'outlook.exe',
            'onenote': 'onenote.exe',
            'vscode': 'code',
            'code': 'code',
            'visual studio code': 'code',
            'pycharm': 'pycharm64.exe',
            'intellij': 'idea64.exe',
            'telegram': 'telegram.exe',
            'discord': 'discord.exe',
            'zoom': 'zoom.exe',
            'teams': 'teams.exe',
            'skype': 'skype.exe',
            'spotify': 'spotify.exe',
            'vlc': 'vlc.exe',
            'steam': 'steam.exe',
            'epic games': 'EpicGamesLauncher.exe',
        }

        app_lower = app_name.lower().strip()

        try:
            if app_lower in app_map:
                target = app_map[app_lower]
                if target.startswith('ms-'):
                    os.startfile(target) if self.is_windows else subprocess.Popen(['xdg-open', target])
                else:
                    subprocess.Popen(target, shell=True)
                return f"'{app_name}' ilovasi ochildi."
            else:
                subprocess.Popen(app_name, shell=True)
                return f"'{app_name}' ishga tushirildi."
        except FileNotFoundError:
            return f"Xato: '{app_name}' topilmadi. Ilova nomi yoki yo'li noto'g'ri bo'lishi mumkin."
        except Exception as e:
            return f"Xato: {str(e)}"

    def close_application(self, app_name):
        """Ilovani yopish"""
        if not self.is_windows:
            return "Bu funksiya faqat Windows'da ishlaydi."

        process_map = {
            'notepad': 'notepad.exe',
            'bloknot': 'notepad.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'vscode': 'code.exe',
            'code': 'code.exe',
            'telegram': 'telegram.exe',
            'discord': 'discord.exe',
            'spotify': 'spotify.exe',
            'vlc': 'vlc.exe',
            'paint': 'mspaint.exe',
            'calculator': 'calculator.exe',
            'kalkulyator': 'calculator.exe',
            'steam': 'steam.exe',
            'zoom': 'zoom.exe',
            'teams': 'teams.exe',
            'explorer': 'explorer.exe',
        }

        app_lower = app_name.lower().strip()
        process_name = process_map.get(app_lower, f"{app_lower}.exe")

        try:
            result = subprocess.run(
                ['taskkill', '/IM', process_name, '/F'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"'{app_name}' ilovasi yopildi."
            else:
                return f"'{app_name}' topilmadi yoki allaqachon yopilgan."
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # FAYLLAR
    # ==========================================

    def open_file(self, file_path):
        """Faylni standart dastur bilan ochish"""
        if not os.path.exists(file_path):
            return f"Xato: Fayl topilmadi - {file_path}"

        try:
            if self.is_windows:
                os.startfile(file_path)
            else:
                subprocess.Popen(['xdg-open', file_path])
            return f"Fayl ochildi: {file_path}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def open_folder(self, folder_path):
        """Papkani Explorer'da ochish"""
        if not os.path.exists(folder_path):
            return f"Xato: Papka topilmadi - {folder_path}"

        try:
            if self.is_windows:
                subprocess.Popen(['explorer', folder_path])
            else:
                subprocess.Popen(['xdg-open', folder_path])
            return f"Papka ochildi: {folder_path}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def create_folder(self, folder_path):
        """Yangi papka yaratish"""
        try:
            os.makedirs(folder_path, exist_ok=True)
            return f"Papka yaratildi: {folder_path}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def delete_file(self, file_path):
        """Faylni o'chirish"""
        if not os.path.exists(file_path):
            return f"Xato: Fayl topilmadi - {file_path}"

        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                return f"Papka o'chirildi: {file_path}"
            else:
                os.remove(file_path)
                return f"Fayl o'chirildi: {file_path}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def list_files(self, folder_path=None):
        """Papkadagi fayllar ro'yxati"""
        if folder_path is None:
            folder_path = os.path.expanduser("~\\Desktop")

        if not os.path.exists(folder_path):
            return f"Xato: Papka topilmadi - {folder_path}"

        try:
            files = os.listdir(folder_path)
            if not files:
                return f"Papka bo'sh: {folder_path}"

            result = f"📁 {folder_path} ichidagi fayllar:\n"
            for f in sorted(files):
                full_path = os.path.join(folder_path, f)
                if os.path.isdir(full_path):
                    result += f"  📁 {f}/\n"
                else:
                    size = os.path.getsize(full_path)
                    result += f"  📄 {f} ({self._format_size(size)})\n"
            return result
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # SKRINSHOT
    # ==========================================

    def take_screenshot(self, save_path=None):
        """Skrinshot olish"""
        if save_path is None:
            desktop = os.path.expanduser("~\\Desktop")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(desktop, f"screenshot_{timestamp}.png")

        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            screenshot.save(save_path)
            return f"Skrinshot saqlandi: {save_path}"
        except ImportError:
            try:
                ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object {{
    $bitmap = New-Object System.Drawing.Bitmap($_.Bounds.Width, $_.Bounds.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($_.Bounds.Location, [System.Drawing.Point]::Empty, $_.Bounds.Size)
    $bitmap.Save('{save_path}')
}}
"""
                subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
                return f"Skrinshot saqlandi: {save_path}"
            except Exception as e:
                return f"Xato: {str(e)}"

    # ==========================================
    # TIZIM BOSHQARISH
    # ==========================================

    def shutdown(self, delay=0):
        """Kompyuterni o'chirish"""
        try:
            subprocess.run(['shutdown', '/s', '/t', str(delay)], capture_output=True)
            return f"Kompyuter {delay} soniyadan keyin o'chadi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def restart(self, delay=0):
        """Kompyuterni qayta ishga tushirish"""
        try:
            subprocess.run(['shutdown', '/r', '/t', str(delay)], capture_output=True)
            return f"Kompyuter {delay} soniyadan keyin qayta ishga tushadi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def cancel_shutdown(self):
        """O'chirishni bekor qilish"""
        try:
            subprocess.run(['shutdown', '/a'], capture_output=True)
            return "O'chirish bekor qilindi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def sleep(self):
        """Kompyuterni uxlash rejimiga o'tkazish"""
        try:
            subprocess.run(
                ['powershell', '-Command',
                 'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState("Suspend", $false, $false)'],
                capture_output=True
            )
            return "Kompyuter uxlash rejimiga o'tdi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def lock_screen(self):
        """Ekranni qulflash"""
        try:
            ctypes.windll.user32.LockWorkStation()
            return "Ekran quflandi."
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # TIZIM MA'LUMOTLARI
    # ==========================================

    def get_system_info(self):
        """Tizim haqida ma'lumot"""
        try:
            info = f"""
💻 TIZIM MA'LUMOTLARI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Kompyuter nomi: {platform.node()}
  OS: {platform.system()} {platform.release()}
  Versiya: {platform.version()}
  Arxitektura: {platform.machine()}
  Protsessor: {platform.processor()}
  Python versiyasi: {platform.python_version()}
"""
            if self.is_windows:
                total, used, free = shutil.disk_usage("C:\\")
                info += f"""
  💾 Disk (C:):
     Jami: {self._format_size(total)}
     Ishlatilgan: {self._format_size(used)}
     Bo'sh: {self._format_size(free)}
"""
            return info
        except Exception as e:
            return f"Xato: {str(e)}"

    def get_battery_info(self):
        """Batareya haqida ma'lumot"""
        try:
            import psutil
            battery = psutil.sensors_battery()
            if battery:
                status = "Quvvat olmoqda" if battery.power_plugged else "Batareyada"
                return f"🔋 Batareya: {battery.percent}% | {status}"
            else:
                return "Batareya topilmadi (stasionar kompyuter)."
        except ImportError:
            try:
                result = subprocess.run(
                    ['powershell', '-Command',
                     '(Get-WmiObject Win32_Battery).EstimatedChargeRemaining'],
                    capture_output=True, text=True
                )
                if result.stdout.strip():
                    return f"🔋 Batareya: {result.stdout.strip()}%"
                else:
                    return "Batareya ma'lumoti mavjud emas."
            except Exception as e:
                return f"Xato: {str(e)}"

    # ==========================================
    # TARMOQ (NETWORK)
    # ==========================================

    def wifi_status(self):
        """Wi-Fi holatini ko'rish"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'interfaces'],
                capture_output=True, text=True, encoding='utf-8'
            )
            if result.returncode == 0:
                return f"📶 Wi-Fi holati:\n{result.stdout}"
            else:
                return "Wi-Fi ma'lumotini olishda xato."
        except Exception as e:
            return f"Xato: {str(e)}"

    def wifi_disconnect(self):
        """Wi-Fi'ni uzish"""
        try:
            subprocess.run(['netsh', 'wlan', 'disconnect'], capture_output=True)
            return "Wi-Fi uzildi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def wifi_connect(self, network_name):
        """Wi-Fi'ga ulanish"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'connect', f'name={network_name}'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"'{network_name}' tarmog'iga ulandi."
            else:
                return f"'{network_name}' tarmog'iga ulanib bo'lmadi."
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # CLIPBOARD
    # ==========================================

    def copy_to_clipboard(self, text):
        """Matnni clipboard'ga nusxalash"""
        try:
            subprocess.run(['clip'], input=text.encode('utf-16le'), check=True)
            return "Matn clipboard'ga nusxalandi."
        except Exception as e:
            return f"Xato: {str(e)}"

    def get_clipboard(self):
        """Clipboard'dagi matnni olish"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-Clipboard'],
                capture_output=True, text=True
            )
            content = result.stdout.strip()
            if content:
                return f"📋 Clipboard: {content}"
            else:
                return "Clipboard bo'sh."
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # WEB
    # ==========================================

    def open_website(self, url):
        """Websaytni brauzerda ochish"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            import webbrowser
            webbrowser.open(url)
            return f"Sayt ochildi: {url}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def search_google(self, query):
        """Google'da qidirish"""
        import urllib.parse
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        try:
            import webbrowser
            webbrowser.open(url)
            return f"Google'da qidirilmoqda: {query}"
        except Exception as e:
            return f"Xato: {str(e)}"

    def search_youtube(self, query):
        """YouTube'da qidirish"""
        import urllib.parse
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        try:
            import webbrowser
            webbrowser.open(url)
            return f"YouTube'da qidirilmoqda: {query}"
        except Exception as e:
            return f"Xato: {str(e)}"

    # ==========================================
    # YORDAMCHI FUNKSIYALAR
    # ==========================================

    def _format_size(self, size_bytes):
        """Bayt hajmini o'qiladigan formatga o'tkazish"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.1f} MB"
        else:
            return f"{size_bytes / (1024 ** 3):.1f} GB"

    def get_time(self):
        """Hozirgi vaqtni ko'rsatish"""
        now = datetime.datetime.now()
        return f"🕐 Hozirgi vaqt: {now.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_running_processes(self):
        """Ishlab turgan jarayonlar ro'yxati"""
        try:
            result = subprocess.run(
                ['tasklist', '/FO', 'TABLE', '/NH'],
                capture_output=True, text=True, encoding='utf-8'
            )
            lines = result.stdout.strip().split('\n')[:20]
            return "📊 Ishlab turgan jarayonlar (top 20):\n" + "\n".join(lines)
        except Exception as e:
            return f"Xato: {str(e)}"

    def empty_recycle_bin(self):
        """Axlat qutisini bo'shatish"""
        try:
            subprocess.run(
                ['powershell', '-Command',
                 'Clear-RecycleBin -Force -ErrorAction SilentlyContinue'],
                capture_output=True
            )
            return "🗑️ Axlat qutisi bo'shatildi."
        except Exception as e:
            return f"Xato: {str(e)}"
