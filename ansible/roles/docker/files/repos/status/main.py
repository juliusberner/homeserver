import os

from telegram import ext

from telegram_status import bot
from telegram_status.statuses import TIMEZONE


UPDATE_INTERVAL = int(os.environ.get("UPDATE_INTERVAL", 300))


def run():
    # Create the Updater and pass it your bot's token.
    defaults = ext.Defaults(tzinfo=TIMEZONE)
    updater = ext.Updater(os.environ["BOT_ID"], use_context=True, defaults=defaults)

    filters = (
        ext.Filters.chat_type.private
        & ext.Filters.chat(chat_id=int(os.environ["CHAT_ID"]))
        & ext.Filters.user(int(os.environ["USER_ID"]))
    )
    updater.dispatcher.add_handler(
        ext.CommandHandler("start", bot.start, filters=filters)
    )
    updater.dispatcher.add_handler(ext.CallbackQueryHandler(bot.button))
    updater.dispatcher.add_handler(
        ext.CommandHandler("help", bot.help_command, filters=filters)
    )
    updater.dispatcher.add_error_handler(bot.error_handler)

    # Start the Bot
    updater.job_queue.run_repeating(bot.auto_updater, interval=UPDATE_INTERVAL)
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    run()
