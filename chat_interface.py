"""
Chat Interface Module
======================
Foydalanuvchi bilan muloqot qiluvchi interfeys.
Buyruqlarni qabul qiladi, tahlil qiladi va natijani ko'rsatadi.
"""

import datetime
from command_parser import CommandParser
from system_controller import SystemController


class ChatInterface:
    """Chat orqali kompyuterni boshqarish interfeysi"""

    def __init__(self):
        self.parser = CommandParser()
        self.controller = SystemController()
        self.history = []
        self.running = True

    def run(self):
        """Asosiy chat tsikli"""
        while self.running:
            try:
                user_input = input("\n🤖 Siz > ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ('exit', 'quit', 'chiqish', 'chiq', 'q'):
                    self._print_response("Xayr! Yaxshi kun tilerman! 👋")
                    self.running = False
                    break

                if user_input.lower() in ('tarix', 'history', 'tarixi'):
                    self._show_history()
                    continue

                parsed = self.parser.parse(user_input)

                self.history.append({
                    'time': datetime.datetime.now().strftime('%H:%M:%S'),
                    'input': user_input,
                    'action': parsed['action'],
                    'confidence': parsed['confidence']
                })

                result = self._execute_command(parsed)
                self._print_response(result)

            except KeyboardInterrupt:
                print("\n")
                self._print_response("Dastur to'xtatildi. Xayr! 👋")
                self.running = False
                break
            except EOFError:
                self.running = False
                break
            except Exception as e:
                self._print_response(f"Kutilmagan xato: {str(e)}")

    def _execute_command(self, parsed):
        """Tahlil qilingan buyruqni bajarish"""
        action = parsed['action']
        params = parsed['params']
        confidence = parsed['confidence']

        if action == 'unknown':
            return self._unknown_response(params.get('original_text', ''))

        if action == 'empty':
            return "Buyruq kiriting yoki 'yordam' deb yozing."

        if action == 'help':
            return self.parser.get_help_text()

        if confidence < 0.6:
            return (
                f"⚠️ Men buyruqni to'liq tushunmadim.\n"
                f"   Taxminim: '{action}'\n"
                f"   Ishonch darajasi: {int(confidence * 100)}%\n"
                f"   'yordam' deb yozing buyruqlar ro'yxatini ko'rish uchun."
            )

        # Wallpaper
        if action == 'set_wallpaper':
            path = params.get('path')
            if not path:
                return "⚠️ Rasm yo'lini ko'rsating. Masalan: wallpaper C:\\rasm.jpg"
            return self.controller.set_wallpaper(path)

        # Ovoz
        elif action == 'set_volume':
            level = params.get('level')
            if not level:
                return "⚠️ Ovoz darajasini ko'rsating. Masalan: ovozni 50% ga qo'y"
            return self.controller.set_volume(int(level))

        elif action == 'increase_volume':
            amount = int(params.get('amount', 10))
            return self.controller.increase_volume(amount)

        elif action == 'decrease_volume':
            amount = int(params.get('amount', 10))
            return self.controller.decrease_volume(amount)

        elif action == 'mute_volume':
            return self.controller.mute_volume()

        elif action == 'unmute_volume':
            return self.controller.unmute_volume()

        # Yorqinlik
        elif action == 'set_brightness':
            level = params.get('level')
            if not level:
                return "⚠️ Yorqinlik darajasini ko'rsating. Masalan: yorqinlik 70%"
            return self.controller.set_brightness(int(level))

        elif action == 'increase_brightness':
            amount = int(params.get('amount', 10))
            return self.controller.increase_brightness(amount)

        elif action == 'decrease_brightness':
            amount = int(params.get('amount', 10))
            return self.controller.decrease_brightness(amount)

        # Ilovalar
        elif action == 'open_app':
            app_name = params.get('app_name')
            if not app_name:
                return "⚠️ Ilova nomini ko'rsating. Masalan: notepad och"
            return self.controller.open_application(app_name)

        elif action == 'close_app':
            app_name = params.get('app_name')
            if not app_name:
                return "⚠️ Ilova nomini ko'rsating. Masalan: chrome yop"
            return self.controller.close_application(app_name)

        # Fayllar
        elif action == 'open_file':
            path = params.get('path')
            if not path:
                return "⚠️ Fayl yo'lini ko'rsating. Masalan: fayl och C:\\doc.pdf"
            return self.controller.open_file(path)

        elif action == 'open_folder':
            path = params.get('path')
            if not path:
                return "⚠️ Papka yo'lini ko'rsating. Masalan: papka och C:\\Users"
            return self.controller.open_folder(path)

        elif action == 'create_folder':
            path = params.get('path')
            if not path:
                return "⚠️ Papka yo'lini ko'rsating. Masalan: papka yarat C:\\yangi"
            return self.controller.create_folder(path)

        elif action == 'delete_file':
            path = params.get('path')
            if not path:
                return "⚠️ Fayl yo'lini ko'rsating. Masalan: fayl o'chir C:\\fayl.txt"
            return (
                f"⚠️ DIQQAT: '{path}' o'chiriladi!\n"
                f"   Tasdiqlash uchun: 'ha o'chir {path}'\n"
                f"   Bekor qilish uchun boshqa narsa yozing."
            )

        elif action == 'list_files':
            path = params.get('path')
            return self.controller.list_files(path)

        # Skrinshot
        elif action == 'screenshot':
            path = params.get('path')
            return self.controller.take_screenshot(path)

        # Tizim boshqarish
        elif action == 'shutdown':
            delay = int(params.get('delay', 30))
            return (
                f"⚠️ Kompyuter {delay} soniyadan keyin o'chadi!\n"
                f"   Bekor qilish uchun: 'o'chirishni bekor qil'\n"
                + self.controller.shutdown(delay)
            )

        elif action == 'restart':
            delay = int(params.get('delay', 30))
            return (
                f"⚠️ Kompyuter {delay} soniyadan keyin qayta ishga tushadi!\n"
                f"   Bekor qilish uchun: 'o'chirishni bekor qil'\n"
                + self.controller.restart(delay)
            )

        elif action == 'cancel_shutdown':
            return self.controller.cancel_shutdown()

        elif action == 'sleep':
            return self.controller.sleep()

        elif action == 'lock_screen':
            return self.controller.lock_screen()

        # Tizim ma'lumotlari
        elif action == 'system_info':
            return self.controller.get_system_info()

        elif action == 'battery_info':
            return self.controller.get_battery_info()

        elif action == 'time':
            return self.controller.get_time()

        elif action == 'processes':
            return self.controller.get_running_processes()

        # Tarmoq
        elif action == 'wifi_status':
            return self.controller.wifi_status()

        elif action == 'wifi_disconnect':
            return self.controller.wifi_disconnect()

        elif action == 'wifi_connect':
            network = params.get('network')
            if not network:
                return "⚠️ Tarmoq nomini ko'rsating. Masalan: wifi ulan MyNetwork"
            return self.controller.wifi_connect(network)

        # Web
        elif action == 'open_website':
            url = params.get('url')
            if not url:
                return "⚠️ Sayt manzilini ko'rsating. Masalan: sayt och google.com"
            return self.controller.open_website(url)

        elif action == 'search_google':
            query = params.get('query')
            if not query:
                return "⚠️ Qidiruv so'zini ko'rsating. Masalan: google qidir python"
            return self.controller.search_google(query)

        elif action == 'search_youtube':
            query = params.get('query')
            if not query:
                return "⚠️ Qidiruv so'zini ko'rsating. Masalan: youtube qidir music"
            return self.controller.search_youtube(query)

        # Clipboard
        elif action == 'copy_clipboard':
            text = params.get('text')
            if not text:
                return "⚠️ Nusxalanishi kerak bo'lgan matnni ko'rsating."
            return self.controller.copy_to_clipboard(text)

        elif action == 'get_clipboard':
            return self.controller.get_clipboard()

        # Boshqa
        elif action == 'empty_recycle_bin':
            return self.controller.empty_recycle_bin()

        else:
            return self._unknown_response(action)

    def _unknown_response(self, text):
        """Tushunib bo'lmagan buyruq uchun javob"""
        suggestions = [
            "Masalan:",
            "  • 'notepad och' - ilovani ochish",
            "  • 'ovozni 50%' - ovoz balandligi",
            "  • 'yorqinlik 70%' - ekran yorqinligi",
            "  • 'skrinshot ol' - ekran surati",
            "  • 'yordam' - barcha buyruqlar ro'yxati",
        ]
        return (
            f"❓ Kechirasiz, '{text}' buyrug'ini tushunmadim.\n\n"
            + "\n".join(suggestions)
        )

    def _print_response(self, message):
        """Javobni chiroyli formatda chiqarish"""
        print(f"\n💬 Agent > {message}")

    def _show_history(self):
        """Buyruqlar tarixini ko'rsatish"""
        if not self.history:
            self._print_response("Tarix bo'sh. Hali hech qanday buyruq berilmagan.")
            return

        result = "📜 BUYRUQLAR TARIXI:\n"
        result += "━" * 40 + "\n"
        for i, item in enumerate(self.history[-20:], 1):
            status = "✅" if item['confidence'] >= 0.6 else "⚠️"
            result += (
                f"  {status} [{item['time']}] {item['input']}\n"
                f"     → {item['action']} (ishonch: {int(item['confidence'] * 100)}%)\n"
            )
        result += "━" * 40

        self._print_response(result)
