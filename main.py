import discord
import timbot
from musicbot import *
from discord.ext import commands
from discord.utils import get
import os, asyncio, time, musicbot
#from key import KEY

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

client = commands.Bot(command_prefix='.' , case_insensitive=True)
DISCORDKEY = os.environ.get('KEY', None)
#CUSTOMRESPONSE1 = os.environ.get('QUINN', None)
#CUSTOMRESPONSE2 = os.environ.get('QUINNBOT', None)

FFMPEG_OPTIONS = {
'options': '-vn'
}

async def afterPlay(client, ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()
  if not q.isEmpty():
    next_song = q.dequeue()
    await ctx.send("Playing " + next_song[1])
    voice.play(discord.FFmpegPCMAudio(next_song[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(client, ctx), client.loop))
  else:
    await voice.disconnect()


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


  # .tim play <song>
  elif dialog_sentence.split()[0].lower() == 'play':
    phrase = ' '.join(dialog_sentence.split()[1:])
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
      q.enqueue(song_info)
      await ctx.send("Added " + song_info[1] + " to queue.")
    else:
      await ctx.send("Playing " + song_info[1])
      voice.play(discord.FFmpegPCMAudio(song_info[0], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(afterPlay(client, ctx), client.loop))

  # .tim kill
  elif dialog_sentence == 'kill':
    vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if vc is not None:
      await vc.disconnect()
    else:
      await ctx.send("I am not connected to a voice channel.")
  

  # .tim pause
  elif dialog_sentence == 'pause':
    vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if vc is not None:
      vc.pause()
    else:
      await ctx.send("I am not connected to a voice channel.")

  # .tim resume 
  elif dialog_sentence == 'resume':
    vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if vc is not None:
      vc.resume()
    else:
      await ctx.send("I am not connected to a voice channel.")
  

  # .tim skip
  elif dialog_sentence == 'skip':
    vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if vc is not None:
      vc.stop()
      await ctx.send("Skipping current song.")
      asyncio.run_coroutine_threadsafe(afterPlay(client, ctx), client.loop)
    elif not vc.is_playing():
      await ctx.send("Nothing is playing.")
    else:
      await ctx.send("I am not connected to a voice channel.")
  
  # .tim check
  elif dialog_sentence == 'queue':
    if q.isEmpty():
      await ctx.send("The queue is empty.")
    else:
      await ctx.send(q.check())


  # .tim <anything else>
  else:
    # pass string of dialog_sentence into your code
    dialog_response = timbot.timResponse(dialog_sentence, ctx.author)
    # response
    await ctx.send(dialog_response)

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
