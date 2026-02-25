import asyncio
import random
from pyrogram import Client, filters

# تنظیمات اصلی
app = Client("my_account", 
             api_id=37609809, 
             api_hash="420c3cf1c6a30bdf9f9293481a167beb")

# لیست کلمات فشاری و فحش‌ها
custom_words = [
    "فشار بخور 😂", "سطحت خیلی پایینه", "بیا پایین سرمون درد گرفت",
    "کص دالگت", "بیشرف", "زنازاده", "حرومزاده", "کصننت", "تخم حروم",
    "مادرجنده", "قیناده", "کیونی", "ننوی سیکیم", "دیوث", "گوت ورن", "هرزادیوی سیکیم",
    "سیحمرم", "سیکیم ازیوی", "سیح بین", "قورومساخ", "گوت", "سیحدیر", "ننه قهبه", "باجیوی سیکیم"
]
enemies = set()

@app.on_message(filters.me & filters.command("p", "."))
async def ping(c, m):
    await m.edit("🚀 ربات با قدرت آنلاین شد!")

@app.on_message(filters.me & filters.command("en", "."))
async def enemy_toggle(c, m):
    if not m.reply_to_message:
        await m.edit("رو پیام طرف ریپلای کن!")
        return
    uid = m.reply_to_message.from_user.id
    enemies.add(uid)
    await m.edit("👤 به لیست دشمن اضافه شد!")

@app.on_message(filters.incoming)
async def handle_enemies(c, m):
    if m.from_user and m.from_user.id in enemies:
        await m.reply(random.choice(custom_words))

if name == "main":
    app.run()
