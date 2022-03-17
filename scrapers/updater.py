from apscheduler.schedulers.background import BackgroundScheduler
from scrapers import news_scrapers
from asgiref.sync import sync_to_async, async_to_sync


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(news_scrapers.save_to_db, "interval", minutes=240)
    scheduler.start()
    news_scrapers.save_to_db()
