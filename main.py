import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from buttons import phone_btn
from aiogram.client.session.aiohttp import AiohttpSession
import os
from aiogram.client.session.aiohttp import AiohttpSession



from config import TOKEN, ADMIN_ID
from database import init_db, add_user, get_user, add_movie
from state import AdminMovie
from movie_code import generate_move_code
from buttons import admin_menu
from state import AdminAds
from database import get_all_users
from database import get_all_movies
from database import get_movie_by_code
from buttons import phone_btn
from buttons import subscribe_btn
from aiogram import Bot
from aiogram import Bot

import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

# ENV dan olish
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
PROXY_URL = os.getenv("PROXY_URL")  # agar proxy ishlatmoqchi bo'lsangiz

# Session yaratish
session = AiohttpSession(proxy=PROXY_URL if PROXY_URL else None)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"), session=session)


logging.basicConfig(level=logging.INFO)



dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    is_subscribed = await check_subscription(bot, user_id)

    if not is_subscribed:
        await message.answer(
            f"👋 Assalomu alaykum <b>{full_name}</b>\n\n"
            "❗ Botdan foydalanish uchun kanalga obuna bo‘ling 👇",
            reply_markup=subscribe_btn
        )
        return

    await message.answer("✅ Xush kelibsiz! Film kodini yuboring 🎬")


    # 🔹 2. Foydalanuvchi bazada bormi?
    user = get_user(user_id)

    if user:
        await message.answer("🎬 Film kodini yuboring")
    else:
        await message.answer(
            "📞 Ro‘yxatdan o‘tish uchun raqamingizni yuboring 👇",
            reply_markup=phone_btn
        )




CHANNEL_USERNAME = "@kino_olamia"   # 👉 kanalingiz username

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """
    Foydalanuvchi kanalga obuna bo‘lganini tekshiradi
    True  → obuna bo‘lgan
    False → obuna bo‘lmagan
    """
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        # 🔍 Debug uchun (terminalda ko‘rasiz)
        print(f"USER {user_id} STATUS:", member.status)

        # ❌ Agar chiqib ketgan yoki bloklangan bo‘lsa
        if member.status in ["left", "kicked"]:
            return False

        # ✅ qolgan barcha statuslar obuna hisoblanadi
        return True

    except Exception as e:
        print("❌ SUBSCRIPTION ERROR:", e)
        return False





@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    is_subscribed = await check_subscription(bot, user_id)

    if is_subscribed:
        await callback.message.answer(
            "✅ Rahmat! Siz kanalga obuna bo‘lgansiz.\n\n📞 Endi raqamingizni yuboring",
            reply_markup=phone_btn
        )
    else:
        await callback.answer(
            "❌ Siz hali kanalga obuna bo‘lmagansiz",
            show_alert=True
        )











@dp.message(F.contact)
async def get_user_conatct(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    phone_number = message.contact.phone_number
    add_user(user_id, full_name, username, phone_number)
    await message.answer("<b><i>Ro'yxatdan o'tdingiz🥳🥳🥳</i>\nFilm kodini yuboring</b>", reply_markup=ReplyKeyboardRemove())



@dp.message(Command("admin"))
async def admin_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id == ADMIN_ID:
        await message.answer("Assalomu alaykum admin xush kelibsiz 👮")
        await message.answer(
            "Admin paneldan tanlang 👇",
            reply_markup=admin_menu
        )
    else:
        await message.answer("❌ Siz admin emassiz")



@dp.message(AdminMovie.movie_file, F.video)
async def get_movie_file(message: types.Message, state: FSMContext):
    movie_file = message.video.file_id
    await state.update_data(movie_file=movie_file)
    await message.answer("Film qabul qilindi\nTavsifini yuboring")
    await state.set_state(AdminMovie.movie_desc)



@dp.message(AdminMovie.movie_desc)
async def get_movie_desc(message: types.Message, state: FSMContext):
    movie_desc = message.text
    await state.update_data(movie_desc=movie_desc)

    data = await state.get_data()

    movie_file = data.get('movie_file')
    movie_desc = data.get('movie_desc')

    code = generate_move_code()

    lines = movie_desc.split('\n')
    new_lines = []

    for line in lines:  
        new_lines.append(line)
        if line.startswith("⚡️ Janri:"):
            new_lines.append(f"\n🔢 KINO KODI: {code}\n")

    final_desc = '\n'.join(new_lines)
    add_movie(movie_file, final_desc, code)
    await message.answer_video(movie_file, caption=final_desc)
    await message.answer("film yuklandi")
    await state.clear()

@dp.callback_query(F.data == "add_movie")
async def cb_add_movie(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("🎬 Film videosini yuboring")
    await state.set_state(AdminMovie.movie_file)
    await callback.answer()

from aiogram.types import ContentType

# Step 1: Admin reklama boshlaydi
@dp.callback_query(F.data == "send_ads")
async def cb_send_ads(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📢 Reklamani yuboring (matn, rasm yoki video)\n"
        "Shundan keyin ENTER bosing"
    )
    await state.set_state(AdminAds.wait_content)        
    await callback.answer()




# Step 2: Admin yuborgan har qanday kontentni saqlaymiz
@dp.message(AdminAds.wait_content, F.content_type.in_([ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO]))
async def get_ads_content(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        await state.update_data(text=message.text)
    elif message.content_type == ContentType.PHOTO:
        await state.update_data(file_id=message.photo[-1].file_id, file_type="photo", text=message.caption)
    elif message.content_type == ContentType.VIDEO:
        await state.update_data(file_id=message.video.file_id, file_type="video", text=message.caption)
    await message.answer("✅ Kontent qabul qilindi. Endi foydalanuvchilarga jo‘natiladi...")
    
    data = await state.get_data()
    users = get_all_users()
    success = 0

    for user in users:
        try:
            file_id = data.get("file_id")
            file_type = data.get("file_type")
            text = data.get("text", "")

            if file_id:
                if file_type == "photo":
                    await bot.send_photo(user[0], file_id, caption=text if text else None)
                elif file_type == "video":
                    await bot.send_video(user[0], file_id, caption=text if text else None)
            else:
                if text:
                    await bot.send_message(user[0], text)
            success += 1
        except Exception as e:
            print(f"Xato foydalanuvchiga yuborishda: {user[0]}, {e}")

    await message.answer(f"✅ Reklama yuborildi: {success} ta foydalanuvchiga")
    await state.clear()








@dp.callback_query(F.data == "all_movies")
async def cb_all_movies(callback: types.CallbackQuery):
    movies = get_all_movies()

    if not movies:
        await callback.message.answer("❌ Hali kino yo‘q")
        await callback.answer()
        return

    text = "📂 <b>Barcha kinolar:</b>\n\n"

    for movie in movies:
        code = movie[0]
        text += f"🎬 Kino kodi: <b>{code}</b>\n\n"

    await callback.message.answer(text)
    await callback.answer()


@dp.message(F.text.regexp(r"^\d+$"))
async def send_movie_by_code(message: types.Message):
    code = int(message.text)

    movie = get_movie_by_code(code)

    if not movie:
        await message.answer("❌ Bunday kodli kino topilmadi")
        return

    movie_file, movie_desc = movie
    await message.answer_video(
        video=movie_file,
        caption=movie_desc
    )


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())