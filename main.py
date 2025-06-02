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

(
    STEP1, STEP2, STEP3, STEP4, STEP5, STEP6,
    STEP7, STEP8, STEP9, STEP10, STEP11, STEP12, STEP13
) = range(13)

# Встав свої посилання!
LINK_KURYER = "https://t.me/YOUR_CHANNEL1"
LINK_PRODAVEC = "https://t.me/YOUR_CHANNEL2"
LINK_GRUZCHIK = "https://t.me/YOUR_CHANNEL3"
LINK_KASSIR = "https://t.me/YOUR_CHANNEL4"
LINK_PODTV = "https://t.me/YOUR_CHANNEL5"
LINK_MUZH = "https://t.me/YOUR_CHANNEL6"
LINK_JENA = "https://t.me/YOUR_CHANNEL7"
PARTNER1 = "https://t.me/YOUR_PARTNER1"
PARTNER2 = "https://t.me/YOUR_PARTNER2"
PARTNER3 = "https://t.me/YOUR_PARTNER3"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    chat_id = user.id
    user_data[chat_id] = {}

    text = (
        "👋 Вітаємо в “Гарячих вакансіях Україна”!\n"
        "Ми працюємо тільки з перевіреними роботодавцями та рекрутерами — тому наші вакансії завжди актуальні й надійні.\n"
        "На зараз терміново потрібні працівники на такі позиції у 25 містах України:"
    )
    await update.message.reply_text(text)
    await context.bot.send_message(chat_id, "Терміново шукаємо працівників:")

    keyboard = [
        [InlineKeyboardButton("🔥 Кур'єр — 40 000 грн", callback_data='kur')],
        [InlineKeyboardButton("🔥 Продавець — 45 000 грн", callback_data='prod')],
        [InlineKeyboardButton("🔥 Вантажник — 43 000 грн", callback_data='gruz')],
        [InlineKeyboardButton("🔥 Касир — 42 000 грн", callback_data='kas')],
        [InlineKeyboardButton("Дивитись ще 26 вакансій", callback_data='other')]
    ]
    await context.bot.send_message(
        chat_id,
        "Оберіть вакансію:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return STEP1

async def vacancy_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    vacancy_map = {
        'kur': ("🔥 Кур'єр — 40 000 грн\nДоставка замовлень пішки, на велосипеді або авто.\n"
                "✅ Досвід не обов’язковий\n✅ Видаємо самокат\n✅ Вільний графік", LINK_KURYER),
        'prod': ("🔥 Продавець — 45 000 грн\nРобота в магазині: допомога покупцям, викладка товару.\n"
                 "✅ Оплачувана відпустка\n✅ Видаємо самокат\n✅ Вільний графік", LINK_PRODAVEC),
        'gruz': ("🔥 Вантажник — 43 000 грн\nЗавантаження й розвантаження товару на складі/у магазині.\n"
                 "✅ Фізична витривалість\n✅ Досвід не обов’язковий\n✅ Пунктуальність", LINK_GRUZCHIK),
        'kas': ("🔥 Касир — 42 000 грн\nРобота в магазині: допомога покупцям, викладка товару.\n"
                "✅ Оплачувана відпустка\n✅ Видаємо самокат\n✅ Вільний графік", LINK_KASSIR),
        'other': ("Або залиш заявку на іншу вакансію", None)
    }
    vacancy, link = vacancy_map.get(query.data, ("", None))
    user_data[chat_id]['vacancy'] = query.data

    if link:
        await query.message.reply_text(vacancy, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Обрати", url=link)]
        ]))
    else:
        await query.message.reply_text(vacancy)

    # 8 повідомлення з фото
    with open("2.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="✅ Підтвердіть, що ви не бот, щоб почати пошук гарячих вакансій!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Підтвердити!", url=LINK_PODTV)]
            ])
        )

    await context.bot.send_message(
        chat_id,
        "Напишіть, яка вакансія вас цікавить!",
        reply_markup=ReplyKeyboardRemove()
    )
    return STEP2

async def vacancy_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['vacancy_text'] = update.message.text

    # 10 повідомлення з фото
    with open("3.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Оберіть вашу стать:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Чоловік", url=LINK_MUZH)],
                [InlineKeyboardButton("Жінка", url=LINK_JENA)],
            ])
        )
    return STEP3

async def gender_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    # 11 повідомлення з фото
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
    return STEP4

async def region_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
    region = region_map.get(query.data)
    user_data[chat_id]['region'] = region

    # 12 повідомлення з фото
    with open("1.jpeg", "rb") as img:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption="Скільки вам років?"
        )
    return STEP5

async def age_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['age'] = update.message.text
    await update.message.reply_text("Розкажіть трохи про себе або надішліть своє резюме!")
    return STEP6

async def about_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_user.id
    user_data[chat_id]['about'] = update.message.text

    # 14 повідомлення з фото
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
    return STEP7

async def partner_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
            STEP1: [CallbackQueryHandler(vacancy_selected)],
            STEP2: [MessageHandler(filters.TEXT & ~filters.COMMAND, vacancy_input)],
            STEP3: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender_selected)],
            STEP4: [CallbackQueryHandler(region_selected)],
            STEP5: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_input)],
            STEP6: [MessageHandler(filters.TEXT & ~filters.COMMAND, about_input)],
            STEP7: [CallbackQueryHandler(partner_selected)],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
