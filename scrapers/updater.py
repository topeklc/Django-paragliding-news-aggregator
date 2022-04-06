from apscheduler.schedulers.background import BackgroundScheduler
from scrapers import news_scrapers


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(news_scrapers.save_to_db, "interval", minutes=60)
    scheduler.start()
    news_scrapers.save_to_db()
