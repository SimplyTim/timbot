from __future__ import unicode_literals
from youtubesearchpython.__future__ import *
import youtube_dl, asyncio, json, discord, os
from discord.ext import commands
from discord.utils import get

ydl_opts = {
  'format': 'bestaudio/worst',
  'continue_dl': True,
  'noplaylist': True,
  'quiet':True,
  'source_address':'0.0.0.0',
}

async def getQueryInfo(query):
  videosSearch = VideosSearch(query, limit = 1)
  videosResult = await videosSearch.next()
  link = videosResult['result'][0]['link']
  name = videosResult['result'][0]['title']
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(link, download=False)
    video_url = info_dict.get("url", None)
    video_id = info_dict.get("id", None)
    video_title = info_dict.get('title', None)
    print(video_title)
    return (video_url, video_title)

async def downloadAudio(result):
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([result])

async def cleanup():
  try:
    if os.path.isfile("current.webm"):
      os.remove('current.webm')
  except:
    pass
