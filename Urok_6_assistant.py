import speech_recognition as sr
from datetime import datetime

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(index,name)

recognizer = sr.Recognizer()

recognized_count = 0
unrecognized_count = 0

def listen():
    global unrecognized_count
    with sr.Microphone() as source:
        print("Listeting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Say something!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            print("Timed out...")
            return

    try:
        text = recognizer.recognize_google(audio, language='uk-UA')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        unrecognized_count += 1
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")
        return ""
    print(f"Text: {text}")
    return text.lower()

def log_speech(text):
    stamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open("log_speech.txt", "a", encoding="utf-8") as f:
        f.write(f"{stamp}: {text}\n")

print("AIDA: Я слухаю. Скажи стоп щоб завершити")

while True:
    text = listen()
    if not text:
        continue
    recognized_count += 1
    if "стоп" in text:
        print("Вимикаю мікро, бувай!")
        break
    log_speech(text)
    print(f"AIDA: Ти сказав {len(text.split())} слова(-ів)")

total_phrases = recognized_count + unrecognized_count

print("\n-------Статистика--------")

print(f"Я розпізнала {recognized_count} з {total_phrases} фраз")
print(f"Я не розпізнала {unrecognized_count} з {total_phrases} фраз")

with open("log_speech.txt", "r", encoding="utf-8") as f:
    print(len(f.readlines()), "записи в журналі")
