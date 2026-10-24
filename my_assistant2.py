import random

NAME = "Біт (Bot)"

def get_response(user_text):
    text = user_text.lower().strip()

    if "привіт" in text or "вітаю" in text:
        return "Йо! Що слухаємо сьогодні?"

    if "мотивуй мене" in text:
        return "Навіть хіт номер один колись був чернеткою!"

    if "музик" in text or "трек" in text:
        return "Хороший біт лікує будь-який поганий день. Додай гучності!"

    if "я втом" in text or "сумно" in text:
        return "Увімкни щось драйвове, бро. Музика заряджає!"

    if "хто ти" in text or "трек" in text:
        return "Я твій віртуальний ді-джей та гід по світу крутих звуків."

    if "рекоменд" in text or "що послухати" in text:
        return "Послухай сьогодні класичний хіп-хоп або якісний синтвейв!"

    return "Мій еквалайзер такого не ловить. Повтори ще раз або скажи 'мотивуй мене'!"

while True:
    user_text = input("Ти: ")
    if user_text.lower().strip() == "бувай":
        print(f"{NAME}: Тримай ритм! До зустрічі.")
        break
    print(f"{NAME}: {get_response(user_text)}")