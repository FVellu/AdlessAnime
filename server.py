from flask import Flask, render_template
from flask import request
import bs4, requests, webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search')
def search():
    search_website = requests.get("https://www.animeworld.tv/search?keyword=" + request.args.get("search"))
    soup = bs4.BeautifulSoup(search_website.text, "html.parser")

    anime_list = soup.find_all("a", class_="name")

    anime_names = []
    anime_links = []
    for anime in anime_list:
        anime_names.append(anime.get("data-jtitle"))
        anime_links.append(anime.get("href").replace("play/", "episodes?anime="))

    return render_template("search.html", anime_names=anime_names, anime_links=anime_links, zip=zip)

@app.route('/episodes')
def episodes():
    search_website = requests.get("https://www.animeworld.tv/play/" + request.args.get("anime"))
    soup = bs4.BeautifulSoup(search_website.text, "html.parser")

    episode_names = []
    episode_codes = []

    for link in soup.find_all("a"):
        if link.get("data-episode-id"):
            episode_names.append(link.decode_contents())
            episode_codes.append(link.get("href").replace("play/", "play?code="))

    return render_template("episodes.html", episode_names=episode_names, episode_codes=episode_codes, len=len)

@app.route("/play")
def play():
    search_website = requests.get("https://www.animeworld.tv/play/" + request.args.get("code"))
    soup = bs4.BeautifulSoup(search_website.text, "html.parser")

    video_link = soup.find("a", id="downloadLink").get("href")

    print(video_link)
    return render_template("play.html", video_link=video_link.replace("download-file.php?id=", ""))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)