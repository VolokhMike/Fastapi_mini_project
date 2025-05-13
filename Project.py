from fastapi import FastAPI, Query
from bs4 import BeautifulSoup
import httpx
import uvicorn

app = FastAPI()

URL = "http://127.0.0.1:8000/action-anime?link=https://myanimelist.net/anime/genre/1/Action"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


@app.get("/action-anime")
async def get_action_anime(
        link: str = Query(...)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(link, headers=HEADERS)

    soup = BeautifulSoup(response.text, "html.parser")
    names = soup.find_all("span", class_="js-title")
    scores = soup.find_all("span", class_="js-score")
    synopsises = soup.find_all("div", class_="synopsis js-synopsis")

    parsed_list = []

    for name, score, synopsis in zip(names, scores, synopsises):
        p = synopsis.find("p", class_="preline")
        synopsis_text = p.text.strip() if p else ""
        parsed_list.append({
            "title": name.text.strip(),
            "score": score.text.strip(),
            "synopsis": synopsis_text
        })

    return parsed_list

if __name__ == '__main__':
    uvicorn.run("Project:app", reload=True)
