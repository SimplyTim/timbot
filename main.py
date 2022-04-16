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
spam = True
skipping = False

client = commands.Bot(command_prefix='.' , case_insensitive=True)
DISCORDKEY = os.environ.get('KEY', None)
#CUSTOMRESPONSE1 = os.environ.get('QUINN', None)
#CUSTOMRESPONSE2 = os.environ.get('QUINNBOT', None)

FFMPEG_OPTIONS = {
'options': '-vn'
}

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='FBI Confidential Files'))
  print("Ready")

@client.command(aliases=['tim'])
async def timbot_dialog(ctx, *, dialog_sentence):
  global spam
  print("Received: " + dialog_sentence)

  # .tim togglespam
  if ctx.message.author.id == 298625295789981697 and dialog_sentence == "togglespam":
    if spam == True:
      spam = False
      await ctx.send("Spam mode off.")
    else:
      spam = True
      await ctx.send("Spam mode on.")
  # .tim <anything else>
  else:
    # pass string of dialog_sentence into your code
    dialog_response = timbot.timResponse(dialog_sentence, ctx.author)
    # response
    await ctx.send(dialog_response)
  
@client.command(aliases=['timplay'])
async def play(ctx, *, dialog_sentence):
  # .timplay <song>
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
      voice.play(discord.FFmpegPCMAudio(song_info[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(ctx), client.loop))

@client.command(aliases=['timskip'])
async def skip(ctx):
  # .timskip
  global skipping
  print('in skip')
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    if vc.is_playing():
      vc.stop()
    if not q.isEmpty() and not skipping:
      await ctx.send("Skipping...")
      skipping = True
      # next_song = q.dequeue() #(phrase, name)
      # await ctx.send("Playing " + next_song[1])
      # song_info = await musicbot.getQueryInfo(next_song[0])
      # vc.play(discord.FFmpegPCMAudio(song_info[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(ctx), client.loop))
      skipping = False
    else:
      await ctx.send("Laters dey.")
      await vc.disconnect()
  else:
    await ctx.send("I am not connected to a voice channel.")
  
async def afterPlay(ctx):
  print('in afterplay')
  global skipping
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    if vc.is_playing():
      vc.stop()
    if not q.isEmpty() and not skipping:
      skipping = True
      await ctx.send("Playing next song...")
      next_song = q.dequeue() #(phrase, name)
      await ctx.send("Playing " + next_song[1])
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
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    await vc.disconnect()
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timpause'])
async def pause(ctx):
  # .timpause
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    vc.pause()
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timresume'])
async def resume(ctx):
  # .timresume 
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if vc is not None:
    vc.resume()
  else:
    await ctx.send("I am not connected to a voice channel.")

@client.command(aliases=['timqueue'])
async def queue(ctx):
  # .timcheck
  if q.isEmpty():
    await ctx.send("The queue is empty.")
  else:
    await ctx.send(q.check())

  
'''
@client.event
async def on_message(message):
  senderId = message.author.id
  if senderId == 789166081910112266 and spam == True:
    await message.channel.send(CUSTOMRESPONSE2)
  elif senderId == 256984382546509824 and spam == True:
    await message.channel.send(CUSTOMRESPONSE1)
  await client.process_commands(message) # Needed to make other commands work since we overrided the default on_message
'''

if __name__ == "__main__":
  client.run(DISCORDKEY)
