import os
import threading
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
)
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "✅ Бот працює!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

# ВСТАВ СВОЇ ПОСИЛАННЯ
LINK_KURYER = "https://t.me/YOUR_CHANNEL1"
LINK_PRODAVEC = "https://t.me/YOUR_CHANNEL2"
LINK_GRUZCHIK = "https://t.me/YOUR_CHANNEL3"
LINK_KASSIR = "https://t.me/YOUR_CHANNEL4"
LINK_OTHER = "https://t.me/YOUR_CHANNEL_OTHER"
LINK_PODTV = "https://t.me/YOUR_CHANNEL5"
LINK_MUZH = "https://t.me/YOUR_CHANNEL6"
LINK_JENA = "https://t.me/YOUR_CHANNEL7"
PARTNER1 = "https://t.me/YOUR_PARTNER1"
PARTNER2 = "https://t.me/YOUR_PARTNER2"
PARTNER3 = "https://t.me/YOUR_PARTNER3"

# Константы шагов анкеты
(
    STEP_VACANCY, STEP_OTHER, STEP_CONFIRM, STEP_VACANCY_TEXT, STEP_GENDER,
    STEP_REGION, STEP_AGE, STEP_ABOUT, STEP_PARTNER
) = range(9)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    user_data[chat_id] = {}

    await update.message.reply_text(
        "👋 Вітаємо в “Гарячих вакансіях Україна”!\n"
        "Ми працюємо тільки з перевіреними роботодавцями та рекрутерами — тому наші вакансії завжди актуальні й надійні.\n"
        "На зараз терміново потрібні працівники на такі позиції у 25 містах України:"
    )
    await context.bot.send_message(chat_id, "Терміново шукаємо працівників:")

    # Вакансія 1: Кур'єр
    await context.bot.send_message(
        chat_id,
        "🔥 Кур'єр — 40 000 грн\n"
        "Доставка замовлень пішки, на велосипеді або авто.\n"
        "✅ Досвід не обов’язковий\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_kuryer")]])
    )
    # Вакансія 2: Продавець
    await context.bot.send_message(
        chat_id,
        "🔥 Продавець — 45 000 грн\n"
        "Робота в магазині: допомога покупцям, викладка товару.\n"
        "✅ Оплачувана відпустка\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_prodavets")]])
    )
    # Вакансія 3: Вантажник
    await context.bot.send_message(
        chat_id,
        "🔥 Вантажник — 43 000 грн\n"
        "Завантаження й розвантаження товару на складі/у магазині.\n"
        "✅ Фізична витривалість\n"
        "✅ Досвід не обов’язковий\n"
        "✅ Пунктуальність",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_gruzchik")]])
    )
    # Вакансія 4: Касир
    await context.bot.send_message(
        chat_id,
        "🔥 Касир — 42 000 грн\n"
        "Робота в магазині: допомога покупцям, викладка товару.\n"
        "✅ Оплачувана відпустка\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_kassir")]])
    )

    # После вакансий — кнопка "Дивитись ще 26 вакансій"
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

    vacancy_map = {
        "v_kuryer": LINK_KURYER,
        "v_prodavets": LINK_PRODAVEC,
        "v_gruzchik": LINK_GRUZCHIK,
        "v_kassir": LINK_KASSIR,
        "other": LINK_OTHER
    }
    chosen = query.data
    user_data[chat_id]["chosen_vacancy"] = chosen

    # 8: подтверждение + фото (2.jpeg)
    with open("2.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="✅ Підтвердіть, що ви не бот, щоб почати пошук гарячих вакансій!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Підтвердити!", url=LINK_PODTV, callback_data="confirm")]
            ])
        )
    # Далее — ждем следующий шаг
    return STEP_CONFIRM

async def handle_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # 9: текстовая вакансия
    chat_id = update.effective_user.id
    await context.bot.send_message(
        chat_id,
        "Напишіть, яка вакансія вас цікавить!",
        reply_markup=ReplyKeyboardRemove()
    )
    return STEP_VACANCY_TEXT

async def handle_vacancy_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]["vacancy_text"] = update.message.text

    # 10: Вибір статі + фото (3.jpeg)
    with open("3.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Оберіть вашу стать:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Чоловік", url=LINK_MUZH, callback_data="male")],
                [InlineKeyboardButton("Жінка", url=LINK_JENA, callback_data="female")]
            ])
        )
    return STEP_GENDER

async def handle_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    # 11: Вибір регіону + фото (4.jpeg)
    with open("4.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="З якого ви регіону?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇦 Східна Україна", callback_data='region_east')],
                [InlineKeyboardButton("🇺🇦 Центральна Україна", callback_data='region_central')],
                [InlineKeyboardButton("🇺🇦 Західна Україна", callback_data='region_west')],
                [InlineKeyboardButton("🇺🇦 Південна Україна", callback_data='region_south')],
                [InlineKeyboardButton("🇺🇦 Північна Україна", callback_data='region_north')],
            ])
        )
    return STEP_REGION

async def handle_region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    region_map = {
        'region_east': "Східна Україна",
        'region_central': "Центральна Україна",
        'region_west': "Західна Україна",
        'region_south': "Південна Україна",
        'region_north': "Північна Україна",
    }
    region = region_map.get(query.data, "Інший")
    user_data[chat_id]['region'] = region

    # 12: Вік + фото (1.jpeg)
    with open("1.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Скільки вам років?"
        )
    return STEP_AGE

async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['age'] = update.message.text
    # 13: Про себе
    await update.message.reply_text("Розкажіть трохи про себе або надішліть своє резюме!")
    return STEP_ABOUT

async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['about'] = update.message.text

    # 14: Партнери + фото (5.jpeg)
    with open("5.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Щоб підвищити шанси знайти роботу та виділитись серед інших кандидатів — підпишіться на Telegram-канали наших партнерів:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Канал 1", url=PARTNER1, callback_data="p1")],
                [InlineKeyboardButton("Канал 2", url=PARTNER2, callback_data="p2")],
                [InlineKeyboardButton("Канал 3", url=PARTNER3, callback_data="p3")],
                [InlineKeyboardButton("Пропустити", callback_data='skip_partners')],
            ])
        )
    return STEP_PARTNER

async def handle_partner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "Дякуємо! Ваше резюме вже у нас. Протягом 3-х днів з вами зв’яжеться наш рекрутер.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    threading.Thread(target=run_flask, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STEP_VACANCY: [CallbackQueryHandler(handle_vacancy_choice)],
            STEP_CONFIRM: [CallbackQueryHandler(handle_confirm, pattern="confirm")],
            STEP_VACANCY_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vacancy_text)],
            STEP_GENDER: [CallbackQueryHandler(handle_gender, pattern="male|female")],
            STEP_REGION: [CallbackQueryHandler(handle_region, pattern="region_.*")],
            STEP_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)],
            STEP_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_about)],
            STEP_PARTNER: [CallbackQueryHandler(handle_partner, pattern="p1|p2|p3|skip_partners")],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
