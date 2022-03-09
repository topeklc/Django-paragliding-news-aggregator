import logging
from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
from requests_html import HTMLSession
from news.models import NewsPost


"""Setup logger"""
logging.basicConfig(
    filename="updater_logs.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


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


def get_xcmag(news_number: int):
    try:
        page = requests.get("https://xcmag.com/news/").text
        soup = bs(page, "html.parser")
        soup.find_all("li")
        first_news = soup.find_all(class_="grid")[0].find_all("li")[news_number]
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
        video_link = ""
        image_link = first_news.a.img["src"]
        author_link = "https://xcmag.com"
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from XCmag")
        logger.error(e)
    return (
        "XCmag",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_flybgd():
    try:
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
        author_link = "https://www.flybgd.com"
        try:
            image_link = first_news.find_all("img")[1]["src"]
        except:
            video_link = first_news.iframe["data-src"]
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from FlyBGD")
        logger.error(e)
    return (
        "FlyBGD",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_niviuk():
    try:
        page = requests.get("https://www.niviuk.com/en/news")
        soup = bs(page.text, "html.parser")
        first_news = soup.find(id="noticia_main")
        news_title = first_news.find(class_="tit").text
        news_link = first_news.find(class_="link").a["href"]
        short_description = first_news.find_all("div")[-2].text
        date = first_news.find(class_="data_publicacio").text
        epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
        video_link = ""
        image_link = first_news.find("img")["src"]
        author_link = "https://www.niviuk.com"
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Niviuk")
        logger.error(e)
    return (
        "Niviuk",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_skywalk():
    try:
        page = requests.get("https://skywalk.info/news/")
        soup = bs(page.text, "html.parser")
        news_title = soup.find(class_="entry-title").text
        news_link = soup.find(class_="entry-title").a["href"]
        short_description = (
            soup.find(class_="post-content")
            .text.replace("read more", "")
            .replace("\n", "")
        )
        date = soup.find(class_="published").text
        date = date.split()
        date = "-".join([date[1], calendar[date[0].lower()], date[2]]).replace(",", "")
        epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
        video_link = ""
        image_link = (
            bs(requests.get(news_link).text, "html.parser").find("article").img["src"]
        )
        author_link = "https://skywalk.info"
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Skywalk")
        logger.error(e)
    return (
        "Skywalk",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_fai():
    try:
        page = requests.get(
            "https://www.fai.org/news?f%5B0%5D=field_related_sports%3A36"
        )
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
        video_link = ""
        image_link = in_news.find("img")["src"]
        author_link = "https://www.fai.org"
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from FAI")
        logger.error(e)
    return (
        "FAI",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_xalps():
    try:
        page = requests.get("https://www.redbullxalps.com/news/")
        soup = bs(page.text, "html.parser")
        first_news = soup.find(class_="cardsRolloverLink d-flex align-items-stretch")
        news_title = first_news.find(class_="customCardTitle").text
        news_link = "https://www.redbullxalps.com" + first_news["href"]
        short_description = soup.find("h4").text
        date = first_news.find(class_="newsDate").text.strip()[:10].replace(".", "-")
        epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
        video_link = ""
        image_link = "https://www.redbullxalps.com" + first_news.find("img")["src"]
        author_link = "https://www.redbullxalps.com"
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from X-Alps")
        logger.error(e)
    return (
        "X-Alps",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def get_flybubble():
    url = "https://www.youtube.com/c/FlybubbleParagliding1/videos"
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    soup = bs(response.html.html, "html.parser")
    news_title = soup.find(id="video-title")["title"]
    raw_link = soup.find(id="video-title")["href"]
    news_link = f"https://www.youtube.com{raw_link}"
    video_link = f"https://www.youtube.com/embed{raw_link.replace('watch?v=', '')}"
    image_link = ""
    video_response = session.get(news_link)
    soup = bs(video_response.html.html, "html.parser")
    short_description = soup.find("meta", itemprop="description")["content"]
    date = soup.find_all("meta")[-2]["content"]
    date = date.split("-")
    date = f"{date[2]}-{date[1]}-{date[0]}"
    epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
    author_link = "https://www.youtube.com/user/FlybubbleParagliding"
    # except Exception as e:
    #     print("Error occured: " + str(e) + " during fetching data from Flybubble")
    #     logger.error(e)
    return (
        "Flybubble",
        date,
        epoch,
        news_title,
        short_description,
        news_link,
        image_link,
        video_link,
        author_link,
    )


def save_to_db():
    scarper_list = [
        get_xcmag(0),
        get_xcmag(1),
        get_flybgd(),
        get_niviuk(),
        get_skywalk(),
        get_fai(),
        get_xalps(),
        get_flybubble(),
    ]

    for news in scarper_list:
        if not NewsPost.objects.filter(title=news[3]).exists():
            NewsPost(
                author=news[0],
                date=news[1],
                epoch=news[2],
                title=news[3],
                short_description=news[4],
                news_link=news[5],
                image_link=news[6],
                video_link=news[7],
                author_link=news[8],
            ).save()
