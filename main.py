from pyrogram import Client, filters
from pyrogram.types import *
import json
import os
import requests
import subprocess
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler


API_ID = os.environ.get("API_ID", None) 
MONGO_URL = os.environ.get("MONGO_URL", None) 
API_HASH = os.environ.get("API_HASH", None) 
BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 
CHANNEL_ID = os.environ.get(int("CHANNEL_ID"))
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME", None) 

app = Client(
    "hentai",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


async def autohentai_parser():
    hentaidb = MongoClient(MONGO_URL)
    hentai = hentaidb["HentaiDb"]["Name"]
    url = f"https://hanime.metavoid.info/recent"
    result = requests.get(url)
    result = result.json()
    url = result["reposone"][0]["slug"]
    name = result["reposone"][0]["name"]
    img = result["reposone"][0]["poster_url"]
    is_hentai = hentai.find_one({"url": url})
    if not is_hentai:
        l = f"https://hanime.metavoid.info/link?id={url}"
        k = requests.get(l)
        data = k.json()
        k = data["data"][0]["url"]
        if not k == "":
            url1 = data["data"][0]["url"]
            url2 = data["data"][1]["url"]
            url3 = data["data"][2]["url"]
            file1 = f'{url}-720p.mp4'
            file2 = f'{url}-480p.mp4'
            file3 = f'{url}-360p.mp4'
            gay = requests.get(img)
            open('themb.jpg', 'wb').write(gay.content)
            image = 'themb.jpg'
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url1, file1),
                           shell=True)
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url2, file2),
                           shell=True)
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url3, file3),
                           shell=True)
            hentai.insert_one({"url": url})
            await app.send_video(CHANNEL_ID,
                                 file1,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 720p')
            await app.send_video(CHANNEL_ID,
                                 file2,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 480p')
            await app.send_video(CHANNEL_ID,
                                 file3,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 360p')
            os.remove(file1)
            os.remove(file2)
            os.remove(file3)
            os.remove(image)
        if k == "":
            url1 = data["data"][1]["url"]
            url2 = data["data"][2]["url"]
            url3 = data["data"][3]["url"]
            file1 = f'{url}-720p.mp4'
            file2 = f'{url}-480p.mp4'
            file3 = f'{url}-360p.mp4'
            gay = requests.get(img)
            open('themb.jpg', 'wb').write(gay.content)
            image = 'themb.jpg'
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url1, file1),
                           shell=True)
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url2, file2),
                           shell=True)
            subprocess.run("ffmpeg -i {} -acodec copy -vcodec copy {}".format(
                url3, file3),
                           shell=True)
            hentai.insert_one({"url": url})
            await app.send_video(CHANNEL_ID,
                                 file1,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 720p')
            await app.send_video(CHANNEL_ID,
                                 file2,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 480p')
            await app.send_video(CHANNEL_ID,
                                 file3,
                                 thumb=f'{image}',
                                 caption=f'[{CHANNEL_USERNAME}] {name} - 360p')
            os.remove(file1)
            os.remove(file2)
            os.remove(file3)
            os.remove(image)


scheduler = AsyncIOScheduler()
scheduler.add_job(autohentai_parser, "interval", minutes=1)
scheduler.start()


app.run()
