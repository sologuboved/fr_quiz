from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from userinfo import TOKEN


CATEGORIE, INDICE, MOTS = range(3)


async def start(update, context):
    await update.message.reply_text(
        "Choisissez la catégorie",
        reply_markup=ReplyKeyboardMarkup(
            [
                ['Noms', 'Verbs'],
                ['Adjectifs', 'Phrases'],
                ['Tout'],
            ],
            one_time_keyboard=True,
            input_field_placeholder="Catégorie ?",
        ),
    )
    return CATEGORIE


async def learn_category(update, context):
    categorie = update.message.text
    context.user_data['categorie'] = categorie
    await update.message.reply_text(
        f"D'accord, {categorie}.\n\nQuel indice ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return INDICE


async def learn_index(update, context):
    indice = update.message.text
    context.user_data['indice'] = indice
    word = 'word'
    await update.message.reply_text(
        f"D'accord, {indice}.\n\n{word} ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOTS


async def send(update, context):
    print('!!', context.user_data['categorie'])
    await update.message.reply_text(
        f"Some word",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOTS


async def cancel(update, context):
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "D'accord, reviens bientôt !",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORIE: [MessageHandler(filters.Regex("^(Noms|Verbs|Adjectifs|Phrases|Tout)$"), learn_category)],
            MOTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    from helpers import write_pid

    pid_fname = write_pid()
    main()
