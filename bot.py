import asyncio
from pyrogram import Client, filters
import random

# اطلاعات اکانت
app = Client("my_account", 
             api_id=37609809, 
             api_hash="420c3cf1c6a30bdf9f9293481a167beb")

# لیست فحش‌ها
custom_words = ["فشار بخور 😂", "بیشرف", "دیوث", "کصننت", "سیکیم"]
enemies = set()

@app.on_message(filters.me & filters.command("p", "."))
async def ping(c, m):
    await m.edit("🚀 ربات بیدار شد!")

@app.on_message(filters.me & filters.command("en", "."))
async def enemy_toggle(c, m):
    if not m.reply_to_message: return
    uid = m.reply_to_message.from_user.id
    enemies.add(uid)
    await m.edit("👤 دشمن اضافه شد!")

@app.on_message(filters.incoming)
async def handle_enemies(c, m):
    if m.from_user and m.from_user.id in enemies:
        await m.reply(random.choice(custom_words))

# اجرای ربات بدون دردسر
if name == "main":
    app.run()
