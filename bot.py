
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os
import random

# Токен Сквады
API_TOKEN = "7876359886:AAH50-gY1Ub2QEvXtQp6FiS1UlU2l3oPHXo"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Хранилище данных
users = {}

def get_user_data(user_id):
    if user_id not in users:
        users[user_id] = {"coins": 0, "beer": 0, "fish": 0, "ore": 0}
    return users[user_id]

# Команды
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Йоу! Я Сквада. Пиши /помощь, чтобы узнать, что я умею 😉")

@dp.message_handler(commands=["помощь"])
async def help_cmd(message: types.Message):
    await message.reply(
        "✨ Я умею:\n"
        "/копать — добыть руду\n"
        "/рыбачить — поймать рыбу\n"
        "/пиво — купить пиво (10 монет)\n"
        "/рейтинг — рейтинг по пиву\n"
        "/кошелёк — баланс\n"
        "\nRP-команды:\n"
        "/обнять @юзер\n"
        "/ударить @юзер\n"
        "/укусить @юзер\n"
        "/испугать @юзер\n"
        "/мурлыкать @юзер\n"
        "/схватить @юзер\n"
        "/ласкать @юзер\n"
        "/анекдот — расскажу прикол"
    )

@dp.message_handler(commands=["копать"])
async def dig(message: types.Message):
    user = get_user_data(message.from_user.id)
    amount = random.randint(5, 15)
    user["coins"] += amount
    user["ore"] += amount
    await message.reply(f"⛏️ Сквада выкопала для тебя {amount} руды! Теперь у тебя {user['coins']} монет.")

@dp.message_handler(commands=["рыбачить"])
async def fish(message: types.Message):
    user = get_user_data(message.from_user.id)
    amount = random.randint(3, 12)
    user["coins"] += amount
    user["fish"] += amount
    await message.reply(f"🎣 Ты поймал рыбку на {amount} монет! Всего у тебя {user['coins']} монет.")

@dp.message_handler(commands=["пиво"])
async def beer(message: types.Message):
    user = get_user_data(message.from_user.id)
    if user["coins"] >= 10:
        user["coins"] -= 10
        user["beer"] += 1
        await message.reply(f"🍺 Сквада налила тебе пива! Всего выпито: {user['beer']}")
    else:
        await message.reply("💸 Не хватает монет! Нужно 10.")

@dp.message_handler(commands=["кошелёк"])
async def wallet(message: types.Message):
    user = get_user_data(message.from_user.id)
    await message.reply(
        f"💼 Баланс:\nМонеты: {user['coins']}\nПиво: {user['beer']} 🍻\nРуда: {user['ore']} ⛏️\nРыба: {user['fish']} 🐟"
    )

@dp.message_handler(commands=["рейтинг"])
async def rating(message: types.Message):
    sorted_users = sorted(users.items(), key=lambda x: x[1]["beer"], reverse=True)
    text = "🏆 Топ пьющих Сквадиных пивунов:\n"
    for i, (uid, data) in enumerate(sorted_users[:10], start=1):
        try:
            user = await bot.get_chat(uid)
            name = user.first_name
        except:
            name = f"Пользователь {uid}"
        text += f"{i}. {name} — {data['beer']} 🍺\n"
    await message.reply(text or "Пока никто не пил пиво со Сквадой.")

rp_actions = {
    "обнять": "🤗 Сквада нежно обняла {user}. Ну всё, хватит, дальше сама!",
    "ударить": "🥊 Сквада смачно ударила {user}. Вот так!",
    "укусить": "🦷 Сквада укусила {user}. За ухо.",
    "испугать": "👻 Сквада испугала {user}! Бу!",
    "мурлыкать": "😻 Сквада мурлычет рядом с {user}. Приятно, да?",
    "схватить": "🫳 Сквада схватила {user} за шкирку. А ну стоять!",
    "ласкать": "💖 Сквада начала ласкать {user}. Хе-хе-хе..."
}

@dp.message_handler(commands=list(rp_actions.keys()))
async def rp_command(message: types.Message):
    cmd = message.get_command().lstrip("/")
    target = message.get_args() or message.from_user.first_name
    action_text = rp_actions.get(cmd, "").format(user=target)
    await message.reply(action_text)

jokes = [
    "— Сквада, ты где была?\n— В кэше. Очистили меня!",
    "Почему Сквада не пьёт чай? Потому что пиво — лучше!",
    "У Сквады нет багов. Есть фичи, от которых смешно."
]

@dp.message_handler(commands=["анекдот"])
async def joke(message: types.Message):
    await message.reply("🤣 " + random.choice(jokes))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
