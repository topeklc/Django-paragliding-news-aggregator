from .models import NewsPost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def paginate_news(request, news):
    page = request.GET.get("page")
    paginator = Paginator(news, 3)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        news = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        news = paginator.page(page)

    return news


def get_author(request):
    choosen_author = ""
    if request.GET.get("author"):
        choosen_author = request.GET.get("author")
    posts = NewsPost.objects.distinct().filter(Q(author__icontains=choosen_author))
    return posts, choosen_author
