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
)
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "✅ Бот працює!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

LINK_KURYER = "https://t.me/YOUR_CHANNEL1"
LINK_PRODAVEC = "https://t.me/YOUR_CHANNEL2"
LINK_GRUZCHIK = "https://t.me/YOUR_CHANNEL3"
LINK_KASSIR = "https://t.me/YOUR_CHANNEL4"
LINK_OTHER = "https://t.me/YOUR_CHANNEL_OTHER"
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    user_data[chat_id] = {}

    await update.message.reply_text(
        "👋 Вітаємо в “Гарячих вакансіях Україна”!\n"
        "Ми працюємо тільки з перевіреними роботодавцями та рекрутерами — тому наші вакансії завжди актуальні й надійні.\n"
        "На зараз терміново потрібні працівники на такі позиції у 25 містах України:"
    )
    await context.bot.send_message(chat_id, "Терміново шукаємо працівників:")

    await context.bot.send_message(
        chat_id,
        "🔥 Кур'єр — 40 000 грн\n"
        "Доставка замовлень пішки, на велосипеді або авто.\n"
        "✅ Досвід не обов’язковий\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_kuryer")]])
    )
    await context.bot.send_message(
        chat_id,
        "🔥 Продавець — 45 000 грн\n"
        "Робота в магазині: допомога покупцям, викладка товару.\n"
        "✅ Оплачувана відпустка\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_prodavets")]])
    )
    await context.bot.send_message(
        chat_id,
        "🔥 Вантажник — 43 000 грн\n"
        "Завантаження й розвантаження товару на складі/у магазині.\n"
        "✅ Фізична витривалість\n"
        "✅ Досвід не обов’язковий\n"
        "✅ Пунктуальність",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_gruzchik")]])
    )
    await context.bot.send_message(
        chat_id,
        "🔥 Касир — 42 000 грн\n"
        "Робота в магазині: допомога покупцям, викладка товару.\n"
        "✅ Оплачувана відпустка\n"
        "✅ Видаємо самокат\n"
        "✅ Вільний графік",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Обрати", callback_data="v_kassir")]])
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
    chosen = query.data
    user_data[chat_id]["chosen_vacancy"] = chosen

    with open("2.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="✅ Підтвердіть, що ви не бот, щоб почати пошук гарячих вакансій!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Підтвердити!", url=LINK_PODTV)]
            ])
        )
    await asyncio.sleep(3)

    if chosen.startswith('v_'):
        # Фото "стать" + пауза + регионы
        with open("3.jpeg", "rb") as img:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=img,
                caption="Оберіть вашу стать:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Чоловік", url=LINK_MUZH)],
                    [InlineKeyboardButton("Жінка", url=LINK_JENA)]
                ])
            )
        await asyncio.sleep(3)
        with open("4.jpeg", "rb") as img:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=img,
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
        return STEP_AGE
    else:
        await context.bot.send_message(
            chat_id,
            "Напишіть, яка вакансія вас цікавить!",
            reply_markup=ReplyKeyboardRemove()
        )
        return STEP_OTHER_TEXT

async def handle_other_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]["other_vacancy_text"] = update.message.text

    await asyncio.sleep(3)
    with open("3.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Оберіть вашу стать:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Чоловік", url=LINK_MUZH)],
                [InlineKeyboardButton("Жінка", url=LINK_JENA)]
            ])
        )
    await asyncio.sleep(3)
    with open("4.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
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
    return STEP_AGE

async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['age'] = update.message.text
    await update.message.reply_text("Розкажіть трохи про себе або надішліть своє резюме!")
    return STEP_ABOUT

async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['about'] = update.message.text

    with open("5.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Щоб підвищити шанси знайти роботу та виділитись серед інших кандидатів — підпишіться на Telegram-канали наших партнерів:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Канал 1", url=PARTNER1)],
                [InlineKeyboardButton("Канал 2", url=PARTNER2)],
                [InlineKeyboardButton("Канал 3", url=PARTNER3)],
                [InlineKeyboardButton("Пропустити", callback_data='skip_partners')],
            ])
        )
    await asyncio.sleep(3)
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
            STEP_OTHER_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other_text)],
            STEP_CONFIRM: [],
            STEP_GENDER: [],
            STEP_REGION: [],
            STEP_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_age)],
            STEP_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_about)],
            STEP_PARTNER: [CallbackQueryHandler(handle_partner, pattern="skip_partners")],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
