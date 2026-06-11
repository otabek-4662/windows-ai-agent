"""
Windows 11 AI Desktop Agent
============================
Matn orqali kompyuterni boshqarish uchun AI agent.

Imkoniyatlari:
- Wallpaper o'zgartirish
- Ovoz balandligini boshqarish
- Yorqinlikni o'zgartirish
- Ilovalarni ochish/yopish
- Fayllarni ochish
- Tizim ma'lumotlarini ko'rish
- Wi-Fi boshqarish
- Skrinshot olish
- Kompyuterni o'chirish/qayta ishga tushirish
"""

from chat_interface import ChatInterface


def main():
    print("=" * 50)
    print("   WINDOWS 11 AI DESKTOP AGENT")
    print("   Kompyuteringizni matn orqali boshqaring!")
    print("=" * 50)
    print()
    print("Misollar:")
    print("  - 'wallpaperni o'zgartir C:/rasm.jpg'")
    print("  - 'ovozni 50% ga qo'y'")
    print("  - 'notepad och'")
    print("  - 'yorqinlikni oshir'")
    print("  - 'skrinshot ol'")
    print("  - 'kompyuterni o'chir'")
    print()
    print("Chiqish uchun 'exit' yoki 'chiqish' yozing.")
    print("-" * 50)

    chat = ChatInterface()
    chat.run()


if __name__ == "__main__":
    main()
