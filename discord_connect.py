import discord
import timbot
import musicbot
from discord.ext import commands
from discord.utils import get
import os, asyncio, time
from key import KEY
import musicbot, Queue

client = commands.Bot(command_prefix='.' , case_insensitive=True)
#DISCORDKEY = os.environ.get('KEY', None)
#CUSTOMRESPONSE1 = os.environ.get('QUINN', None)
#CUSTOMRESPONSE2 = os.environ.get('QUINNBOT', None)
try:
  os.remove('current.mp3')
except:
  pass
spam = True
channel_id = 0
vc = ""


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='FBI Confidential Files'))
  print("Ready")

@client.command(aliases=['tim'])
async def timbot_dialog(ctx, *, dialog_sentence):
  global channel_id
  global spam
  global vc
  print(dialog_sentence)
  if ctx.message.author.id == 298625295789981697 and dialog_sentence == "togglespam":
    if spam == True:
      spam = False
      await ctx.send("Spam mode off.")
    else:
      spam = True
      await ctx.send("Spam mode on.")
  elif ctx.message.author.id == 298625295789981697 and dialog_sentence.split()[0] == "setmusicchannel":
    channel_id  = int(' '.join(dialog_sentence.split()[1:]))
    await ctx.send("Channel set.")
  elif dialog_sentence.split()[0].lower() == 'play':
    if channel_id == 0:
      await ctx.send("Please set a channel for me to go to.")
    elif vc != "":
      if vc.is_playing():
        await ctx.send("I'm busy. Do .tim skip if you want me to do something else.")
    else:
      try:
        if os.path.exists('current.mp3'):
          os.remove('current.mp3')
      except:
        pass

      phrase = ' '.join(dialog_sentence.split()[1:])
      await ctx.send("Playing " + phrase + ".")
      await musicbot.main(phrase)
      vc = await client.get_channel(channel_id).connect()
      vc.play(discord.FFmpegPCMAudio(executable="C:/ProgramData/chocolatey/bin/ffmpeg.exe", source="current.mp3"))
  elif dialog_sentence == 'skip':
      try:
        if vc.is_connected():
          await vc.disconnect()
          vc = ""
      except:
        pass

      try:
        if os.path.exists('current.mp3'):
          os.remove('current.mp3')
      except:
        pass
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
  client.run(KEY)