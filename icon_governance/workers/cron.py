from time import sleep

from icon_governance.config import settings


def cron_worker():

    while True:
        sleep(settings.CRON_SLEEP_SEC)
