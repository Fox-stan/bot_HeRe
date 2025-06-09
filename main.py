import os
import threading
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
)
from flask import Flask
from aiohttp import ClientSession, TCPConnector

from peewee import SqliteDatabase, Model, BigIntegerField, TextField

BOT_TOKEN = os.getenv("BOT_TOKEN")  # обязательно установи переменную окружения

# --- DATABASE SETUP ---

db = SqliteDatabase('db.sqlite3')


class User(Model):
    tg_id = BigIntegerField(unique=True)
    sub_id = TextField()

    def __repr__(self):
        return f"{self.tg_id} - {self.sub_id}"

    class Meta:
        database = db


class DBManager:

    @classmethod
    def initialize(cls):
        db.connect()
        db.create_tables([User], safe=True)
        db.close()

    @classmethod
    def add_user(cls, tg_id, sub_id) -> bool:
        try:
            user, created = User.get_or_create(tg_id=tg_id, defaults={'sub_id': sub_id})
            if not created:
                # Если пользователь уже есть, обновим sub_id (на случай, если он изменился)
                if user.sub_id != sub_id:
                    user.sub_id = sub_id
                    user.save()
                print(f'User {tg_id} already in db')
                return False
            else:
                print(f'User {tg_id} added to database')
                return True
        except Exception as e:
            print(f'Error in add_user: {e}')
            return False

    @classmethod
    def get_sub_id(cls, tg_id):
        try:
            user = User.get(User.tg_id == tg_id)
            return user.sub_id
        except User.DoesNotExist:
            return None


# --- FLASK APP ---

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Бот працює!"


def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)


# --- YOUR ORIGINAL CONSTANTS AND FUNCTIONS ---

CHANNELS = [
    -1002451226832,
    -1002599197728,
    -1002618219543,
    -1002669832980,
    -1002648070121,
    -1002688260177,
    -1002589814978,
    -1002566204798,
    -1002592832472,
    -1002640991456,
    -1002428903920,
    -1002644410680,
    -1002269277900,
]

POSTBACK_URL = "https://tele-check.lol/7fa6ffd/postback"

LINK_PODTV = "https://t.me/+mY3hHEOcA1hjNjll"
LINK_MUZH = "https://t.me/+78CQ-szbfq9iNjVl"
LINK_JENA = "https://t.me/+2O-E6-ujo05iMzJl"
PARTNER1 = "https://t.me/+yQnB4LWBmEw3Njdl"
PARTNER2 = "https://t.me/+po9rWTrL1dAzMTc1"
PARTNER3 = "https://t.me/+tVmHFavEeRw5YTBl"
REGION_LINKS = {
    'east': "https://t.me/+cmc5r38zfi5jYWU1",
    'central': "https://t.me/+j2qKmGqgaV81NjZl",
    'west': "https://t.me/+RV6bxd_J8S5iMDBl",
    'south': "https://t.me/+bZvcyN4hMa8xODI1",
    'north': "https://t.me/+b6O1CD4LeHQzYjFl",
}

(
    STEP_VACANCY, STEP_OTHER_TEXT, STEP_CONFIRM,
    STEP_GENDER, STEP_REGION, STEP_AGE, STEP_ABOUT, STEP_PARTNER
) = range(8)

user_data = {}


async def send_start_postback(sub_id):
    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            await session.get(f"{POSTBACK_URL}?subid={sub_id}&status=start_bot&from=bot")
    except Exception as e:
        print(e)


async def send_subscribe_postback(index, sub_id):
    try:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            await session.get(f"{POSTBACK_URL}?subid={sub_id}&status=subscribe{index+1}&from=bot")
    except Exception as e:
        print(e)


# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    subid = context.args[0] if context.args else "unknown"
    DBManager.add_user(chat_id, subid)
    await send_start_postback(subid)

    await update.message.reply_text(
        "👋 Вітаємо в “Гарячих вакансіях Україна”!\n"
        "На зараз терміново потрібні працівники:"
    )

    jobs = [
        ("Кур'єр", "v_kuryer", "40 000 грн", "Доставка замовлень пішки, на велосипеді або авто.\n✅ Досвід не обов’язковий\n✅ Видаємо самокат\n✅ Вільний графік"),
        ("Продавець", "v_prodavets", "45 000 грн","Робота в магазині: допомога покупцям, викладка товару.\n✅ Оплачувана відпустка✅ Видаємо самокат\n✅ Вільний графік"),
        ("Вантажник", "v_gruzchik", "43 000 грн", "Завантаження й розвантаження товару на складі/у магазині.\n✅ Фізична витривалість✅ Досвід не обов’язковий\n✅ Пунктуальність"),
        ("Касир", "v_kassir", "42 000 грн", "Робота в магазині: допомога покупцям, викладка товару.\n✅ Вільний графік✅ Досвід не обов’язковий\n✅ Вільний графік"),
    ]
    for title, data, salary, details in jobs:
        await context.bot.send_message(
            chat_id,
            f"🔥 {title} — {salary}\n{details}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Обрати", callback_data=data)]
            ])
        )

    await context.bot.send_message(
        chat_id,
        "Або залиш заявку на іншу вакансію",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Дивитись ще 26 вакансій", callback_data="other")]
        ])
    )
    return STEP_VACANCY


