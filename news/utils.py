from .models import NewsPost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate_news(request):
    news = NewsPost.objects.all()
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
