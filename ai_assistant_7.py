#from gtts import gTTS
#from playsound import playsound
#
#tts = gTTS(text="Привіт, тестовий запис для gTTS.", lang="uk")
#tts.save("speech.mp3")
#print("File Saved")
#playsound("speech.mp3")

import os
from gtts import gTTS
from playsound import playsound
from datetime import datetime
import speech_recognition as sr

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
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio, language='uk-UA')
    except (sr.UnknownValueError, sr.RequestError):
        return ""
    print(f"Ти: {text}")
    return text.lower()

def respond(text):
    if "привіт" in text:
        return "Привіт! Рада тебе чути."
    if "годин" or "котра" in text:
        return "Зараз " + datetime.now().strftime("%H:%M")
    return "Я почула: " + text

say("Привіт! Я слухаю. Скажи СТОП, щоб завершити.")
while True:
    text = listen()
    if not text:
        continue
    if "стоп" in text:
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
