import os
import json
from datetime import datetime
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import random
import webbrowser

recognizer = sr.Recognizer()

def say(text, lang="uk"):
    print(f"AIDA: {text}")
    try:
        tts = gTTS(text, lang=lang)
        tts.save("voice.mp3")
        playsound("voice.mp3")
        os.remove("voice.mp3")
    except Exception as e:
        print(f"We have an exception! Details: {e}" )

def listen():
    with sr.Microphone() as source:
        print("Слухаю...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio, language='uk-UA')
    except (sr.UnknownValueError, sr.RequestError):
        return ""
    print(f"Ви: {text}")
    return text.lower()

def get_user_name():
    if os.path.exists("user.json"):
        try:
            with open("user.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                return data.get("name", "")
        except Exception:
            return ""
    return ""

def respond(text):
    name = get_user_name()
    if "привіт" in text:
        return f"Привіт, {name}! Рада тебе чути."
    elif "годин" in text or "котра" in text:
        return "Зараз " + datetime.now().strftime("%H:%M")
    elif "монетк" in text or "орел" in text:
        result = random.choice(["Орел", "Решка"])
        return f"Випало: {result}!"
    elif "ютуб" in text or "відео" in text:
        webbrowser.open("https://youtube.com")
        return "Відкриваю YouTube."
    return "Я почула: " + text

say("Привіт! Я слухаю. Скажи СТОП, щоб завершити.")
while True:
    text = listen()
    if not text:
        continue
    if "стоп" in text or "бувай" in text:
        say("Бувай! Гарного дня!")
        break
    say(respond(text))

def split_sentences(text):
    sentences, current = [], ""
    for ch in text:
        current += ch
        if ch in ".!?":
            if current.strip():
                sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    return sentences

def clean_for_speech(text):
    result = ""
    for ch in text:
        if ch.isalnum() or ch in ".,!?;:-'`()%":
            result += ch
        elif ch == "\n":
            result += " "
    return " ".join(result.split())
