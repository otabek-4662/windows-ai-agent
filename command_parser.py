"""
Command Parser Module (AI Buyruq Tahlilchisi)
==============================================
Foydalanuvchi matnini tahlil qilib, tegishli buyruqni aniqlaydi.

Bu modul o'zbek va ingliz tillarida yozilgan buyruqlarni tushunadi.
Oddiy keyword-based matching + fuzzy matching ishlatiladi.
"""

import re
from difflib import SequenceMatcher


class CommandParser:
    """Foydalanuvchi buyruqlarini tahlil qiluvchi klass"""

    def __init__(self):
        self.command_patterns = self._build_patterns()

    def parse(self, user_input):
        """
        Foydalanuvchi kiritgan matnni tahlil qilish.

        Returns:
            dict: {
                'action': str,
                'params': dict,
                'confidence': float
            }
        """
        text = user_input.lower().strip()

        if not text:
            return {'action': 'empty', 'params': {}, 'confidence': 1.0}

        # 1. Aniq buyruqlarni tekshirish
        result = self._match_exact(text)
        if result and result['confidence'] >= 0.8:
            return result

        # 2. Pattern matching (regex)
        result = self._match_pattern(text)
        if result and result['confidence'] >= 0.6:
            return result

        # 3. Fuzzy matching
        result = self._match_fuzzy(text)
        if result and result['confidence'] >= 0.5:
            return result

        # 4. Tushunib bo'lmadi
        return {
            'action': 'unknown',
            'params': {'original_text': user_input},
            'confidence': 0.0
        }

    def _build_patterns(self):
        """Buyruq shablonlarini yaratish"""
        patterns = {
            # ===== WALLPAPER =====
            'set_wallpaper': {
                'keywords': [
                    'wallpaper', 'fon rasm', 'orqa fon',
                    'wallpaperni o\'zgartir', 'fon o\'zgartir',
                    'background', 'rasm qo\'y'
                ],
                'regex': [
                    r'wallpaper.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'fon.*?rasm.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'wallpaper.*?\"(.+?)\"',
                    r'fon.*?\"(.+?)\"',
                ],
                'extract_param': 'path'
            },

            # ===== OVOZ (VOLUME) =====
            'set_volume': {
                'keywords': [
                    'ovoz', 'volume', 'tovush', 'sound',
                    'ovozni.*?%', 'volume.*?%'
                ],
                'regex': [
                    r'ovoz.*?(\d+)\s*%',
                    r'volume.*?(\d+)\s*%',
                    r'ovozni\s+(\d+)',
                    r'tovush.*?(\d+)',
                    r'sound.*?(\d+)',
                ],
                'extract_param': 'level'
            },
            'increase_volume': {
                'keywords': [
                    'ovozni oshir', 'ovoz oshir', 'balandroq',
                    'volume up', 'ovozni ko\'tar', 'ovozni kattalashtir',
                    'tovushni oshir', 'ovozni baland'
                ],
                'regex': [
                    r'ovoz.*?oshir.*?(\d+)',
                    r'ovoz.*?ko\'tar.*?(\d+)',
                ],
                'extract_param': 'amount'
            },
            'decrease_volume': {
                'keywords': [
                    'ovozni pasaytir', 'ovoz pasaytir', 'pastroq',
                    'volume down', 'ovozni kamaytir', 'ovozni kichiklashtir',
                    'tovushni pasaytir', 'ovozni past'
                ],
                'regex': [
                    r'ovoz.*?pasaytir.*?(\d+)',
                    r'ovoz.*?kamaytir.*?(\d+)',
                ],
                'extract_param': 'amount'
            },
            'mute_volume': {
                'keywords': [
                    'ovozni o\'chir', 'mute', 'tovushni o\'chir',
                    'ovoz o\'chir', 'jim bo\'l', 'sound off',
                    'ovozsiz', 'ovozni yop'
                ],
                'regex': [],
                'extract_param': None
            },
            'unmute_volume': {
                'keywords': [
                    'ovozni yoq', 'unmute', 'tovushni yoq',
                    'ovoz yoq', 'sound on', 'ovozni och'
                ],
                'regex': [],
                'extract_param': None
            },

            # ===== YORQINLIK (BRIGHTNESS) =====
            'set_brightness': {
                'keywords': [
                    'yorqinlik', 'brightness', 'ekran yorug\'ligi',
                    'yorqinlikni.*?%'
                ],
                'regex': [
                    r'yorqinlik.*?(\d+)\s*%',
                    r'brightness.*?(\d+)\s*%',
                    r'yorqinlikni\s+(\d+)',
                    r'yorqinlik.*?(\d+)',
                ],
                'extract_param': 'level'
            },
            'increase_brightness': {
                'keywords': [
                    'yorqinlikni oshir', 'yorqinlik oshir',
                    'ekranni yorug\'roq', 'brightness up',
                    'yorug\'roq', 'yorqinlikni ko\'tar'
                ],
                'regex': [
                    r'yorqinlik.*?oshir.*?(\d+)',
                ],
                'extract_param': 'amount'
            },
            'decrease_brightness': {
                'keywords': [
                    'yorqinlikni kamaytir', 'yorqinlik kamaytir',
                    'ekranni qoraytir', 'brightness down',
                    'qorong\'iroq', 'yorqinlikni pasaytir'
                ],
                'regex': [
                    r'yorqinlik.*?kamaytir.*?(\d+)',
                    r'yorqinlik.*?pasaytir.*?(\d+)',
                ],
                'extract_param': 'amount'
            },

            # ===== ILOVALAR =====
            'open_app': {
                'keywords': [
                    'och', 'open', 'ishga tushir', 'run',
                    'launch', 'start', 'ochib ber', 'yoq'
                ],
                'regex': [
                    r'(?:och|open|ishga tushir|run|launch|start|ochib ber|yoq)(?:ib ber)?\s+(.+)',
                    r'(.+?)\s+(?:och|open|ochib ber)',
                    r'(.+?)(?:ni|ni\s+)och',
                ],
                'extract_param': 'app_name'
            },
            'close_app': {
                'keywords': [
                    'yop', 'close', 'o\'chir', 'kil', 'stop',
                    'yopib ber', 'to\'xtat'
                ],
                'regex': [
                    r'(?:yop|close|o\'chir|stop|yopib ber|to\'xtat)\s+(.+)',
                    r'(.+?)\s+(?:yop|close|o\'chir)',
                    r'(.+?)(?:ni|ni\s+)yop',
                ],
                'extract_param': 'app_name'
            },

            # ===== FAYLLAR =====
            'open_file': {
                'keywords': [
                    'fayl och', 'file open', 'faylni och'
                ],
                'regex': [
                    r'fayl.*?och.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'fayl.*?och.*?\"(.+?)\"',
                    r'och.*?([a-zA-Z]:\\[^\s]+\.\w+)',
                ],
                'extract_param': 'path'
            },
            'open_folder': {
                'keywords': [
                    'papka och', 'folder open', 'papkani och'
                ],
                'regex': [
                    r'papka.*?och.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'papka.*?och.*?\"(.+?)\"',
                ],
                'extract_param': 'path'
            },
            'create_folder': {
                'keywords': [
                    'papka yarat', 'folder create', 'yangi papka',
                    'papka qil'
                ],
                'regex': [
                    r'papka.*?yarat.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'papka.*?yarat.*?\"(.+?)\"',
                ],
                'extract_param': 'path'
            },
            'delete_file': {
                'keywords': [
                    'fayl o\'chir', 'file delete', 'faylni o\'chir',
                    'o\'chirib tashla'
                ],
                'regex': [
                    r'(?:fayl|file).*?o\'chir.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                    r'o\'chir.*?([a-zA-Z]:\\[^\s]+)',
                ],
                'extract_param': 'path'
            },
            'list_files': {
                'keywords': [
                    'fayllar ro\'yxati', 'fayl ko\'rsat', 'list files',
                    'papka ichida nima bor', 'fayllarni ko\'rsat'
                ],
                'regex': [
                    r'fayllar.*?([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)',
                ],
                'extract_param': 'path'
            },

            # ===== SKRINSHOT =====
            'screenshot': {
                'keywords': [
                    'skrinshot', 'screenshot', 'ekranni sura',
                    'ekran rasmi', 'surat ol', 'skrinshot ol'
                ],
                'regex': [
                    r'skrinshot.*?([a-zA-Z]:\\[^\s]+)',
                ],
                'extract_param': 'path'
            },

            # ===== TIZIM BOSHQARISH =====
            'shutdown': {
                'keywords': [
                    'kompyuterni o\'chir', 'shutdown', 'o\'chir kompyuter',
                    'shut down', 'tizimni o\'chir', 'pc o\'chir'
                ],
                'regex': [
                    r'o\'chir.*?(\d+)\s*(?:soniya|sek|s)',
                ],
                'extract_param': 'delay'
            },
            'restart': {
                'keywords': [
                    'qayta ishga tushir', 'restart', 'reboot',
                    'qayta yoq', 'qayta yuklash', 'perezagruzka'
                ],
                'regex': [
                    r'restart.*?(\d+)',
                ],
                'extract_param': 'delay'
            },
            'cancel_shutdown': {
                'keywords': [
                    'o\'chirishni bekor', 'cancel shutdown',
                    'shutdown bekor', 'o\'chirma', 'bekor qil'
                ],
                'regex': [],
                'extract_param': None
            },
            'sleep': {
                'keywords': [
                    'uxla', 'sleep', 'uxlash rejimi',
                    'suspend', 'kutish rejimi'
                ],
                'regex': [],
                'extract_param': None
            },
            'lock_screen': {
                'keywords': [
                    'ekranni qulfla', 'lock', 'qulflash',
                    'ekran qulfi', 'lock screen', 'qufla'
                ],
                'regex': [],
                'extract_param': None
            },

            # ===== TIZIM MA'LUMOTLARI =====
            'system_info': {
                'keywords': [
                    'tizim haqida', 'system info', 'kompyuter haqida',
                    'tizim ma\'lumot', 'pc info', 'specs'
                ],
                'regex': [],
                'extract_param': None
            },
            'battery_info': {
                'keywords': [
                    'batareya', 'battery', 'quvvat', 'zaryadka',
                    'batareya qancha'
                ],
                'regex': [],
                'extract_param': None
            },
            'time': {
                'keywords': [
                    'vaqt', 'soat', 'time', 'hozir soat nech',
                    'soat nechchi', 'vaqt qancha'
                ],
                'regex': [],
                'extract_param': None
            },
            'processes': {
                'keywords': [
                    'jarayonlar', 'processes', 'nima ishlamoqda',
                    'ishlab turgan', 'task list'
                ],
                'regex': [],
                'extract_param': None
            },

            # ===== TARMOQ =====
            'wifi_status': {
                'keywords': [
                    'wifi holat', 'wifi status', 'internet holat',
                    'wi-fi', 'wifi'
                ],
                'regex': [],
                'extract_param': None
            },
            'wifi_disconnect': {
                'keywords': [
                    'wifi uz', 'wifi o\'chir', 'wifi disconnect',
                    'internetni uz', 'wi-fi uz'
                ],
                'regex': [],
                'extract_param': None
            },
            'wifi_connect': {
                'keywords': [
                    'wifi ulan', 'wifi connect', 'internetga ulan',
                    'wi-fi ulan'
                ],
                'regex': [
                    r'wifi.*?ulan.*?["\']?(\w+)["\']?',
                    r'connect.*?["\']?(\w+)["\']?',
                ],
                'extract_param': 'network'
            },

            # ===== WEB =====
            'open_website': {
                'keywords': [
                    'sayt och', 'website open', 'saytni och',
                    'brauzer och'
                ],
                'regex': [
                    r'(?:sayt|website|brauzer).*?och.*?((?:https?://)?[\w.-]+\.[\w]{2,}[/\w.-]*)',
                    r'och.*?((?:https?://)?[\w.-]+\.[\w]{2,})',
                ],
                'extract_param': 'url'
            },
            'search_google': {
                'keywords': [
                    'google', 'qidir', 'search', 'googleda qidir',
                    'internetda qidir'
                ],
                'regex': [
                    r'(?:google|qidir|search|googleda|internetda).*?["\'](.+?)["\']',
                    r'(?:google|googleda|internetda)\s+(?:qidir\s+)?(.+)',
                    r'qidir\s+(.+)',
                ],
                'extract_param': 'query'
            },
            'search_youtube': {
                'keywords': [
                    'youtube', 'youtubeda', 'video qidir'
                ],
                'regex': [
                    r'youtube.*?(?:qidir|search|och)?\s+(.+)',
                    r'video.*?qidir\s+(.+)',
                ],
                'extract_param': 'query'
            },

            # ===== CLIPBOARD =====
            'copy_clipboard': {
                'keywords': [
                    'clipboard ga nusxala', 'copy', 'nusxala',
                    'clipboard yoz'
                ],
                'regex': [
                    r'(?:nusxala|copy|clipboard).*?["\'](.+?)["\']',
                    r'(?:nusxala|copy)\s+(.+)',
                ],
                'extract_param': 'text'
            },
            'get_clipboard': {
                'keywords': [
                    'clipboard ko\'rsat', 'clipboard nima',
                    'nima nusxalangan', 'clipboard'
                ],
                'regex': [],
                'extract_param': None
            },

            # ===== BOSHQA =====
            'empty_recycle_bin': {
                'keywords': [
                    'axlat quti', 'recycle bin', 'axlatni bo\'shat',
                    'axlat qutisini bo\'shat', 'korzina'
                ],
                'regex': [],
                'extract_param': None
            },
            'help': {
                'keywords': [
                    'yordam', 'help', 'nima qila olasan',
                    'buyruqlar', 'commands', 'imkoniyatlar'
                ],
                'regex': [],
                'extract_param': None
            },
        }

        return patterns

    def _match_exact(self, text):
        """Aniq keyword matching"""
        best_match = None
        best_confidence = 0

        for action, data in self.command_patterns.items():
            for keyword in data['keywords']:
                if keyword in text:
                    confidence = len(keyword) / max(len(text), 1)
                    confidence = min(confidence * 2, 1.0)

                    if confidence > best_confidence:
                        best_confidence = confidence
                        params = self._extract_params(text, data)
                        best_match = {
                            'action': action,
                            'params': params,
                            'confidence': confidence
                        }

        return best_match

    def _match_pattern(self, text):
        """Regex pattern matching"""
        for action, data in self.command_patterns.items():
            for pattern in data.get('regex', []):
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    params = {}
                    if data['extract_param'] and match.groups():
                        params[data['extract_param']] = match.group(1).strip()
                    return {
                        'action': action,
                        'params': params,
                        'confidence': 0.85
                    }

        return None

    def _match_fuzzy(self, text):
        """Fuzzy matching"""
        best_match = None
        best_score = 0

        for action, data in self.command_patterns.items():
            for keyword in data['keywords']:
                score = SequenceMatcher(None, text, keyword).ratio()

                if score > best_score and score >= 0.5:
                    best_score = score
                    params = self._extract_params(text, data)
                    best_match = {
                        'action': action,
                        'params': params,
                        'confidence': score
                    }

        return best_match

    def _extract_params(self, text, data):
        """Buyruqdan parametrlarni ajratib olish"""
        params = {}
        param_name = data.get('extract_param')

        if not param_name:
            return params

        for pattern in data.get('regex', []):
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.groups():
                params[param_name] = match.group(1).strip()
                return params

        if param_name in ('level', 'amount', 'delay'):
            number_match = re.search(r'(\d+)', text)
            if number_match:
                params[param_name] = number_match.group(1)

        if param_name == 'path':
            path_match = re.search(r'([a-zA-Z]:\\[^\s]+|[a-zA-Z]:/[^\s]+)', text)
            if path_match:
                params[param_name] = path_match.group(1)
            else:
                quoted_match = re.search(r'["\'](.+?)["\']', text)
                if quoted_match:
                    params[param_name] = quoted_match.group(1)

        if param_name == 'app_name':
            action_words = [
                'och', 'open', 'ishga', 'tushir', 'run', 'launch',
                'start', 'ochib', 'ber', 'yop', 'close', "o'chir",
                'kil', 'stop', 'yopib', "to'xtat", 'ni', 'yoq'
            ]
            words = text.split()
            remaining = [w for w in words if w.lower() not in action_words]
            if remaining:
                params[param_name] = ' '.join(remaining)

        if param_name == 'url':
            url_match = re.search(r'((?:https?://)?[\w.-]+\.[\w]{2,}[/\w.-]*)', text)
            if url_match:
                params[param_name] = url_match.group(1)

        if param_name == 'query':
            query_words = [
                'google', 'googleda', 'qidir', 'search',
                'youtube', 'youtubeda', 'video', 'internetda'
            ]
            words = text.split()
            remaining = [w for w in words if w.lower() not in query_words]
            if remaining:
                params[param_name] = ' '.join(remaining)

        if param_name == 'network':
            net_words = ['wifi', 'wi-fi', 'ulan', 'connect', 'ga']
            words = text.split()
            remaining = [w for w in words if w.lower() not in net_words]
            if remaining:
                params[param_name] = ' '.join(remaining)

        if param_name == 'text':
            quoted_match = re.search(r'["\'](.+?)["\']', text)
            if quoted_match:
                params[param_name] = quoted_match.group(1)
            else:
                clip_words = ['nusxala', 'copy', 'clipboard', 'ga', 'yoz']
                words = text.split()
                remaining = [w for w in words if w.lower() not in clip_words]
                if remaining:
                    params[param_name] = ' '.join(remaining)

        return params

    def get_help_text(self):
        """Barcha mavjud buyruqlar ro'yxati"""
        help_text = """
╔══════════════════════════════════════════════════╗
║           MAVJUD BUYRUQLAR RO'YXATI             ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  🖼️  WALLPAPER:                                  ║
║    • wallpaperni o'zgartir C:\\rasm.jpg           ║
║    • fon rasm "C:\\Users\\rasm.png"               ║
║                                                  ║
║  🔊 OVOZ:                                        ║
║    • ovozni 50% ga qo'y                          ║
║    • ovozni oshir / pasaytir                     ║
║    • ovozni o'chir (mute)                        ║
║    • ovozni yoq (unmute)                         ║
║                                                  ║
║  🔆 YORQINLIK:                                   ║
║    • yorqinlik 70%                               ║
║    • yorqinlikni oshir / kamaytir                ║
║                                                  ║
║  📱 ILOVALAR:                                    ║
║    • notepad och / chrome och                    ║
║    • telegram yop / chrome yop                   ║
║                                                  ║
║  📁 FAYLLAR:                                     ║
║    • fayl och C:\\doc.pdf                         ║
║    • papka och C:\\Users\\Desktop                  ║
║    • papka yarat C:\\yangi_papka                  ║
║    • fayllar ro'yxati C:\\Users                   ║
║                                                  ║
║  📸 SKRINSHOT:                                   ║
║    • skrinshot ol                                ║
║                                                  ║
║  🌐 WEB:                                         ║
║    • sayt och google.com                         ║
║    • google qidir "python tutorial"              ║
║    • youtube qidir "music"                       ║
║                                                  ║
║  💻 TIZIM:                                       ║
║    • kompyuterni o'chir                          ║
║    • qayta ishga tushir (restart)                ║
║    • uxla (sleep)                                ║
║    • ekranni qulfla (lock)                       ║
║    • tizim haqida ma'lumot                       ║
║    • batareya holati                             ║
║    • vaqt / soat                                 ║
║                                                  ║
║  📶 TARMOQ:                                      ║
║    • wifi holati                                 ║
║    • wifi uz / wifi ulan [nomi]                  ║
║                                                  ║
║  📋 CLIPBOARD:                                   ║
║    • nusxala "matn"                              ║
║    • clipboard ko'rsat                           ║
║                                                  ║
║  🗑️  BOSHQA:                                     ║
║    • axlat qutisini bo'shat                      ║
║    • jarayonlar ko'rsat                          ║
║                                                  ║
║  ❌ CHIQISH:                                     ║
║    • exit / chiqish / chiq                       ║
║                                                  ║
╚══════════════════════════════════════════════════╝
"""
        return help_text
