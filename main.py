import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ChatJoinRequestHandler,
    ContextTypes,
)
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")

user_contexts = {}

# Flask-сервер для UptimeRobot
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Бот працює!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# ——— Хендлер для заявки на вступление
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = user.id
    username = user.first_name

    user_contexts[chat_id] = {
        "username": username
    }

    # Заменить на юзернейм своего бота!
    start_link = "https://t.me/Nst_auto_bot?start=ok"
    caption = (
        f"{username}, потрібно натиснути "
        f"<a href='{start_link}'>/start</a>. "
        f"Після чого ваша заявка буде вам повторно надіслана."
    )

    with open("2.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=caption,
            parse_mode="HTML"
        )

# ——— Хендлер для /start в личке
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    username = update.effective_user.first_name

    # Можете использовать сохраненное имя, если нужно:
    # username = user_contexts.get(chat_id, {}).get("username", update.effective_user.first_name)

    # 1
    with open("1.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"""{username}, УВАГА❗️
ОБОВʼЯЗКОВА ПЕРЕВІРКА!

👇 Підтвердіть, що вам є 18 років?""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Мені є 18 ✅", url="https://t.me/+9HZXshlGyOZiMGVl")],
                [InlineKeyboardButton("Мені немає 18 ❌", url="https://t.me/+_41Qv55A-X84MGE9")],
                [InlineKeyboardButton("Пропустити", url="https://t.me/+mqiW2ngd--Y1Y2U1")],
            ])
        )
    await asyncio.sleep(3)

    # 2
    with open("6.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"""{username}, УВАГА❗️
ОБОВʼЯЗКОВА ПЕРЕВІРКА!

👇 Підтвердіть, що вам є 18 років?""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ДИВИТИСЯ ВІДЕО", url="https://t.me/+rmaupgN4ZDcyMGZl")],
                [InlineKeyboardButton("ЗАЛИШИТИ КОМЕНТАР", url="https://t.me/+rmaupgN4ZDcyMGZl")],
            ])
        )
    await asyncio.sleep(3)

    # 3
    message = await context.bot.send_message(chat_id=chat_id, text="Запит знаходиться в обробці...⌛")
    await asyncio.sleep(3)
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    # 4
    with open("3.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"""💬 Коментарі соцмереж вже вибухають

Це відео побачив кожен другий українець — а ти ще ні?

Не залишайся осторонь!""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Я ЖІНКА 👩", url="https://t.me/+YHtR-mrnU_4yZGE1")],
                [InlineKeyboardButton("Я ЧОЛОВІК 👨", url="https://t.me/+N6_OqsI5JoJkZmRl")],
            ])
        )
    await asyncio.sleep(2)

    # 5
    message = await context.bot.send_message(chat_id=chat_id, text="У вас залишилось 10 секунд ☝️")
    await asyncio.sleep(10)
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

    # 6
    with open("4.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"{username}, Оберіть свою область!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇦 Східна Україна", url="https://t.me/+8RSGQFhllDgwMzI1")],
                [InlineKeyboardButton("🇺🇦 Центральна Україна", url="https://t.me/+kTrA8INEr_41Y2E1")],
                [InlineKeyboardButton("🇺🇦 Західна Україна", url="https://t.me/+_JU73CfrepM0Y2M9")],
                [InlineKeyboardButton("🇺🇦 Південна Україна", url="https://t.me/+Qm7nbtxBfh83NTVl")],
                [InlineKeyboardButton("🇺🇦 Північна Україна", url="https://t.me/+snd6k-IWzKJmY2M1")],
            ])
        )

    # 7
    with open("5.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=f"""🔔 {username}, Ваша заявка схвалена,
для отримання доступу натисніть «ПІДТВЕРДИТИ»""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ПІДТВЕРДИТИ ✅", url="https://t.me/+5rBW_rjAAPw3OTQ9")],
            ])
        )

def main():
    threading.Thread(target=run_flask).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CommandHandler("start", handle_start))
    app.run_polling()

if __name__ == "__main__":
    main()
