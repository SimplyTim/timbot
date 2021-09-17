from __future__ import unicode_literals
from youtubesearchpython.__future__ import *
import youtube_dl
import asyncio
import json
import Queue

async def main(query):
    videosSearch = VideosSearch(query, limit = 1)
    videosResult = await videosSearch.next()
    result = videosResult['result'][0]['link']
    print(result)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'current.mp3',
        'ignoreerrors': True,
        'nooverwrites': False,
        'fixup': 'detect_or_warn',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([result])