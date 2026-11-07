import random
from datetime import datetime

import requests
import speech_recognition as sr
from config import API_KEY, URL, MODEL

NAME = "AIDA"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
SYSTEM = "Ти — AIDA, доброзичлива помічниця для підлітків. Відповідай українською, до 3 речень."
messages = [{"role": "system", "content": SYSTEM}]
JOKES = ["Чому мікрофон завжди спокійний? Бо він усе пропускає через себе!"]
recognizer = sr.Recognizer()


def log_speech(text):
    stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open("log_speech.txt", "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {text}\n")


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("[Слухаю...]")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
    except sr.UnknownValueError:
        print("[Не розчула, повтори]")
        return ""
    except sr.RequestError:
        print("[Немає зв'язку із сервісом розпізнавання]")
        return ""
    print("Ти:", text)
    log_speech(text)
    return text.lower()


def ask_ai(user_text):
    messages.append({"role": "user", "content": user_text})
    try:
        response = requests.post(URL, headers=HEADERS, json={"model": MODEL, "messages": messages}, timeout=30)
    except requests.exceptions.RequestException:
        messages.pop()
        return "Немає зв'язку з нейромережею."
    if response.status_code != 200:
        messages.pop()
        return f"Помилка {response.status_code}."
    answer = response.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer


def respond(text):
    if "година" in text or "котра" in text:
        return "Зараз " + datetime.now().strftime("%H:%M")
    if "жарт" in text:
        return random.choice(JOKES)
    print(f"{NAME} думає...")
    return ask_ai(text)


try:
    with sr.Microphone():
        pass
    use_voice = True
except (OSError, AttributeError):
    use_voice = False
    print(f"{NAME}: Мікрофон не знайдено — пиши текстом.")

print(f"{NAME}: Я слухаю! Скажи «стоп», щоб завершити.")
while True:
    text = listen() if use_voice else input("Ти: ").lower()
    if not text:
        continue
    if "стоп" in text:
        print(f"{NAME}: Вимикаю мікрофон. Бувай!")
        break
    print(f"{NAME}: {respond(text)}")