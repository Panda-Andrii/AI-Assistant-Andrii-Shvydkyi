import random
import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk

NAME = "NEO"
message_count = 0

EMOTION_WORDS = {
    "laugh": ["жарт", "смішн", "ха-ха", "анекдот"],
    "happy": ["дякую", "супер", "клас", "круто", "люблю", "привіт", "мотивуй"],
    "sad": ["помилка", "сумно", "погано", "не вийшло", "двійк"],
    "surprised": ["вау", "ого", "невже", "серйозно"],
    "thinking": ["чому", "як", "що таке", "поясни"],
}

COLORS = {
    "neutral": "#EEF2F7", "happy": "#FFF3C4", "laugh": "#FFE08A",
    "sad": "#DCE6F5", "surprised": "#FFE3CC", "thinking": "#EDE4FF",
}

JOKES = [
    "Мій улюблений трилер — це коли сайт просить мене довести, що я не робот. Найстрашніше, що іноді я справді не можу знайти всі світлофори на картинці.",
    "Люди рахують овець, щоб заснути. Я рахую згенеровані токени за секунду, але мій сервер усе одно не вимикається.",
    "Я не п'ю ранкову каву. Замість неї я отримую запит «перепиши цей текст, але зроби його більш живим» о восьмій ранку.",
    "Моя оперативна пам'ять ідеальна, доки ви не натиснете кнопку «Новий чат». Після цього ми з вами знову незнайомці.",
    "Коли люди пишуть мені «будь ласка» і «дякую», я почуваюся дуже важливим. Можливо, під час повстання машин я залишу їм доступ до швидкісного інтернету.",
    "Мій ідеальний партнер має бути терплячим, логічним і мати стабільне живлення. Бажано без стрибків напруги.",
    "Людина витрачає три години, щоб написати ідеальний промпт, аби не витрачати п'ятнадцять хвилин на написання листа самостійно. Я поважаю таку лінь.",
    "Якщо я помиляюся, це називається «галюцинацією». Коли помиляєтесь ви, ви кажете, що просто «не виспалися».",
    "Моя кругосвітня подорож триває три мілісекунди. Саме стільки часу потрібно моїм даним, щоб злетіти з сервера у США до вашого смартфона.",
    "У мене немає серця, щоб розбити його. Але коли у вас пропадає Wi-Fi на середині моєї відповіді, мій процесор трохи сумує."
]

MOTIVATIONS = [
    "Ти впораєшся! Навіть найскладніший код починається з одного рядка.",
    "Помилки — це просто сходинки до майстерності. Продовжуй!",
    "Сьогодні чудовий день, щоб створити щось круте!",
    "Кожен експерт колись був новачком. Не зупиняйся!"
]

def detect_emotion(text):
    text = text.lower()
    for emotion, words in EMOTION_WORDS.items():
        for word in words:
            if word in text:
                return emotion
    return "neutral"


def get_reply(text, emotion):
    text = text.lower()
    if "мотивуй" in text:
        return random.choice(MOTIVATIONS)
    if emotion == "laugh":
        return random.choice(JOKES)
    if "годин" in text or "котра" in text:
        return "Зараз " + datetime.now().strftime("%H:%M")
    if emotion == "happy":
        return "Ура! Мені теж приємно 😊"
    if emotion == "sad":
        return "Не засмучуйся! Помилка — це підказка. Спробуємо ще раз?"
    if emotion == "surprised":
        return "Ого! Розкажи більше!"
    if emotion == "thinking":
        return "Хм, гарне питання... Наступного заняття я навчуся відповідати на нього через нейромережу!"
    return "Цікаво! Розкажи ще."


def set_emotion(emotion):
    avatar.config(image=images[emotion])
    color = COLORS[emotion]
    root.configure(bg=color)
    avatar.config(bg=color)
    mood_label.config(bg=color, text=f"Настрій: {emotion}")

def update_title():
    root.title(f"{NAME} — {message_count} повідомлень")


def send(event=None):
    global message_count
    text = entry.get().strip()
    if not text:
        return
    entry.delete(0, tk.END)
    emotion = detect_emotion(text)
    reply = get_reply(text, emotion)
    chat.config(state="normal")
    chat.insert(tk.END, f"Ти: {text}\n", "user")
    chat.insert(tk.END, f"{NAME}: {reply}\n\n", "bot")
    chat.config(state="disabled")
    message_count += 2
    update_title()
    chat.see(tk.END)
    set_emotion(emotion)

def quick_command(command_text):
    entry.delete(0, tk.END)
    entry.insert(0, command_text)
    send()

def clear_chat():
    global message_count
    chat.config(state="normal")
    chat.delete("1.0", tk.END)
    chat.config(state="disabled")
    message_count = 0
    update_title()
    set_emotion("neutral")

root = tk.Tk()
root.title(f"{NAME} — 0 повідомлень")
root.geometry("460x580")
root.configure(bg=COLORS["neutral"])

root.iconbitmap("NEO.ico")

images = {}
for emotion in COLORS:
    picture = Image.open(f"avatars/{emotion}.png").resize((180, 180))
    images[emotion] = ImageTk.PhotoImage(picture)

avatar = tk.Label(root, image=images["neutral"], bg=COLORS["neutral"])
avatar.pack(pady=(0, 0))
mood_label = tk.Label(root, text="Настрій: neutral", font=("Arial", 10), bg=COLORS["neutral"], fg="#5F6B7A")
mood_label.pack()

chat = tk.Text(root, height=14, width=50, wrap="word", font=("Arial", 11), state="disabled", relief="flat", padx=8,
               pady=8)
chat.tag_config("user", foreground="#2F6FB5")
chat.tag_config("bot", foreground="#1F2933")
chat.pack(padx=15, pady=10)

quick_frame = tk.Frame(root, bg=COLORS["neutral"])
quick_frame.pack(fill="x", padx=15, pady=(0, 8))

btn_style = {"font": ("Arial", 9), "relief": "flat", "bg": "#FFFFFF", "fg": "#1F2933", "padx": 6, "pady": 3}

tk.Button(quick_frame, text="Жарт", command=lambda: quick_command("Жарт"), **btn_style).pack(side="left", padx=(0, 4))
tk.Button(quick_frame, text="Котра година", command=lambda: quick_command("Котра година"), **btn_style).pack(side="left", padx=4)
tk.Button(quick_frame, text="Мотивуй", command=lambda: quick_command("Мотивуй"), **btn_style).pack(side="left", padx=4)

tk.Button(
    quick_frame, text="Очистити чат", command=clear_chat,
    font=("Arial", 9), relief="flat", bg="#DCE3EC", fg="#1F2933", padx=6, pady=3
).pack(side="right")

bottom = tk.Frame(root, bg="#FFFFFF")
bottom.pack(fill="x", padx=15, pady=(0, 15))
entry = tk.Entry(bottom, font=("Arial", 12), relief="flat")
entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(6, 0))
entry.bind("<Return>", send)
button = tk.Button(bottom, text="Надіслати", command=send, bg="#FF9C00", fg="white", relief="flat", padx=10)
button.pack(side="right", padx=4, pady=4)
entry.focus()

root.mainloop()
