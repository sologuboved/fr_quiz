from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

from userinfo import TOKEN


CATEGORIE, INDICE, ACCENTS, MOTS = range(4)


async def start_and_ask_about_category(update, context):
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


async def learn_category_and_ask_about_index(update, context):
    categorie = update.message.text
    context.user_data['categorie'] = categorie
    await update.message.reply_text(
        f"D'accord, {categorie}.\n\nQuel indice ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return INDICE


async def learn_index_and_ask_about_accents(update, context):
    indice = update.message.text
    context.user_data['indice'] = indice
    await update.message.reply_text(
        f"D'accord, {indice}.\n\nEt les accents ?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ['Eigu', 'Grave', 'Circumflex'],
                ['Arbitraire', "N'importe"],
            ],
            one_time_keyboard=True,
            input_field_placeholder="Accents ?",
        ),
    )
    return ACCENTS


async def learn_accents_and_send_1st_word(update, context):
    accents = update.message.text
    context.user_data['accents'] = accents
    word = 'word'
    await update.message.reply_text(
        f"D'accord, {accents}.\n\n{word}",
        reply_markup=ReplyKeyboardRemove(),

    )
    return MOTS


async def send_words(update, context):
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
        entry_points=[CommandHandler("start", start_and_ask_about_category)],
        states={
            CATEGORIE: [MessageHandler(filters.Regex("^(Noms|Verbs|Adjectifs|Phrases|Tout)$"), learn_category_and_ask_about_index)],
            INDICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, learn_index_and_ask_about_accents)],
            MOTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, send_words)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    from helpers import write_pid

    pid_fname = write_pid()
    main()
