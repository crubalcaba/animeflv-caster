import cloudscraper
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List
import json

base_url = "https://www3.animeflv.net"

scraper = cloudscraper.create_scraper()

cookies = {'login': 'meNAc3YX6TQkgF3SHKvUEFFArJ8Kt5j3ZdIKnoR5cy5JijB8dpIvJPLFjEfVOmEs5Jh1pd9IABQ%3D'}

res = scraper.get(f"{base_url}/perfil/__stark__/siguiendo")

soup = BeautifulSoup(res.text, 'html.parser')

class Anime(BaseModel):
    base_url: str = "https://www3.animeflv.net"
    title: str
    link: str
    description: str
    cover_link: str
    last_seen: int = 0
    episode_count: int = 0

    @property
    def name(self):
        return self.link.split('/')[-1]

    @property
    def full_url(self):
        return base_url + self.link 
    
    @property
    def full_cover_url(self):
        return base_url + self.cover_link
    
    def episode_link(self, episode: int):
        return f"{self.base_url}/ver/{self.name}-{episode}"


animes = []
for anime in soup.select("article.Anime"):
    link = anime.select_one("h3.Title a")
    image = anime.select_one("figure img")
    image_link = image.get("src") or image.get("data-cfsrc")
    animes.append(Anime(
        title=link.text,
        link=link.get("href"),
        cover_link=image_link,
        description=anime.select_one("article p").text
    ))

idaten = animes[0]
res = scraper.get(idaten.full_url, cookies=cookies)

idaten_soup = BeautifulSoup(res.text, "html.parser")

for script in idaten_soup.find_all('script'):
    contents = str(script)
    if 'var episodes = [' in contents:
        data = json.loads(contents.split('var episodes = ')[1].split(';')[0])
        idaten.episode_count = len(data)
        idaten.last_seen = int(contents.split('var last_seen = ')[1].split(';')[0])
        break

res = scraper.get(idaten.episode_link(1))
episode = res.text.split('SUB":')[1].split("};")[0]
episode_servers = json.loads(episode)
