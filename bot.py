import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
import pytz
import wikipedia

# --- تنظیمات اصلی ---
# اگر قبلاً api_id و api_hash خودت رو داشتی، می‌تونی جایگزین کنی
app = Client("my_account", 
             api_id=37609809, 
             api_hash="420c3cf1c6a30bdf9f9293481a167beb")

MY_NAME = "star"
config = {"prof": False, "antidel": False}
enemies = set()
unmsg_list = set()
custom_words = [
    "فشار بخور 😂", "سطحت خیلی پایینه، برو مشقاتو بنویس ✍️", "بیا پایین سرمون درد گرفت بابا 🤫",
    "فشار چیه داری می‌رقصی؟ 💃", "صدات نمیاد، بلندتر فشار بخور 📣", "حیف وقت که بخوام با تو بحث کنم 🚶‍♂️",
    "نبینم دپرس باشی، فشار بخور درست میشه 💊", "تو هنوز تو مرحله لودینگی، بمون تا برسی ⏳",
    "فشاری کی بودی تو؟ 🍼", "بیشرف", "زنازاده", "حرومزاده", "تخم حروم", "مادرجنده", "دیوث"
]

# --- حلقه ساعت (آپدیت اسم) ---
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
@app.on_message(filters.me & filters.command("help", "."))
async def help_cmd(c, m):
    await m.edit("📗 Star Bot Guide\n• .p : Ping\n• .c on/off : Clock Name\n• .ad on/off : Anti-Delete\n• .d [num] : Delete Msgs\n• .w [text] : Wikipedia\n• .en on/off : Enemy\n• .un on/off : Unmessage\n• .add [text] : Add Word")

@app.on_message(filters.me & filters.command("p", "."))
async def ping(c, m): await m.edit("🚀 Online!")

@app.on_message(filters.me & filters.command("c", "."))
async def clock_toggle(c, m):
    if len(m.command) < 2: return
    status = m.command[1].lower()
    config["prof"] = (status == "on")
    if status == "on": asyncio.create_task(clock_loop())
    await m.edit(f"⏰ Clock: {status.upper()}")

@app.on_message(filters.me & filters.command("ad", "."))
async def antidel_toggle(c, m):
    if len(m.command) < 2: return
    status = m.command[1].lower()
    config["antidel"] = (status == "on")
    await m.edit(f"🗑 Anti-Delete: {status.upper()}")

@app.on_message(filters.me & filters.command("d", "."))
async def delete_msgs(c, m):
    count = int(m.command[1]) if len(m.command) > 1 else 1
    async for message in c.get_chat_history(m.chat.id, limit=count + 1):
        if message.from_user and message.from_user.is_self: await message.delete()

@app.on_message(filters.me & filters.command("w", "."))
async def wiki_search(c, m):
    if len(m.command) < 2: return
    query = m.text.split(None, 1)[1]
    wikipedia.set_lang("fa")
    try:
        res = wikipedia.summary(query, sentences=2)
        await m.edit(f"🔍 Wiki: {res}")
    except: await m.edit("❌ Not Found")

@app.on_message(filters.me & filters.command("en", "."))
async def enemy_toggle(c, m):
    if not m.reply_to_message or len(m.command) < 2: return
    uid = m.reply_to_message.from_user.id
    status = m.command[1].lower()
    if status == "on": enemies.add(uid)
    else: enemies.discard(uid)
    await m.edit(f"👤 User {uid} Enemy: {status.upper()}")

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

@app.on_deleted_messages()
async def save_deleted(c, msgs):
    if config["antidel"]:
        for msg in msgs:
            if msg.text: await c.send_message("me", f"🗑 Deleted Msg:\n{msg.text}")

# --- اجرای نهایی (بدون بخش شرطی حساس) ---
print("--- STAR BOT STARTING... ---")
app.run()