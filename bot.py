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
    print('here!')
    categorie = update.message.text
    context.user_data['categorie'] = categorie
    await update.message.reply_text(
        f"D'accord, {categorie}.\n\nQuel indice ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return INDICE


async def learn_index_and_ask_about_accents_or_skip_and_send_1st_word(update, context):
    print('here!')
    indice = update.message.text
    context.user_data['indice'] = indice
    intro = f"D'accord, {indice}.\n\n"
    if context.user_data.get('categorie') == 'Phrases':
        word = 'word'
        await update.message.reply_text(
            f"{intro}{word}",
            reply_markup=ReplyKeyboardRemove(),
        )
        return MOTS
    await update.message.reply_text(
        f"{intro}Et les accents ?",
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
    print('here!')
    accents = update.message.text
    context.user_data['accents'] = accents
    word = 'word'
    await update.message.reply_text(
        f"D'accord, {accents}.\n\n{word}",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOTS


async def send_words(update, context):
    await update.message.reply_text(
        f"Some word",
        reply_markup=ReplyKeyboardRemove(),
    )
    return MOTS


async def skip(update, context):
    print(context.user_data)
    if 'indice' in context.user_data:
        point = ACCENTS
        to_skip = 'accents'
    elif 'categorie' in context.user_data:
        point = INDICE
        to_skip = 'indice'
    else:
        point = CATEGORIE
        to_skip = 'categorie'
    await update.message.reply_text(
        f"D'accord. Nous sautons {to_skip}.",
        # reply_markup=ReplyKeyboardRemove(),
    )
    print(point)
    return point


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
        entry_points=[CommandHandler("start", start_and_ask_about_category), CommandHandler("skip", skip)],
        states={
            CATEGORIE: [
                MessageHandler(
                    filters.Regex("^(Noms|Verbs|Adjectifs|Phrases|Tout)$"),
                    learn_category_and_ask_about_index,
                ),
                CommandHandler("skip", skip),
            ],
            INDICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    learn_index_and_ask_about_accents_or_skip_and_send_1st_word,
                ),
                CommandHandler("skip", skip),
            ],
            ACCENTS: [MessageHandler(
                filters.Regex("^(Eigu|Grave|Circumflex|Arbitraire|N'importe)$"),
                learn_accents_and_send_1st_word,
            ), CommandHandler("skip", skip)],
            MOTS: [MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                send_words,
            )],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    from helpers import write_pid

    pid_fname = write_pid()
    main()
