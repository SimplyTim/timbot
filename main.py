from operator import is_
import discord
import timbot
from musicbot import *
from discord.ext import commands
from discord.utils import get
import os, asyncio, time, musicbot
#from key import KEY

# #opus for Heroku
if not discord.opus.is_loaded():
  discord.opus.load_opus('libopus.so')


class Queue():
  def __init__(self):
    self.q = []
  
  def enqueue(self, item):
    self.q.append(item)
  
  def dequeue(self):
    url = self.q.pop(0)
    return url
  
  def check(self):
    returnstr = ""
    for i, song in enumerate(self.q):
      returnstr += str(i+1) + ") " + song[1] + "\n"
    return returnstr

  def isEmpty(self):
    return len(self.q)==0

q = Queue()
skipping = False
currently_playing = ""

client = commands.Bot(command_prefix='.' , case_insensitive=True)
DISCORDKEY = os.environ.get('KEY', None)

FFMPEG_OPTIONS = {
'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-v 40',
}

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='FBI Confidential Files'))
  print("Ready")
  
@client.command(aliases=['timplay'])
async def play(ctx, *, dialog_sentence):
  # .timplay <song>
  global currently_playing
  print('in play')
  if dialog_sentence == "":
    ctx.send("Please enter a phrase/URL to play a song.")
    return
  else:
    phrase = dialog_sentence.lower()
    voice_client = ctx.message.author.voice
    if voice_client is None:
      await ctx.send("You must be in a voice channel to play music.")
      return
    current_channel_id = voice_client.channel.id
    voice_channel = discord.utils.get(ctx.guild.voice_channels, id=current_channel_id)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    song_info = await musicbot.getQueryInfo(phrase)  # song_info = (url, title)

    if voice is None:
      voice = await voice_channel.connect()
    
    if voice.is_playing():
      q.enqueue((phrase, song_info[1]))
      await ctx.send("Added " + song_info[1] + " to queue.")
    else:
      await ctx.send("Playing " + song_info[1])
      currently_playing = song_info[1]
      voice.play(discord.FFmpegPCMAudio(song_info[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(ctx), client.loop))

@client.command(aliases=['timskip'])
async def skip(ctx):
  # .timskip
  global skipping
  print('in skip')
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    vc.stop()
    if not q.isEmpty() and not skipping:
      await ctx.send("Skipping song...")
  else:
    await ctx.send("I am not connected to a voice channel.")
  
async def afterPlay(ctx):
  print('in afterplay')
  global skipping
  global currently_playing
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    if vc.is_playing():
      vc.stop()
    if not q.isEmpty() and not skipping:
      skipping = True
      await ctx.send("Playing next song...")
      next_song = q.dequeue() #(phrase, name)
      await ctx.send("Playing " + next_song[1])
      currently_playing = song_info[1]
      song_info = await musicbot.getQueryInfo(next_song[0])
      vc.play(discord.FFmpegPCMAudio(song_info[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(ctx), client.loop))
      skipping = False
    else:
      await ctx.send("Laters dey.")
      await vc.disconnect()
  else:
    await vc.disconnect()

@client.command(aliases=['timkill'])
async def kill(ctx):
  # .timkill
  q.q = [] #empties the queue
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    await ctx.send("Laters dey.")
    await vc.disconnect()
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timpause'])
async def pause(ctx):
  # .timpause
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    vc.pause()
    await ctx.send("**" + currently_playing + " paused.**")
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timresume'])
async def resume(ctx):
  # .timresume 
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    vc.resume()
    await ctx.send("**Resuming" + currently_playing + ".**")
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timqueue'])
async def queue(ctx):
  # .timcheck
  global currently_playing
  
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc.is_playing():
    await ctx.send("**Currently playing: " + currently_playing + ".**" )
  
  if q.isEmpty():
    await ctx.send("The queue is empty.")
  else:
    await ctx.send(q.check())

if __name__ == "__main__":
  client.run(DISCORDKEY)
