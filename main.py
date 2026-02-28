import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from buttons import menu, fanlar, sinflar
from sinf import sinf_soni

# ======================
# ENV YUKLASH
# ======================
load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylida topilmadi!")

ADMIN_ID = getenv("ADMIN_ID")
if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID .env faylida topilmadi!")

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("❌ ADMIN_ID faqat raqam bo‘lishi kerak!")

# ======================
# BOT VA DISPATCHER
# ======================
dp = Dispatcher()

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# ======================
# /start
# ======================
@dp.message(Command("start"))
async def start(message: Message):
    text = f"""
<b>Assalomu alaykum, {message.from_user.full_name}! 👋</b>

🏫 <b>1-sonli umumiy o‘rta ta’lim maktabining rasmiy botiga xush kelibsiz!</b>

Quyidagi menyulardan birini tanlang 👇
"""
    await message.answer(text, reply_markup=menu)


# ======================
# Maktab haqida
# ======================
@dp.message(F.text == "1-maktab haqida🏨")
async def about(msg: Message):
    text = """
<b>🏫 1-sonli umumiy o‘rta ta’lim maktabi</b>

📍 Manzil: Sirdaryo viloyati, Mirzaobod tumani  
📅 Tashkil topgan: 1995-yil  
👨‍🏫 O‘qituvchilar soni: 45+  
👩‍🎓 O‘quvchilar soni: 600+  

✨ Zamonaviy ta’lim tizimi  
✨ Fan olimpiadalari ishtirokchilari  
✨ Sport va ma’naviy tadbirlar faol
"""
    await msg.answer(text)


# ======================
# Fanlar
# ======================
@dp.message(F.text == "📚Fanlar")
async def courses(msg: Message):
    text = """
<b>📚 Maktabimiz fanlari:</b>

📘 Matematika  
📗 Ona tili  
📕 Ingliz tili  
🌍 Tarix  
🧪 Kimyo  
⚡ Fizika  
💻 Informatika  
🏃 Jismoniy tarbiya  

Fan tanlang 👇
"""
    await msg.answer(text, reply_markup=fanlar)


# ======================
# Sinflar
# ======================
@dp.message(F.text == "Sinflar")
async def classes(msg: Message):
    text = """
<b>🏫 Maktab sinflari</b>

1–11-sinflar mavjud.

Sinfni tanlang 👇
"""
    await msg.answer(text, reply_markup=sinflar)


# ======================
# Sinf o‘quvchi soni
# ======================
@dp.message(F.text.in_(sinf_soni.keys()))
async def sinf_soni_chiqar(msg: Message):
    sinf = msg.text
    soni = sinf_soni[sinf]

    text = f"""
<b>📊 {sinf} haqida ma’lumot</b>

👩‍🎓 O‘quvchilar soni: <b>{soni} ta</b>
📚 Ta’lim sifati: Yuqori darajada
"""
    await msg.answer(text)


# ======================
# Orqaga
# ======================
@dp.message(F.text == "🔙orqaga")
async def back(msg: Message):
    await msg.answer("<b>🔙 Asosiy menyu</b>", reply_markup=menu)


# ======================
# Manzil
# ======================
@dp.message(F.text == "📍Manzilimiz:")
async def location(msg: Message):
    await msg.answer("Bizning manzilimiz:")
    await msg.answer_location(40.49533310808186, 68.70414287047306)



# ======================
# Telefon qabul qilish
# ======================
@dp.message(F.contact)
async def send_contact(msg: Message):
    phone = msg.contact.phone_number
    name = msg.contact.full_name
    username = msg.from_user.username or "Mavjud emas"

    matn = f"""
📥 <b>Yangi ariza</b>

👤 Ismi: {name}
📱 Telefon: {phone}
🔗 Username: @{username}
"""

    try:
        await bot.send_message(chat_id=ADMIN_ID, text=matn)
    except Exception as e:
        print("Xabar yuborilmadi:", e)

    await msg.answer("✅ <b>Rahmat!</b>\nTez orada siz bilan bog‘lanamiz ❤️")


# ======================
# BOTNI ISHGA TUSHIRISH
# ======================
async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())