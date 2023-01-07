import logging
from time import sleep
from telegram import Update
from telegram.ext import CallbackContext

from django.conf import settings

from app.internal.infrastructure.db_fill import db_update_v4, page_tree_update, prerender_page_elements


def force_update_pages(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != int(settings.TG_CHAT_TO_LISTEN) and chat_id != int(settings.TG_MASTER_ID):
        context.bot.send_message(chat_id=chat_id, text="Я тебе не подчиняюсь, дорогуша...")
        return
    if not settings.STATE.available:
        context.bot.send_message(chat_id=chat_id, text="Да я блин и так пытаюсь, че ты(")
        return
    context.bot.send_message(chat_id=chat_id, text="Капец ты жесткий...\nНу ладно, я попытаюсь")
    try:
        settings.STATE.block()
        page_tree_update.update_page_tree()
        db_update_v4.check_db(force_update=True)
        prerender_page_elements.prerender_all()
        sleep(3)
        context.bot.send_message(chat_id=chat_id, text="Прикинь, всё получилось 0_о")
    except Exception as e:
        logging.error(f"Caching error; {str(e)}")
        context.bot.send_message(chat_id=chat_id, text="Всё потеряно, всё поламалось...\nhttps://godsaves.ru/molitva-o-spasenii-dushi/")
    finally:
        settings.STATE.unblock()

def update_pages(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != int(settings.TG_CHAT_TO_LISTEN) and chat_id != int(settings.TG_MASTER_ID):
        context.bot.send_message(chat_id=chat_id, text="Я тебе не подчиняюсь, дорогуша...")
        return
    if not settings.STATE.available:
        context.bot.send_message(chat_id=chat_id, text="Зайка, я и так обновляюсь...")
        return
    context.bot.send_message(chat_id=chat_id, text="Окей, сейчас попробую обновить")
    try:
        settings.STATE.block()
        page_tree_update.update_page_tree()
        db_update_v4.check_db()
        prerender_page_elements.prerender_all()
        sleep(3)
        context.bot.send_message(chat_id=chat_id, text="Вроде обновился")
    except Exception as e:
        logging.error(f"Caching error; {str(e)}")
        context.bot.send_message(chat_id=chat_id, text="Чета поломалось")
    finally:
        settings.STATE.unblock()