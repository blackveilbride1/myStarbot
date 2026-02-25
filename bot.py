import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import pytz
import wikipedia

# --- تنظیمات اصلی ---
app = Client("my_account", 
             api_id=37609809, 
             api_hash="420c3cf1c6a30bdf9f9293481a167beb")

# --- دیتابیس (همونایی که می‌خواستی) ---
MY_NAME = "star"
config = {"prof": False, "antidel": False}
enemies = set()
unmsg_list = set()
custom_words = [
    "فشار بخور 😂", "سطحت خیلی پایینه، برو مشقاتو بنویس ✍️", "بیا پایین سرمون درد گرفت بابا 🤫",
    "فشار چیه داری می‌رقصی؟ 💃", "صدات نمیاد، بلندتر فشار بخور 📣", "حیف وقت که بخوام با تو بحث کنم 🚶‍♂️",
    "نبینم دپرس باشی، فشار بخور درست میشه 💊", "تو هنوز تو مرحله لودینگی، بمون تا برسی ⏳",
    "فشاری کی بودی تو؟ 🍼", "کص دالگت", "بیشرف", "زنازاده", "حرومزاده", "کصننت", "تخم حروم",
    "مادرجنده", "قیناده", "کیونی", "ننوی سیکیم", "دیوث", "گوت ورن", "هرزادیوی سیکیم",
    "سیحمرم", "سیکیم ازیوی", "سیح بین", "قورومساخ", "گوت", "سیحدیر", "ننه قهبه", "باجیوی سیکیم"
]

# --- حلقه ساعت (بدون ارور) ---
async def clock_loop():
    while True:
        try:
            if config["prof"]:
                tehran_tz = pytz.timezone('Asia/Tehran')
                time_str = datetime.now(tehran_tz).strftime("%H:%M")
                await app.update_profile(first_name=f"{MY_NAME} | {time_str}")
            await asyncio.sleep(60)
        except:
            await asyncio.sleep(10)

# --- دستورات مدیریتی ---

@app.on_message(filters.me & filters.command("p", "."))
async def ping(c, m): await m.edit("🚀 Online & Powerful!")

@app.on_message(filters.me & filters.command("c", "."))
async def clock_toggle(c, m):
    if len(m.command) < 2: return
    status = m.command[1].lower()
    config["prof"] = (status == "on")
    await m.edit(f"⏰ Clock: {status.upper()}")

@app.on_message(filters.me & filters.command("d", "."))
async def delete_msgs(c, m):
    count = int(m.command[1]) if len(m.command) > 1 else 1
    async for message in c.get_chat_history(m.chat.id, limit=count + 1):
        if message.from_user and message.from_user.is_self: await message.delete()

@app.on_message(filters.me & filters.command("en", "."))
async def enemy_toggle(c, m):
    if not m.reply_to_message or len(m.command) < 2: return
    uid = m.reply_to_message.from_user.id
    status = m.command[1].lower()
    if status == "on": enemies.add(uid)
    else: enemies.discard(uid)
    await m.edit(f"👤 User {uid} Enemy: {status.upper()}")

@app.on_message(filters.me & filters.command("un", "."))
async def unmsg_toggle(c, m):
    if not m.reply_to_message or len(m.command) < 2: return
    uid = m.reply_to_message.from_user.id
    status = m.command[1].lower()
    if status == "on": unmsg_list.add(uid)
    else: unmsg_list.discard(uid)
    await m.edit(f"🚫 User {uid} Unmessage: {status.upper()}")

# --- پردازش خودکار پیام‌ها ---

@app.on_message(filters.incoming)
async def handle_incoming(c, m):
    if not m.from_user: return
    uid = m.from_user.id
    if uid in unmsg_list:
        await c.delete_user_history(m.chat.id, uid)
        return
    if uid in enemies:
        await m.reply(random.choice(custom_words))

# --- موتور روشن‌کننده (سازگار با رندر) ---
async def main():
    print("--- STAR BOT STARTING... ---")
    async with app:
        print("--- BOT IS LIVE NOW! ---")
        # اجرای ساعت در پس‌زمینه
        asyncio.create_task(clock_loop())
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
