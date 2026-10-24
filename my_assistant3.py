from datetime import datetime
import time

KEYWORDS = {"greeting": ["привіт", "вітаю", "добрий день", "хай"], "time": ["годин", "котра", "час", "яка година"], "joke": ["жарт", "анекдот", "смішн", "розсміши"], "weather": ["погод", "дощ", "сонце", "температур", "тепло"]}

def clean(user_text):
    text = user_text.lower()
    punctuation = ".,!?;:-()/'_"
    for char in punctuation:
        text = text.replace(char, " ")

    return text.strip()

def analyze(user_text):
    cleaned_text = clean(user_text)
    for topic, words in KEYWORDS.items():
        for word in words:
            if word in cleaned_text:
                return topic
    return "unknown"

def handle_greeting():
    return "Біт: Привіт! Радий тебе бачити. Чим можу допомогти?"

def handle_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    return f"Біт: Зараз {current_time} - саме час для продуктивної роботи або відпочинку!"

def handle_joke():
    return "Біт: Чому барабанщик не ходить у бібліотеку? Бо там тихо!"

def handle_weather():
    return "Біт: За вікном чудовий день для програмування!"

def handle_unknown():
    return "Біт: На жаль, я не зрозумів фразу. Спробуй сказати інакше."

def respond(topic):
    if topic == "greeting":
        return handle_greeting()
    elif topic == "time":
        return handle_time()
    elif topic == "joke":
        return handle_joke()
    elif topic == "weather":
        return handle_weather()
    else:
        return handle_unknown()

def run_assistant(phrase):
    print(f"Ти: {phrase}")
    time.sleep(0.5)
    topic = analyze(phrase)
    response = respond(topic)
    print(response)
    print("-" * 30)

#Тестування помічника на різних фразах (Закоментуйте усе внизу щоб просто користуватись помічником)

if __name__ == "__main__":
    test_phrases = ["Привіт, боте!", "Підкажи, а котра зараз година?", "Нумо, розсміши мене!", "Яка там сьогодні погода?", "Що ти вмієш робити?", "Доброго дня!!!", "Скільки часу?", "Розкажи свіжий анекдот."]

    print("--- Запуск тестування помічника --- \n")
    for phrase in test_phrases:
        run_assistant(phrase)

# Перевірка на фразах: (Ваш запит - відповідь помічника - правильно/неправильно)
# ---------------------------------------------------------------------------------------------------------------------------------
# Привіт, боте! - Привіт! Радий тебе бачити. Чим можу допомогти? - правильно
# Підкажи, а котра зараз година? - Зараз 18:37:26 - саме час для продуктивної роботи або відпочинку! - правильно
# Нумо, розсміши мене! - Чому барабанщик не ходить у бібліотеку? Бо там тихо! - правильно
# Яка там сьогодні погода? - За вікном чудовий день для програмування! - правильно
# Що ти вмієш робити? - На жаль, я не зрозумів фразу. Спробуй сказати інакше. - правильно (бо нема ніяких слів про його вміння)
# Доброго дня!!! На жаль, я не зрозумів фразу. Спробуй сказати інакше. - правильно (звичайна помилка, правильно казати добрий день)
# Скільки часу? - Зараз 18:37:28 - саме час для продуктивної роботи або відпочинку! - правильно
# Розкажи свіжий анекдот. - Чому барабанщик не ходить у бібліотеку? Бо там тихо!