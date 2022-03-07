from django.shortcuts import render
from scrapers.news_scrapers import save_to_db
from .models import NewsPost
from .utils import paginate_news


def index(request):
    posts = paginate_news(request)
    content = {"posts": posts}
    return render(request, "index.html", content)
