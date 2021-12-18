from datetime import datetime, timedelta
from functools import partial
import html
import json
import logging
import os
import traceback

import telegram

from . import actions, statuses


ACTION_HANDLER = {
    "next-update": actions.next_update,
    "update": actions.update_status,
    "clear": actions.clear,
}

logging.basicConfig(format="%(name)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def help_command(update, context):
    update.message.reply_text("Type /start to test this bot.")


def start(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton(file, callback_data=f"{file}.txt")
            for file in ["disk-usage", "docker-ps", "docker-stats"]
        ],
        [
            telegram.InlineKeyboardButton(action, callback_data=action)
            for action in ACTION_HANDLER
        ],
        [
            telegram.InlineKeyboardButton(
                f"{service}-status", callback_data=f"status-{service}.json"
            )
            for service in actions.STATUS_HANDLER
        ],
        [
            telegram.InlineKeyboardButton(
                f"{service_name}-error", callback_data=f"error-{service_name}.json"
            )
            for service_name in actions.STATUS_HANDLER
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if not update.effective_user.id == int(os.environ["USER_ID"]):
        return query.edit_message_text(text="Not authorized.")

    if auto_updater_collision(query.edit_message_text, context):
        return

    if query.data.endswith((".txt", ".json")):
        path = statuses.LOG_PATH / query.data
        if path.is_file():
            with path.open(mode="r") as f:
                query.edit_message_text(
                    text=f"<pre><code>{html.escape(f.read())}</code></pre>",
                    parse_mode=telegram.ParseMode.HTML,
                )
        else:
            query.edit_message_text(text=f"ERROR [file] {query.data} not found.")

    else:
        ACTION_HANDLER[query.data](msg_func=query.message.reply_text, context=context)
        query.edit_message_text(text="Done.")


def auto_updater(context):
    msg_func = partial(context.bot.send_message, chat_id=os.environ["CHAT_ID"])
    try:
        me = context.bot.get_chat_member(
            os.environ["CHAT_ID"], int(os.environ["USER_ID"])
        )
        if not me.status == "member":
            msg_func(text="Not authorized.")
            return
    except telegram.error.BadRequest:
        msg_func(text="Not authorized.")
        return

    actions.update_status(msg_func, context)


def auto_updater_collision(msg_func, context):
    delta = timedelta(seconds=10)
    current_jobs = context.job_queue.get_jobs_by_name("auto_updater")
    if (
        current_jobs
        and abs(current_jobs[0].next_t - datetime.now(statuses.TIMEZONE)) < delta
    ):
        msg_func(
            text=f"Please wait, next update: {current_jobs[0].next_t:%Y-%m-%d %H:%M}"
        )
        return True
    return False


def error_handler(update, context):
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    update_str = (
        update.to_dict() if isinstance(update, telegram.Update) else str(update)
    )
    message = (
        f"An exception was raised while handling an update:\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    context.bot.send_message(
        chat_id=os.environ["CHAT_ID"], text=message, parse_mode=telegram.ParseMode.HTML
    )
