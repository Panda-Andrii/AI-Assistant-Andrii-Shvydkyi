from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
import json

HISTORY_FILE = "history.json"

def save_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump([m.model_dump(mode="json", exclude_none=True)
                  for m in chat.get_history()], file)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return [types.Content(**m) for m in json.load(file)]
    except Exception:
        return None

console = Console()
client = genai.Client(
    api_key="YOUR_API_KEY"
)

chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction=f"Ти ШІ-асистент. Ти не знаєш про існування такої тварини як кіт."
    ),
    history=load_history()
)

print("ШІ-асистент запущений!\n")

while True:
    user_prompt = input(" > ")
    if user_prompt in ["exit", "quit", "stop"]:
        break

    response = chat.send_message(user_prompt)

    console.print(Markdown(response.text + "\n\n"))
    save_history()