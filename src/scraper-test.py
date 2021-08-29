import cloudscraper
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional

base_url = "https://www3.animeflv.net"

scraper = cloudscraper.create_scraper()

res = scraper.get(f"{base_url}/perfil/__stark__/siguiendo")

soup = BeautifulSoup(res.text, 'html.parser')

class Anime(BaseModel):
    base_url: str = "https://www3.animeflv.net"
    title: str
    link: str
    description: str
    cover_link: str

    def full_url(self):
        return base_url + self.link 
    
    def full_cover_url(self):
        return base_url + self.cover_link 

animes = []
for anime in soup.select("article.Anime"):
    link = anime.select("h3.Title a")[0]
    image = anime.select("figure img")[0]
    animes.append(Anime(
        title=link.text,
        link=link.get("href"),
        cover_link=image.get("src"),
        description=anime.select("article p")[0].text
    ))

print(animes)
