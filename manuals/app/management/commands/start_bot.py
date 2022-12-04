import logging
from app.tg_bot.updater import BotUpdater

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.basicConfig(filename="logs",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        logging.info("Starting bot")
        

        # updater = BotUpdater(settings.TG_BOT_TOKEN)
        # updater.start_polling()
