import requests
import logging
from datetime import datetime
from news.models import NewsPost
from bs4 import BeautifulSoup as bs
from requests_html import AsyncHTMLSession
import aiohttp
import time
import asyncio


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
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


async def get_xcmag(news_number: int):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://xcmag.com/news/") as page:
                page = await page.text()
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
                ).split()
                date = "-".join([date[1], calendar[date[2][:3].lower()], date[3]])
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = first_news.a.img["src"]
                author_link = "https://xcmag.com"

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

    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from XCmag")
        logger.error(e)


async def get_flybgd():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.flybgd.com/en/paragliders/news-wings-gliders-6-0-0.html"
            ) as page:
                page = await page.text()
                soup = bs(page, "html.parser")
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
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from FlyBGD")
        logger.error(e)


async def get_niviuk():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.niviuk.com/en/news") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                first_news = soup.find(id="noticia_main")
                news_title = first_news.find(class_="tit").text
                news_link = first_news.find(class_="link").a["href"]
                short_description = first_news.find_all("div")[-2].text
                date = first_news.find(class_="data_publicacio").text
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = first_news.find("img")["src"]
                author_link = "https://www.niviuk.com"

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
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Niviuk")
        logger.error(e)


async def get_skywalk():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://skywalk.info/news/") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                news_title = soup.find(class_="entry-title").text
                news_link = soup.find(class_="entry-title").a["href"]
                short_description = (
                    soup.find(class_="post-content")
                    .text.replace("read more", "")
                    .replace("\n", "")
                )
                date = soup.find(class_="published").text.split()
                date = "-".join([date[1], calendar[date[0].lower()], date[2]]).replace(
                    ",", ""
                )
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = (
                    bs(requests.get(news_link).text, "html.parser")
                    .find("article")
                    .img["src"]
                )
                author_link = "https://skywalk.info"

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
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Skywalk")
        logger.error(e)


async def get_fai():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.fai.org/news?f%5B0%5D=field_related_sports%3A36"
            ) as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                first_news = soup.find(class_="news-row")
                news_title = first_news.find_all(class_="field__item")[3].text
                news_link = (
                    "https://www.fai.org" + first_news.find(class_="link")["href"]
                )
                in_news = bs(requests.get(news_link).text, "html.parser")
                short_description = in_news.find("p").text
                date = first_news.find_all(class_="field__item")[2].text.split()
                date = "-".join([date[0], calendar[date[1].lower()], date[2]])
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = in_news.find("img")["src"]
                author_link = "https://www.fai.org"

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
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from FAI")
        logger.error(e)


async def get_xalps():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.redbullxalps.com/news/") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                first_news = soup.find(
                    class_="cardsRolloverLink d-flex align-items-stretch"
                )
                news_title = first_news.find(class_="customCardTitle").text
                news_link = "https://www.redbullxalps.com" + first_news["href"]
                short_description = soup.find("h4").text
                date = (
                    first_news.find(class_="newsDate")
                    .text.strip()[:10]
                    .replace(".", "-")
                )
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = (
                    "https://www.redbullxalps.com" + first_news.find("img")["src"]
                )
                author_link = "https://www.redbullxalps.com"

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
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from X-Alps")
        logger.error(e)


async def get_phi():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://phi-air.com/") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                first_news = soup.find(class_="post-entry-content")
                news_title = first_news.a.text
                news_link = first_news.a["href"]
                short_description = first_news.p.text
                date = first_news.find(class_="entry-date updated").text.replace(
                    "/", "-"
                )
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = soup.find(class_="post-thumbnail").a.img["data-src"]
                author_link = "https://phi-air.com/"

        return (
            "PHI",
            date,
            epoch,
            news_title,
            short_description,
            news_link,
            image_link,
            video_link,
            author_link,
        )
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from PHI")
        logger.error(e)


async def get_ozone():
    try:
        session = AsyncHTMLSession(browser_args=["--no-sandbox"])
        response = await session.get("https://www.flyozone.com/paragliders/news")
        await response.html.arender(sleep=4, timeout=15)
        soup = bs(response.html.html, "html.parser")
        first_news = soup.find(class_="article")
        news_title = " ".join(first_news.h3.text.replace("\n", "").strip().split())
        news_link = first_news.a["href"]
        short_description = first_news.find(class_="article__excerpt").text.replace(
            "\xa0", ""
        )
        date = first_news.find(class_="article__date").text.replace(",", "").split()
        date = f"{date[1]}-{calendar[date[0].lower()]}-{date[2]}"
        epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
        video_link = ""
        image_link = first_news.find(class_="article__thumbnail")["src"]
        author_link = "https://www.flyozone.com/"
        await session.close()
        return (
            "Ozone",
            date,
            epoch,
            news_title,
            short_description,
            news_link,
            image_link,
            video_link,
            author_link,
        )
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Ozone")
        logger.error(e)


