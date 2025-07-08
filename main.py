import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from database import *
from utils import generate_link_id

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # .env fayldan olinadi

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

current_collection = None

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    text = message.text
    if text.startswith("/start watch_"):
        collection_id = text.split("_")[1]
        files = get_files_by_collection(collection_id)
        if not files:
            return await message.answer("❌ Hech narsa topilmadi.")
        await message.answer("📦 Yuklanmoqda...")
        for fid in files:
            try:
                await message.answer_video(fid)
            except:
                await message.answer_document(fid)
    else:
        await message.answer("🎬 Anime link orqali foydalaning.")

@dp.message(F.content_type.in_({'video', 'document'}))
async def handle_admin_file(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    global current_collection
    if not current_collection:
        await message.answer("❌ Avval `link` deb yozib yangi to‘plam boshlang.")
        return

    file_id = message.video.file_id if message.video else message.document.file_id
    add_file_to_collection(current_collection, file_id)
    await message.answer("✅ Fayl saqlandi.")

@dp.message(F.text.lower() == "link")
async def create_link(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    global current_collection
    current_collection = generate_link_id()
    create_collection(current_collection)
    await message.answer(f"🔗 Link tayyor: https://t.me/{(await bot.get_me()).username}?start=watch_{current_collection}")