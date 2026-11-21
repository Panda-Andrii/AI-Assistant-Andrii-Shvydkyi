import random
import threading
import tkinter as tk

import requests
from PIL import Image, ImageTk
from config import API_KEY, URL, MODEL

NAME = "AIDA"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
EMOTIONS = ["neutral", "happy", "sad", "surprised", "thinking", "laugh"]
COLORS = {"neutral": "#EEF2F7", "happy": "#FFF3C4", "laugh": "#FFE08A",
          "sad": "#DCE6F5", "surprised": "#FFE3CC", "thinking": "#EDE4FF"}
SYSTEM = f"""Ти — {NAME}, доброзичлива помічниця для підлітків. Відповідай українською, до 3 речень.
На початку КОЖНОЇ відповіді постав тег своєї емоції у квадратних дужках —
один з: [neutral], [happy], [sad], [surprised], [thinking], [laugh]. Далі — сама відповідь.
Приклад: [happy] Чудова ідея!"""
QUICK = {
    "Порада дня": "Дай одну коротку корисну пораду дня для підлітка.",
    "Жарт": "Розкажи короткий смішний жарт для підлітків.",
    "Мотивуй": "Скажи мені щось мотивуюче одним-двома реченнями.",
}
messages = [{"role": "system", "content": SYSTEM}]
current = {"emotion": "neutral", "waiting": False, "answer": None}


# ---------- мозок ----------
def ask_ai(text):
    messages.append({"role": "user", "content": text})
    try:
        r = requests.post(URL, headers=HEADERS, json={"model": MODEL, "messages": messages}, timeout=30)
    except requests.exceptions.RequestException:
        messages.pop()
        return "[sad] Немає зв'язку з сервером. Перевір інтернет."
    if r.status_code != 200:
        messages.pop()
        return f"[sad] Помилка {r.status_code}. Спробуй пізніше."
    answer = r.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer


def parse_reply(answer):
    answer = answer.strip()
    if answer.startswith("[") and "]" in answer:
        tag = answer[1:answer.index("]")].strip().lower()
        text = answer[answer.index("]") + 1:].strip()
        return (tag if tag in EMOTIONS else "neutral"), text
    return "neutral", answer


# ---------- анімації ----------
def set_emotion(emotion):
    current["emotion"] = emotion
    paint(COLORS[emotion])
    avatar.config(image=images[emotion])


def paint(color):
    for widget in (root, avatar, status, buttons):
        widget.configure(bg=color)


def blink():
    if not current["waiting"]:
        avatar.config(image=images["blink"])
        root.after(150, lambda: avatar.config(image=images[current["emotion"]]))
    root.after(random.randint(2500, 4500), blink)


def animate_thinking(step=0):
    if not current["waiting"]:
        status.config(text="")
        return
    status.config(text=f"{NAME} думає" + "." * (step % 4))
    root.after(300, animate_thinking, step + 1)


def flash(times=6):
    if times == 0:
        paint(COLORS[current["emotion"]])
        return
    paint("#FFC94D" if times % 2 else "#FFF3C4")
    root.after(120, flash, times - 1)


# ---------- чат ----------
def add_to_chat(who, text, tag):
    chat.config(state="normal")
    chat.insert(tk.END, f"{who}: {text}\n\n", tag)
    chat.config(state="disabled")
    chat.see(tk.END)


def worker(text):                       # працює в окремому потоці, tkinter тут не чіпаємо
    current["answer"] = ask_ai(text)


def check_answer():
    if current["answer"] is None:
        root.after(100, check_answer)   # ще не готово — перевіримо через 0,1 с
        return
    current["waiting"] = False
    emotion, text = parse_reply(current["answer"])
    add_to_chat(NAME, text, "bot")
    set_emotion(emotion)
    if emotion == "laugh":
        flash()
    send_button.config(state="normal")


def ask(text, shown=None):
    if current["waiting"]:
        return
    add_to_chat("Ти", shown or text, "user")
    current["waiting"] = True
    current["answer"] = None
    send_button.config(state="disabled")
    set_emotion("thinking")
    animate_thinking()
    threading.Thread(target=worker, args=(text,), daemon=True).start()
    check_answer()


def send(event=None):
    text = entry.get().strip()
    if text:
        entry.delete(0, tk.END)
        ask(text)


# ---------- вікно ----------
root = tk.Tk()
root.title(f"{NAME} — AI-помічниця")
root.geometry("480x610")
images = {e: ImageTk.PhotoImage(Image.open(f"avatars/{e}.png").resize((170, 170))) for e in EMOTIONS + ["blink"]}

avatar = tk.Label(root, image=images["neutral"])
avatar.pack(pady=(12, 0))
status = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="#5F6B7A")
status.pack()
buttons = tk.Frame(root)
buttons.pack(pady=4)
for title, prompt in QUICK.items():
    tk.Button(buttons, text=title, width=11, command=lambda t=title, p=prompt: ask(p, shown=t)).pack(side="left", padx=3)

chat = tk.Text(root, height=14, wrap="word", font=("Arial", 11), state="disabled", relief="flat", padx=8, pady=8)
chat.tag_config("user", foreground="#2F6FB5")
chat.pack(fill="x", padx=15, pady=8)
bottom = tk.Frame(root, bg="#FFFFFF")
bottom.pack(fill="x", padx=15, pady=(0, 12))
entry = tk.Entry(bottom, font=("Arial", 12), relief="flat")
entry.pack(side="left", fill="x", expand=True, ipady=6, padx=6)
entry.bind("<Return>", send)
send_button = tk.Button(bottom, text="Надіслати", command=send, bg="#FF9C00", fg="white", relief="flat")
send_button.pack(side="right", padx=4, pady=4)

set_emotion("neutral")
add_to_chat(NAME, "Привіт! Я AIDA. Питай що завгодно або натисни кнопку вгорі.", "bot")
root.after(3000, blink)
entry.focus()
root.mainloop()