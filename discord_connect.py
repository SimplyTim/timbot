import discord
import timbot
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.' , case_insensitive=True)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='FBI Confidential Files'))
  print("Ready")


@client.command(aliases=['tim'])
async def timbot_dialog(ctx, *, dialog_sentence):
  # pass string of dialog_sentence into your code
  dialog_response = timbot.timResponse(dialog_sentence, ctx.author)
  # response
  await ctx.send(dialog_response)

if __name__ == "__main__":
  client.run("Nzg5MTczMTg4NTQ5ODA0MTIz.X9uMzg.m9_xFlJZSxgpLHNpnkcnrh4qrvM")