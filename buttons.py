from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎬 Kino qo‘shish", callback_data="add_movie"),
    ],
    [
        InlineKeyboardButton(text="📢 Reklama qilish", callback_data="send_ads"),
    ],
    [
        InlineKeyboardButton(text="📂 Hamma kinolar", callback_data="all_movies"),
    ]
])
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Admin menyu
admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🎬 Kino qo‘shish", callback_data="add_movie"),
    ],
    [
        InlineKeyboardButton(text="📢 Reklama qilish", callback_data="send_ads"),
    ],
    [
        InlineKeyboardButton(text="📂 Hamma kinolar", callback_data="all_movies"),
    ]
])

# Foydalanuvchi uchun telefon raqam yuborish tugmasi
phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Raqamni ulashish", request_contact=True)]
    ],
    resize_keyboard=True
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANNEL_USERNAME = "@kino_olamia"  # 🔴 kanal username (majburiy)

subscribe_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Obuna bo‘lish",
                url=f"https://t.me/{CHANNEL_USERNAME[1:]}"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Tekshirish",
                callback_data="check_sub"
            )
        ]
    ]
)

