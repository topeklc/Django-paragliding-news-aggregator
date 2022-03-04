from django.shortcuts import render
from scrapers.news_scrapers import save_to_db
from scrapers import news_scrapers


def index(request):
    # news_scrapers.save_to_db()
    return render(request, "index.html")