async def get_nova():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.nova.eu/en/news-stories/") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                news = soup.find(class_="news-list-view")
                news_title = news.find(class_="header").h3.text
                news_link = f"https://www.nova.eu/{news.a['href']}"
                short_description = news.p.text
                date = datetime.today().strftime("%d-%m-%Y")
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                image_link = f"https://www.nova.eu/{news.a.img['src']}"
                author_link = "https://www.nova.eu/"

        return (
            "Nova",
            date,
            epoch,
            news_title,
            short_description,
            news_link,
            image_link,
            video_link,
            author_link,
        )
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from Nova")
        logger.error(e)


async def get_world_cup():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pwca.org/") as page:
                page = await page.text()
                soup = bs(page, "html.parser")
                first_news = soup.find(class_="article important news")
                news_title = first_news.img["alt"]
                news_link = first_news.a["href"]
                page = requests.get(news_link)
                soup = bs(page.text, "html.parser")
                short_description = (
                    soup.find(class_="card-body").find_all("div")[2].text
                )
                short_description = (
                    short_description[:200]
                    if len(short_description) > 200
                    else short_description
                )
                date = datetime.today().strftime("%d-%m-%Y")
                epoch = int(datetime.strptime(date, "%d-%m-%Y").timestamp())
                video_link = ""
                if first_news.img["src"]:
                    image_link = first_news.img["src"]
                else:
                    image_link = "https://picsum.photos/seed/picsum/500"
                author_link = "https://pwca.org/"

        return (
            "PWC",
            date,
            epoch,
            news_title,
            short_description,
            news_link,
            image_link,
            video_link,
            author_link,
        )
    except Exception as e:
        print("Error occured: " + str(e) + " during fetching data from PWC")
        logger.error(e)


async def get_youtube(channel_name: str, name: str):
    try:
        url = f"https://www.youtube.com/c/{channel_name}/videos"
        session = AsyncHTMLSession(browser_args=["--no-sandbox"])
        response = await session.get(url)
        await response.html.arender(sleep=3, timeout=15)
        html = str(response.html.html)
        soup = bs(html, "html.parser")
        news_title = soup.find(id="video-title")["title"]
        raw_link = soup.find(id="video-title")["href"]
        news_link = f"https://www.youtube.com{raw_link}"
        video_link = f"https://www.youtube.com/embed{raw_link.replace('watch?v=', '')}"
        image_link = ""
        video_response = await session.get(news_link)
        soup = bs(video_response.html.html, "html.parser")
        short_description = soup.find("meta", itemprop="description")["content"]
        date = soup.find_all("meta")[-2]["content"].split("-")
        if channel_name == "FlyWithGreg":
            date = f"{date[2][:2]}-{date[1]}-{date[0]}"
        else:
            date = f"{date[2]}-{date[1]}-{date[0]}"
        epoch = int(datetime.timestamp(datetime.strptime(date, "%d-%m-%Y")))
        author_link = f"https://www.youtube.com/c/{channel_name}"
        await session.close()
        return (
            name,
            date,
            epoch,
            news_title,
            short_description,
            news_link,
            image_link,
            video_link,
            author_link,
        )
    except Exception as e:
        print("Error occured: " + str(e) + f" during fetching data from {name} YT")
        logger.error(e)


async def get_results():
    res = await asyncio.gather(
        get_xcmag(0),
        get_xcmag(1),
        get_flybgd(),
        get_niviuk(),
        get_skywalk(),
        get_fai(),
        get_xalps(),
        get_phi(),
        get_nova(),
        get_world_cup(),
        get_ozone(),
        get_youtube("FlybubbleParagliding1", "Flybubble"),
        get_youtube("FlyWithGreg", "FlyWithGreg"),
        get_youtube("xcmag", "XCmag-YouTube"),
    )
    return res


def save_to_db():
    result = asyncio.run(get_results())
    for news in result:
        try:
            if not NewsPost.objects.filter(title=news[3]).exists():
                print(f"Saving {news[3]} to db")
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
        except Exception as e:
            print(
                "Error occured: "
                + str(e)
                + f" during saving data from function {news} to db"
            )
            logger.error(e)
