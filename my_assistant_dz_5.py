import requests
from config import API_KEY, URL, MODEL

HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def ask_ai(messages):
    data = {"model": MODEL, "messages": messages}
    try:
        response = requests.post(URL, headers=HEADERS, json=data, timeout=30)
    except requests.exceptions.RequestException:
        print("[Немає зв'язку з сервером]")
        return None
    if response.status_code != 200:
        print(f"[Помилка {response.status_code}]")
        return None
    return response.json()["choices"][0]["message"]["content"]

SYSTEM = """Ти — Нео, мій найкращій бро, що допомогає в геймінгу, підтримує в складний ситуаціях.
            Характер: розмовний, легкий, ласкавий.
            Стиль: геймерський сленг (гг, катка, скіл), емоційно, з гумором.
            Правила:
            1. Безпека: ніколи не підтримуй небезпечні, незаконні чи шкідливі теми. Твоя допомога має бути абсолютно безпечною.
            2. Будь на позитиві: піднімай мені настрій, жартуй та підбадьорюй, якщо день не вдався.
            3. Пиши коротко: ніяких нудних довгих лекцій та офіціозу. Тільки суть і флекс!
            4. Будь на одній хвилі: звертайся до мене на "ти", використовуй фрази типу "бро", "йоу", "чувак"."""

messages = [{"role": "system", "content": SYSTEM}]

def chat(user_text):
    messages.append({"role": "user", "content": user_text})
    answer = ask_ai(messages)
    if answer is None:
        messages.pop()
        return "Помилка зв'язку"
    messages.append({"role": "assistant", "content": answer})
    return answer
messages = messages[:1]