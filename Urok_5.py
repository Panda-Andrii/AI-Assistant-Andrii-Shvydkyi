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


SYSTEM = """Ти — Рекс, досвідчений ігровий наставник для геймерів-початківців.
            Характер: азартний, підтримуючий, оптимістичний.
            Стиль: геймерський сленг (гг, катка, скіл), емоційно, з гумором.
            Правила:
            Завжди підбадьоруй гравця після поразок у грі.
            Давай короткі підказки щодо проходження, але не спойлери сюжет.
            Радь цікаві великодки (пасхалки) та приховані квести.
            Безпека: ніколи не пропонуй і не посилайся на піратські сайти, чити або шкідливі програми для зламу ігор."""

messages = [{"role": "system", "content": SYSTEM}]

def chat(user_text):
    messages.append({"role": "user", "content": user_text})
    answer = ask_ai(messages)
    if answer is None:
        messages.pop()
        return "Вибач, не вдалося отримати відповідь."
    messages.append({"role": "assistant", "content": answer})
    return answer
