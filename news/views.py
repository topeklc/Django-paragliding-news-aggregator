from django.shortcuts import render
from scrapers.news_scrapers import save_to_db
from .models import NewsPost


def index(request):
    posts = NewsPost.objects.all()[:6]
    content = {"posts": posts}
    return render(request, "index.html", content)
