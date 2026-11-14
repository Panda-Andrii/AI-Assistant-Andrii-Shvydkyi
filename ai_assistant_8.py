# import tkinter as tk
#
# def on_click():
#     name = entry.get()
#     label.config(text=f"Привіт, {name}!")
#
# root = tk.Tk()
# root.title("AIDA")
# root.geometry("400x200")
#
# label = tk.Label(root, text="Як тебе звати", font = ("Arial", 20))
# label.pack(pady=15)
# entry = tk.Entry(root, font=("Arial", 14))
# entry.pack()
# button = tk.Button(root, text="Привітатися", font=("Arial", 20), command=on_click)
# button.pack(pady=15)
#
# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
#
# root = tk.Tk()
# root.title("Аватар AIDA")
# root.geometry("320x300")
#
# picture = Image.open("avatars/neutral.png")
# picture = picture.resize((220,220))
# photo = ImageTk.PhotoImage(picture)
#
# avatar = tk.Label(root, image=photo)
# avatar.pack(pady=10)
# tk.Label(root, text="Я AIDA", font=("Arial", 14)).pack()
#
# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
#
# EMOTIONS = ["neutral", "happy", "sad", "surprised"]
#
# def set_emotion(emotion):
#     avatar.config(image=images[emotion])
#     status.config(text=f"Емоція: {emotion}")
#
# root = tk.Tk()
# root.title("AIDA")
# root.geometry("420x320")
#
# images = {}
# for emotion in EMOTIONS:
#     picture = Image.open(f"avatars/{emotion}.png").resize((200,200))
#     images[emotion] = ImageTk.PhotoImage(picture)
#
# avatar = tk.Label(root, image=images["neutral"])
# avatar.pack(pady=5)
# status = tk.Label(root, text="Емоція: neutral", font=("Arial", 12))
# status.pack()
#
# buttons = tk.Frame(root)
# buttons.pack(pady=10)
# for emotion in EMOTIONS:
#     tk.Button(buttons, text=emotion, width=9, command=lambda e=emotion: set_emotion(e)).pack(side="left" ,padx=3)
#
# root.mainloop()

import random
import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk

NAME = "AIDA"
EMOTION_WORDS = {
    "laugh": ["жарт", "смішн", "ха-ха", "анекдот"],
    "happy": ["дякую", "супер", "клас", "круто", "люблю", "привіт"],
    "sad": ["помилка", "сумно", "погано", "не вийшло", "двійк"],
    "surprised": ["вау", "ого", "невже", "серйозно"],
    "thinking": ["чому", "як ", "що таке", "поясни"],
}
COLORS = {
    "neutral": "#EEF2F7", "happy": "#FFF3C4", "laugh": "#FFE08A",
    "sad": "#DCE6F5", "surprised": "#FFE3CC", "thinking": "#EDE4FF",
}
JOKES = [
    "Чому програміст плутає Хелловін і Різдво? Бо 31 OCT = 25 DEC.",
    "Скільки програмістів треба, щоб замінити лампочку? Жодного — це апаратна проблема.",
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


def send(event=None):
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
    chat.see(tk.END)
    set_emotion(emotion)


root = tk.Tk()
root.title(f"{NAME} — мій AI-помічник")
root.geometry("460x550")
root.configure(bg=COLORS["neutral"])

images = {}
for emotion in COLORS:
    picture = Image.open(f"avatars/{emotion}.png").resize((180, 180))
    images[emotion] = ImageTk.PhotoImage(picture)

avatar = tk.Label(root, image=images["neutral"], bg=COLORS["neutral"])
avatar.pack(pady=(15, 0))
mood_label = tk.Label(root, text="Настрій: neutral", font=("Arial", 10), bg=COLORS["neutral"], fg="#5F6B7A")
mood_label.pack()

chat = tk.Text(root, height=14, width=50, wrap="word", font=("Arial", 11), state="disabled", relief="flat", padx=8,
               pady=8)
chat.tag_config("user", foreground="#2F6FB5")
chat.tag_config("bot", foreground="#1F2933")
chat.pack(padx=15, pady=10)

bottom = tk.Frame(root, bg="#FFFFFF")
bottom.pack(fill="x", padx=15, pady=(0, 15))
entry = tk.Entry(bottom, font=("Arial", 12), relief="flat")
entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(6, 0))
entry.bind("<Return>", send)
button = tk.Button(bottom, text="Надіслати", command=send, bg="#FF9C00", fg="white", relief="flat", padx=10)
button.pack(side="right", padx=4, pady=4)
entry.focus()

root.mainloop()
