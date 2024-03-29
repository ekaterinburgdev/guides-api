from typing import List
from telegram.ext import CommandHandler, Updater, Handler

from .manuals_update_handler import update, help


class BotUpdater():
    def __init__(self, token) -> None:
        updater = Updater(token=token)
        self.updater = updater
        self.dispatcher = updater.dispatcher

        handlers = self._create_handlers()
        self._add_handlers(handlers)

    def _create_handlers(self) -> List[Handler]:
        yield CommandHandler("update", update, run_async=True)
        yield CommandHandler("help", help, run_async=True)
        
    def _add_handlers(self, handlers: List[Handler]) -> None:
        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def start_polling(self) -> None:
        self.updater.start_polling()
