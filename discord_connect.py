import discord
import timbot
from discord.ext import commands
from discord.utils import get
import os
#from key import KEY

client = commands.Bot(command_prefix='.' , case_insensitive=True)
DISCORDKEY = os.environ.get('KEY', None)
CUSTOMRESPONSE1 = os.environ.get('QUINN', None)
CUSTOMRESPONSE2 = os.environ.get('QUINNBOT', None)
spam = True

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='FBI Confidential Files'))
  print("Ready")

@client.command(aliases=['tim'])
async def timbot_dialog(ctx, *, dialog_sentence):
  print(dialog_sentence)
  if ctx.message.author.id == 298625295789981697 and dialog_sentence == "togglespam":
    global spam
    if spam == True:
      spam = False
      await ctx.send("Spam mode off.")
    else:
      spam = True
      await ctx.send("Spam mode on.")
  else:
    # pass string of dialog_sentence into your code
    dialog_response = timbot.timResponse(dialog_sentence, ctx.author)
    # response
    await ctx.send(dialog_response)

@client.event
async def on_message(message):
  senderId = message.author.id
  if senderId == 789166081910112266 and spam == True:
    await message.channel.send(CUSTOMRESPONSE2)
  elif senderId == 256984382546509824 and spam == True:
    await message.channel.send(CUSTOMRESPONSE1)
  await client.process_commands(message) # Needed to make other commands work since we overrided the default on_message

if __name__ == "__main__":
  client.run(DISCORDKEY)