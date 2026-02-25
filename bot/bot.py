# bot/bot.py
import os
import asyncio
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)

async def send_notification(text):
    await bot.send_message(ADMIN_ID, text)

def notify_new_guest(guest):
    text = f"""
🎉 Новая анкета!

👤 {guest.full_name}
✅ Придёт: {"Да" if guest.will_come else "Нет"}
🍷 Алкоголь: {guest.alcohol_preference}
💬 Комментарий: {guest.comment}
"""
    asyncio.run(send_notification(text))
