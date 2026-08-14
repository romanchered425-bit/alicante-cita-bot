import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

message = (
    "🤖 Alicante Cita Monitor запущено!\n\n"
    "Бот готовий до налаштування моніторингу Protección Temporal."
)

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message,
    },
    timeout=30,
)

response.raise_for_status()
print("Повідомлення успішно відправлено.")
