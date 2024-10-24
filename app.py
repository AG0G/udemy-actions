import traceback
import asyncio
from coupons import Scrapper
from pytz import timezone
from datetime import datetime
import logging
from jinja2 import Environment, FileSystemLoader

# logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger(__name__)

# scraper
page = 2
scp = Scrapper()

# jinja environment
environment = Environment(loader=FileSystemLoader("templates/"))


async def updater():
    global page, coup, current_time, count, html_code
    try:
        current_time = datetime.now(
            timezone('Asia/Kolkata')).strftime('%H:%M:%S GMT%z %d-%m-%Y')
        logger.info(
            "------------------------Started collecting Coupons---------------------------------")
        links = await scp.discudemy(page)
        links += await scp.udemy_freebies(page)
        links += await scp.tutorialbar(page)
        links += await scp.coursevania(page)
        links += await scp.idcoupons(page)

        # unpack
        index = {}
        for link in links:
            for lin in link:
                if lin not in index:
                    index[lin] = 1

        links = list(index.keys())
        links.sort()
        count = len(links)
        logger.info(
            f"---------------------successfully-collected---{count} coupons----------------")

        # render HTML
        template = environment.get_template("index.html")
        html_code = template.render(
            count=count,
            current_time=current_time,
            links=links
        )
        with open("index.html", "w+") as file:
            file.write(html_code)
    except TimeoutError:
        logger.info("Couldn't Collect Coupons..!")
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(updater())
