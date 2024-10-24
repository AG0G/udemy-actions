import json
import re
from urllib.parse import unquote
import requests
import aiohttp
from bs4 import BeautifulSoup as bs
from yarl import URL

class Scrapper:
    """Udemy Free Courses Scrapper"""

    def __init__(self) -> None:
        self.head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://udemy.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}
        self.session = aiohttp.ClientSession

            return await response.text()
    def __fetch_html(self, url: str, headers: dict = None) -> bytes:
        if headers is None:
            headers = self.head
        return requests.get(url, headers=headers).content


    async def __fetch_json(self, session: aiohttp.ClientSession, url) -> any:
        async with session.get(url) as response:
            return await response.json()

    async def __fetch_url(self, session: aiohttp.ClientSession, url) -> URL:
        async with session.get(url) as response:
            return response.url

    async def discudemy(self, page) -> list:
        du_links = []
        async with self.session(headers=self.head) as ass:
            soup = bs(
                await self.__fetch_html(
                    ass, "https://www.discudemy.com/all/" + str(page)
                ),
                "html5lib",
            )
            all = soup.find_all("section", "card")
            for index, items in enumerate(all):
                try:
                    title = items.a.text
                    url = items.a["href"]
                    soup = bs(await self.__fetch_html(ass, url), "html5lib")
                    next = soup.find("div", "ui center aligned basic segment")
                    url = next.a["href"]
                    soup = bs(await self.__fetch_html(ass, url), "html5lib")
                    du_links.append(
                        title + "|:|" + soup.find("div", "ui segment").a["href"]
                    )
                except:
                    continue
            return self._parse(du_links)

    async def udemy_freebies(self, page) -> list:
        uf_links = []
        async with self.session(headers=self.head) as ass:
            soup = bs(
                await self.__fetch_html(
                    ass, "https://www.udemyfreebies.com/free-udemy-courses/" + str(page)
                ),
                
                "html5lib",
            )
            all = soup.find_all("div", "coupon-name")
            for index, items in enumerate(all):
                try:
                    title = items.a.text
                    url = items.a["href"]
                    soup = bs(await self.__fetch_html(ass, url), "html5lib")
                    next = soup.find("a", class_="button-icon")
                    url = next["href"]
                    uf_links.append(
                        title + "|:|" + str(await self.__fetch_url(ass, url))
                    )
                except:
                    continue
        return self._parse(uf_links)

    async def tutorialbar(self, page) -> list:
        tb_links = []
        async with self.session(headers=self.head) as ass:
            soup = bs(
                await self.__fetch_html(
                    ass, "https://www.tutorialbar.com/all-courses/page/{str(page)}"
                ),
                "html5lib",
            )
            all = soup.find_all(
                    "h3", class_="mb15 mt0 font110 mobfont100 fontnormal lineheight20"
                )
            for index, items in enumerate(all):
                try:
                    title = items.a.text
                    url = items.a["href"]
                    soup = bs(await self.__fetch_html(ass, url), "html5lib")
                    link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
                    if "www.udemy.com" in link:
                        tb_links.append(title + "|:|" + link)
                except:
                    continue
        return self._parse(tb_links)

    async def real_discount(self, page) -> list:
        rd_links = []
        async with self.session(headers=self.head) as ass:
            soup = bs(
                await self.__fetch_html(
                    ass, "https://app.real.discount/stores/Udemy?page=" + str(page)
                ),
                "html5lib",
            )
            all = soup.find_all("div", class_="col-xl-4 col-md-6")
            for index, items in enumerate(all):
                title = items.h3.text
                url = "https://app.real.discount" + items.a["href"]
                soup = bs(await self.__fetch_html(ass, url), "html5lib")
                try:
                    link = soup.select_one("a[href^='https://www.udemy.com']")["href"]
                    rd_links.append(title + "|:|" + link)
                except:
                    pass
        return self._parse(rd_links)

    async def coursevania(self, page) -> list:
        cv_links = []
        async with self.session(headers=self.head) as ass:
            soup= bs(await self.__fetch_html(ass, "https://coursevania.com/courses/"),
            "html5lib",
            )
            print(soup.text)
            nonce = (
                json.loads(re.search(r"var stm_lms_nonces = ({.*?});", soup.text, re.DOTALL).group(1))["load_content"]
            )
            url = (
                "https://coursevania.com/wp-admin/admin-ajax.php?&template=courses/grid&args={%22posts_per_page%22:%2230%22}&action=stm_lms_load_content&nonce="
                + nonce
                + "&sort=date_high"
            )
            r = await self.__fetch_json(ass, url)
            soup = bs(r["content"], "html5lib")
            all = soup.find_all(
                "div", attrs={"class": "stm_lms_courses__single--title"}
            )
            for _, items in enumerate(all):
                title = items.h5.text
                url = items.a["href"]
                soup = bs(await self.__fetch_html(ass, url), "html5lib")
                cv_links.append(
                    title
                    + "|:|"
                    + soup.find("div", attrs={"class": "masterstudy-button-affiliate__link"}).a["href"]
                )
        return self._parse(cv_links)

    async def idcoupons(self, page) -> list:
        idc_links = []
        async with self.session(headers=self.head) as ass:
            soup = bs(
                await self.__fetch_html(
                    ass,
                    "https://idownloadcoupon.com/product-category/udemy-2/page/"
                    + str(page),
                ),
                "html5lib",
            )
            all = soup.find_all("a", attrs={"class": "button product_type_external"})
            for index, items in enumerate(all):
                title = items["aria-label"]
                link = unquote(items["href"]).split("ulp=")
                try:
                    link = link[1]
                except:
                    link = link[0]
                if link.startswith("https://www.udemy.com"):
                    idc_links.append(title + "|:|" + link)
        return self._parse(idc_links)

    
    @staticmethod
    def _parse(links) -> list:
        if not links:
            return links
        _links = []
        r_links = []
        f_links = []
        n = 1
        for _link in links:
            link = _link.split("|:|")[1]
            title = _link.split("|:|")[0]
            lin = f"<li><a href='{link}' target =_blank>{title}</a></li>"
            _links.append(lin)
            if len(_links) == 20:
                f_links.append(_links)
                _links = []
                r_links = []
            else:
                r_links.append(lin)
            n += 1
            
        if r_links:
            f_links.append(r_links)

        return f_links