async def handle_vacancy_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    user_data[chat_id] = {"chosen_vacancy": query.data}

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open("2.jpeg", "rb"),
        caption="✅ Підтвердіть, що ви не бот, щоб почати пошук гарячих вакансій!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Підтвердити!", url=LINK_PODTV)]
        ])
    )

    await asyncio.sleep(3)
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open("3.jpeg", "rb"),
        caption="Оберіть вашу стать:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Чоловік", url=LINK_MUZH)],
            [InlineKeyboardButton("Жінка", url=LINK_JENA)]
        ])
    )
    await asyncio.sleep(3)
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open("4.jpeg", "rb"),
        caption="З якого ви регіону?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇦 Східна Україна", url=REGION_LINKS['east'])],
            [InlineKeyboardButton("🇺🇦 Центральна Україна", url=REGION_LINKS['central'])],
            [InlineKeyboardButton("🇺🇦 Західна Україна", url=REGION_LINKS['west'])],
            [InlineKeyboardButton("🇺🇦 Південна Україна", url=REGION_LINKS['south'])],
            [InlineKeyboardButton("🇺🇦 Північна Україна", url=REGION_LINKS['north'])],
        ])
    )
    await asyncio.sleep(3)
    await context.bot.send_message(chat_id, "Скільки вам років?")
    return STEP_AGE


async def handle_other_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id] = {"other_vacancy_text": update.message.text}
    return await handle_vacancy_choice(update, context)


async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['age'] = update.message.text
    await update.message.reply_text("Розкажіть трохи про себе або надішліть своє резюме!")
    return STEP_ABOUT


async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['about'] = update.message.text

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open("5.jpeg", "rb"),
        caption="Підпишіться на канали партнерів, щоб підвищити шанси:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🟤 Вектор | Україна", url=PARTNER1)],
            [InlineKeyboardButton("ФОКУС UA", url=PARTNER2)],
            [InlineKeyboardButton("🚨 Події LIVE", url=PARTNER3)],
            [InlineKeyboardButton("Відправити", callback_data='send_anyway')],
        ])
    )
    return STEP_PARTNER


async def handle_partner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Дякуємо! Ваше резюме вже у нас. Протягом 3-х днів з вами зв’яжеться наш рекрутер."
    )
    return ConversationHandler.END


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.chat_join_request.chat.id
        if chat_id in CHANNELS:
            idx = CHANNELS.index(chat_id)
            user_id = update.chat_join_request.from_user.id
            subid = DBManager.get_sub_id(user_id)
            await send_subscribe_postback(idx, subid)
    except Exception as e:
        print(e)


# --- Команды для работы с БД ---

async def db_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    test_sub_id = "test_subid123"
    status = DBManager.add_user(chat_id, test_sub_id)
    found = DBManager.get_sub_id(chat_id)
    await update.message.reply_text(f"✅ DB Test\nДодано: {status}\nЗнайдено sub_id: {found}")


async def get_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправить файл базы данных пользователю"""
    db_path = "db.sqlite3"
    if os.path.exists(db_path):
        await update.message.reply_document(open(db_path, "rb"))
    else:
        await update.message.reply_text("Файл бази даних не знайдено.")


# --- MAIN ---

def main():
    # Инициализация базы при старте бота
    DBManager.initialize()

    # Запускаем Flask в отдельном потоке
    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STEP_VACANCY: [CallbackQueryHandler(handle_vacancy_choice)],
            STEP_OTHER_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other_text)],
            STEP_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)],
            STEP_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_about)],
            STEP_PARTNER: [CallbackQueryHandler(handle_partner)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("dbtest", db_test))
    app.add_handler(CommandHandler("getdb", get_db))
    app.add_handler(ChatJoinRequestHandler(join_request))
    app.run_polling()


if __name__ == "__main__":
    main()
