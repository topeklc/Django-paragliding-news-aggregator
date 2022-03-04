import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
from news.models import NewsPost

calendar = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sept": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def get_xcmag():
    page = requests.get("https://xcmag.com/news/").text
    soup = bs(page, "html.parser")
    soup.find_all("li")
    first_news = soup.find_all(class_="grid")[0].find_all("li")[0]
    news_title = first_news.h2.text
    short_description = first_news.p.text
    news_link = first_news.a["href"]
    date = (
        bs(requests.get(news_link).text, "html.parser")
        .find_all(class_="single-post-meta")[1]
        .text.replace("\\", "")
        .replace("\n", "")
        .strip()
    )
    date = date.split()
    date = "-".join([date[1], calendar[date[2][:3].lower()], date[3]])
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    media_link = first_news.a.img["src"]

    return "XCmag", date, epoch, news_title, short_description, news_link, media_link


def get_flybgd():
    page = requests.get(
        "https://www.flybgd.com/en/paragliders/news-wings-gliders-6-0-0.html"
    )
    soup = bs(page.text, "html.parser")
    first_news = soup.find_all(class_="row")[2]
    news_title = first_news.find("h3").text
    short_description = first_news.p.text
    news_link = first_news.find("h3").a["href"]
    date = first_news.find("h4").text
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    image_link = ""
    video_link = ""
    try:
        image_link = first_news.find_all("img")[1]["src"]
    except:
        video_link = first_news.iframe["data-src"]
    media_link = image_link if image_link else video_link

    return "FlyBGD", date, epoch, news_title, short_description, news_link, media_link


def get_niviuk():
    page = requests.get("https://www.niviuk.com/en/news")
    soup = bs(page.text, "html.parser")
    first_news = soup.find(id="noticia_main")
    news_title = first_news.find(class_="tit").text
    news_link = first_news.find(class_="link").a["href"]
    short_description = first_news.find_all("div")[-2].text
    date = first_news.find(class_="data_publicacio").text
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    media_link = first_news.find("img")["src"]

    return "Niviuk", date, epoch, news_title, short_description, news_link, media_link


def get_skywalk():
    page = requests.get("https://skywalk.info/news/")
    soup = bs(page.text, "html.parser")
    news_title = soup.find(class_="entry-title").text
    news_link = soup.find(class_="entry-title").a["href"]
    short_description = (
        soup.find(class_="post-content").text.replace("read more", "").replace("\n", "")
    )
    date = soup.find(class_="published").text
    date = date.split()
    date = "-".join([date[1], calendar[date[0].lower()], date[2]]).replace(",", "")
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    media_link = (
        bs(requests.get(news_link).text, "html.parser").find("article").img["src"]
    )

    return "Skywalk", date, epoch, news_title, short_description, news_link, media_link


def get_fai():
    page = requests.get("https://www.fai.org/news?f%5B0%5D=field_related_sports%3A36")
    soup = bs(page.text, "html.parser")
    first_news = soup.find(class_="news-row")
    news_title = first_news.find_all(class_="field__item")[3].text
    news_link = "https://www.fai.org" + first_news.find(class_="link")["href"]
    in_news = bs(requests.get(news_link).text, "html.parser")
    short_description = in_news.find("p").text
    date = first_news.find_all(class_="field__item")[2].text
    date = date.split()
    date = "-".join([date[0], calendar[date[1].lower()], date[2]])

    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    media_link = in_news.find("img")["src"]

    return "FAI", date, epoch, news_title, short_description, news_link, media_link


def get_xalps():
    page = requests.get("https://www.redbullxalps.com/news/")
    soup = bs(page.text, "html.parser")
    first_news = soup.find(class_="cardsRolloverLink d-flex align-items-stretch")
    news_title = first_news.find(class_="customCardTitle").text
    news_link = "https://www.redbullxalps.com" + first_news["href"]
    short_description = soup.find("h4").text
    date = first_news.find(class_="newsDate").text.strip()[:10].replace(".", "-")
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    media_link = "https://www.redbullxalps.com" + first_news.find("img")["src"]

    return "X-Alps", date, epoch, news_title, short_description, news_link, media_link


def save_to_db():
    scarper_list = [
        get_xcmag(),
        get_flybgd(),
        get_niviuk(),
        get_skywalk(),
        get_fai(),
        get_xalps(),
    ]

    for news in scarper_list:
        NewsPost(
            author=news[0],
            date=news[1],
            epoch=news[2],
            title=news[3],
            short_description=news[4],
            news_link=news[5],
            media_link=news[6],
        ).save()
