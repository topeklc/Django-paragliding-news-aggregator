from django.shortcuts import render
from scrapers.news_scrapers import save_to_db
from .models import NewsPost
from .utils import paginate_news, get_author


def index(request):
    authors = NewsPost.objects.values("author")
    authors = sorted(list({author["author"] for author in authors}))
    posts, author = get_author(request)
    posts = paginate_news(request, posts)
    content = {"posts": posts, "authors": authors, "author": author}
    return render(request, "index.html", content)
