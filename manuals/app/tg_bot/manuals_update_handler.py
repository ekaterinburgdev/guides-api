import logging
from time import sleep
from telegram import Update
from telegram.ext import CallbackContext

from django.conf import settings

from app.internal.infrastructure.db_fill import db_update_v4, page_tree_update, prerender_page_elements, update_request


def update(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = update.effective_message.text.split()[1:]
    if chat_id != int(settings.TG_CHAT_TO_LISTEN) and chat_id != int(settings.TG_MASTER_ID):
        context.bot.send_message(chat_id=chat_id, text="Я тебе не подчиняюсь, дорогуша...")
        return
    if not settings.STATE.available:
        context.bot.send_message(chat_id=chat_id, text="Да я блин и так пытаюсь, че ты(")
        return

    request, error_msg = update_request.from_command(args)

    if not request:
        msg = error_msg if error_msg else "Чета пошло не так((((("
        context.bot.send_message(chat_id=chat_id, text=msg)
        return

    msg = "Капец ты жесткий...\nНу ладно, я попытаюсь" if request.force_update else "Окей, сейчас попробую обновить"
    context.bot.send_message(chat_id=chat_id, text=msg)
    try:
        settings.STATE.block()
        page_tree_update.update_page_tree()
        db_update_v4.check_db(request)
        prerender_page_elements.prerender_all()
        sleep(3)
        msg = "Прикинь, всё получилось 0_о" if request.force_update else "Вроде обновился"
        context.bot.send_message(chat_id=chat_id, text=msg)
    except Exception as e:
        logging.error(f"[Caching error]; {str(e)}")
        msg = "Всё потеряно, всё поламалось...\nhttps://godsaves.ru/molitva-o-spasenii-dushi/" if request.force_update else "Чета поломалось"
        context.bot.send_message(chat_id=chat_id, text=msg)
    finally:
        settings.STATE.unblock()

def help(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = '''Умею только апдейтить (я туповат)
\n/update --force [page_url]
\nФлаг --force опциональный, вкдючает форс - обновить все элементы страницы вне зависимости от времени последнего изменения. АПАСНА!
\nАргумент page_url опциональный. Если указан, то обновится страница по указанному урлу (в теории...).
Если не указан, то обновится всё.
\nПример использования: "/update --force facades/signboards"'''
    context.bot.send_message(chat_id=chat_id, text=msg)
