from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from userinfo import TOKEN


CATEGORIE = 0


async def start(update, context):
    reply_keyboard = [
        ['Noms', 'Verbs'],
        ['Adjectifs', 'Phrases'],
        ['Tout'],
    ]
    await update.message.reply_text(
        "Choisissez la catégorie",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Catégorie ?",
        ),
    )
    return CATEGORIE


async def launch(update, context):
    categorie = update.message.text
    await update.message.reply_text(
        f"D'accord, {categorie}",
        reply_markup=ReplyKeyboardRemove(),
    )
    while True:
        reply = await send_words(update, context)
        if reply.lower() == 'assez':
            await context.bot.send_message(chat_id=update.message.chat_id, text="")
            break


async def send_words(update, context):
    return 'assez'


async def cancel(update, context):
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "D'accord, reviens bientôt !", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORIE: [MessageHandler(filters.Regex("^(Noms|Verbs|Adjectifs|Phrases|Tout)$"), launch)],
            # PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            # LOCATION: [
            #     MessageHandler(filters.LOCATION, location),
            #     CommandHandler("skip", skip_location),
            # ],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    from helpers import write_pid

    pid_fname = write_pid()
    main()
