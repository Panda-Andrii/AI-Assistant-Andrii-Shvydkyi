# import tkinter as tk
#
# seconds = 0
#
# def tick():
#     global seconds
#     seconds += 1
#     label.config(text=f"Минуло секунд: {seconds}")
#     root.after(1000, tick)
#
# root = tk.Tk()
# root.title("after usage")
# root.geometry("360x120")
# label = tk.Label(root, text="Минуло секунд: 0", font = ("Arial", 18))
# label.pack(pady=35)
# root.after(1000, tick)
# root.mainloop()

# import random
# import tkinter as tk
# from PIL import Image, ImageTk
#
# current_emotion = "neutral"
#
# def blink():
#     avatar.config(image=images["blink"])
#     root.after(150, open_eyes)
#
# def open_eyes():
#     avatar.config(image=images[current_emotion])
#     root.after(random.randint(2500, 4500), blink)
#
# root = tk.Tk()
# root.title("AIDA Blinks")
# images = {e: ImageTk.PhotoImage(Image.open(f"avatars/{e}.png").resize((200,200)))
#           for e in ["neutral", "blink"]}
# avatar = tk.Label(root, image=images["neutral"])
# avatar.pack(padx=40, pady=(0, 20))
# root.after(3000, open_eyes)
# root.mainloop()

# import tkinter as tk
#
# waiting = True
#
# def animate_thinking(step=0):
#     if not waiting:
#         status.config(text="")
#     status.config(text="AIDA Thinking" + "." * (step % 4))
#     root.after(300, animate_thinking, step + 1)
#
# def flash(times=6):
#     if times == 0:
#         paint(COLORS[current_emotion])
#         return
#     paint("#FFC940" if times % 2 else "#FFF3C4")
#     root.after(120, flash, times - 1)
#
# root = tk.Tk()
# root.title("Waiting Animation")
# root.geometry("320x100")
# status = tk.Label(root, text="", font=("Arial", 16, "italic"))
# status.pack(pady=30)
# animate_thinking()
# root.mainloop()

import threading
import time
result = {"answer": None}

def slow_ai(question):
    time.sleep(2)
    result["answer"] = "Відповідь на:" + question

def worker(text):
    current["answer"] = ask_ai(text)

def check_answer():
    if current["answer"] is None:
        root.after(100, check_answer)
        return
    show_answer(current["answer"])

def ask(text):
    current["answer"] = None
    set_emotion("thinking")
    threading.Thread(target=worker, args=(text,), daemon=True).start()
    check_answer()


thread = threading.Thread(target=slow_ai, args=("Що таке API"), daemon=True)
thread.start()
print("Запит пішов, а програма працює далі!")
thread.join()
print(result["answer"])
