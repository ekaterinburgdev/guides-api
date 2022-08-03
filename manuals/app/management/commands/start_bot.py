from app.tg_bot.updater import BotUpdater

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = BotUpdater(settings.TG_BOT_TOKEN)
        updater.start_polling()
