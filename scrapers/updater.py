from apscheduler.schedulers.background import BackgroundScheduler
from scrapers import news_scrapers
from datetime import datetime
from time import time


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        news_scrapers.save_to_db,
        "interval",
        start_date=str(datetime.fromtimestamp(int(time() + 300))),
    )
    scheduler.start()
