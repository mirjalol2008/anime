import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from database import init_db, create_collection, add_file_to_collection, get_files_by_collection
from utils import generate_link_id

# --- Yuklashlar ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- Aiogram ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Global holat (admin session) ---
current_collection = None

# --- Boshlanishda DB yaratish ---
init_db()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    text = message.text
    if text.startswith("/start watch_"):
        collection_id = text.split("_")[1]
        files = get_files_by_collection(collection_id)
        if not files:
            return await message.answer("❌ Fayllar topilmadi.")
        await message.answer("📦 Yuklanmoqda...")
        for fid in files:
            try:
                await message.answer_video(fid)
            except:
                await message.answer_document(fid)
    else:
        await message.answer("👋 Bu bot orqali anime ko‘rishingiz mumkin.\nAdmin yuborgan linkni yuboring.")

@dp.message(F.text.lower() == "link")
async def create_link_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Bu buyruq faqat admin uchun.")
    global current_collection
    current_collection = generate_link_id()
    create_collection(current_collection)
    await message.answer(f"🔗 Yangi link yaratildi:\nhttps://t.me/{(await bot.get_me()).username}?start=watch_{current_collection}")

@dp.message(F.content_type.in_({'video', 'document'}))
async def admin_upload_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return  # faqat admin fayl yubora oladi

    global current_collection
    if not current_collection:
        return await message.answer("⛔ Avval 'link' deb yozib yangi to‘plam boshlang.")
    
    file_id = message.video.file_id if message.video else message.document.file_id
    add_file_to_collection(current_collection, file_id)
    await message.answer("✅ Fayl saqlandi.")

@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer("ℹ️ Fayl yuborish faqat admin uchun. Link orqali /start orqali anime ko‘rishingiz mumkin.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))