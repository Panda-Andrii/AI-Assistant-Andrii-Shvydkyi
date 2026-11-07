import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Слухаю...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Скажи щось!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            print("Час вичерпаний...")
            return

    try:
        text = recognizer.recognize_google(audio, language='uk-UA')
    except sr.UnknownValueError:
        print("Не розпізнаний звук, повтори знову.")
        return ""
    except sr.RequestError:
        print("Проблеми зі з'єднанням з сервісами. Спробуй пізніше.")
        return ""
    print(f"Ти сказав: {text}")
    return text.lower()

print("NEON: Я слухаю друже! Скажи стоп щоб завершити")

while True:
    text = listen()
    if not text:
        continue
    if "стоп" in text:
        print("Тримай ритм, бувай!")
        break
    elif "порадь музику" in text or "включи музику" in text:
        print("NEON: Спробуй lo-fi - ідеально для домашки.")
    elif "який настрій" in text:
        print("NEON: Рок-н-рольний! Готовий до нових треків.")
    elif "твоє ім'я" in text or "хто ти" in text:
        print("NEON: Я твій музичний біт-помічник")
    else:
        print(f"NEON: Ви сказали '{text}', але я поки не знаю такої команди.")

#NEON: Я слухаю друже! Скажи стоп щоб завершити
#Слухаю...
#Скажи щось!
#Ти сказав: музику
#NEON: Ви сказали 'музику', але я поки не знаю такої команди.
#Слухаю...
#Скажи щось!
#Не розпізнаний звук, повтори знову.
#Слухаю...
#Скажи щось!
#Ти сказав: включи
#NEON: Ви сказали 'включи', але я поки не знаю такої команди.
#Слухаю...
#Скажи щось!
#Ти сказав: Включи музику
#NEON: Спробуй lo-fi - ідеально для домашки.
#Слухаю...
#Скажи щось!
#Ти сказав: який настрій
#NEON: Рок-н-рольний! Готовий до нових треків.
#Слухаю...
#Скажи щось!
#Ти сказав: Хто ти
#NEON: Я твій музичний біт-помічник
#Слухаю...
#Скажи щось!
#Час вичерпаний...
#Слухаю...
#Скажи щось!
#Ти сказав: Ну все стоп
#Тримай ритм, бувай!