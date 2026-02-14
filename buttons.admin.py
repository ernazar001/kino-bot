from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Kino qo‘shish", callback_data="add_movie")],
        [InlineKeyboardButton(text="📢 Reklama qilish", callback_data="send_ads")],
        [InlineKeyboardButton(text="📂 Hamma kinolar", callback_data="all_movies")]
    ]
)
