from aiogram.fsm.state import State, StatesGroup

# 🎬 Film qo‘shish
class AdminMovie(StatesGroup):
    movie_file = State()
    movie_desc = State()

# 📢 Rekлама yuborish
class AdminAds(StatesGroup):
    wait_content = State()
