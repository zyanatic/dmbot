import os
from os import path
import discord
from discord.ext import commands
import asyncio
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
  if message.content.startswith(">on") and message.channel.id == "223590013982474241" or message.channel.id == "432682586259718145":
    test_msg = str(message.author).split("#")[0] + " tipped in " + str(message.channel.name) + ": " + str(message.content).replace(">on", "")
    f = str(message.author).replace("#", "-") + ".txt"
    if (path.isfile(f)):
      file = open(f, 'r')
      subs = [sub for sub in file]
      file.close()
      if len(subs) > 0:
        for x in subs:
          await bot.send_message(message.server.get_member(x.replace("\n", "")), test_msg)
  await bot.process_commands(message)

@bot.command(pass_context=True)
async def sub(ctx):
  members = [str(x) for x in ctx.message.server.members]
  #name = ctx.message.content.split(">sub")[1].strip()
  name = str(ctx.message.server.get_member(str(ctx.message.mentions[0].id).replace("<@", "").replace(">", "")))
  print(name)
  print(ctx.message.author)
  if name in members and name != str(ctx.message.author) and name != "TipsBot#5822":
    name = name.replace("#","-")
    f = name + ".txt"
    print(f)
    if (path.isfile(f)):
      file = open(f, 'r')
      subs = [x.replace("\n","") for x in file]
      file.close()
    else:
      subs = []
    print(subs)
    if str(ctx.message.author.id) not in subs:
      file = open(name + ".txt", "a+")
      print(ctx.message.author.id)
      file.write(str(ctx.message.author.id) + "\n")
      file.close()
      msg = "You subscribed to " + str(ctx.message.server.get_member(str(ctx.message.mentions[0].id).replace("<@", "").replace(">", "").split("#")[0])) #name # ctx.message.content.split(">sub")[1].strip()
      # await bot.send_message(bot.get_channel('248873735715684353'), msg)
      await bot.send_message(ctx.message.author, msg)
    else:
      msg2 = "You are already subscribed to " + str(ctx.message.server.get_member(str(ctx.message.mentions[0].id).replace("<@", "").replace(">", "").split("#")[0])) #name #ctx.message.content.split(">sub")[1].strip()
      # await bot.send_message(bot.get_channel('248873735715684353'), msg2)
      await bot.send_message(ctx.message.author, msg2)

@bot.command(pass_context=True)
async def unsub(ctx):
  name = str(ctx.message.server.get_member(str(ctx.message.mentions[0].id).replace("<@", "").replace(">", "")))
  user_id = str(ctx.message.mentions[0].id).replace("<@", "").replace(">", "")
  f = name.replace("#", "-") + ".txt"
  print(f)
  subs = [line.rstrip('\n') for line in open(f)]
  print("AUTHOR", str(ctx.message.author.id))
  if str(ctx.message.author.id) in [x for x in subs]:
    newsubs = [x for x in subs if x != str(ctx.message.author.id)]
    if len(newsubs) > 0:
      with open(name.replace("#", "-") + ".txt", 'w') as fb:
        for item in newsubs:
          print(item)
          fb.write("%s\n" % item)
    else:
      open(name.replace("#", "-") + ".txt", 'w').close()
    msg = "You unsubbed from " + name
    await bot.send_message(ctx.message.author, msg)
  else:
    msg = "You were not subbed to " + name
    await bot.send_message(ctx.message.author, msg)


@bot.command(pass_context=True)
async def mysubs(ctx):
  f = str(ctx.message.author).replace("#", "-") + ".txt"
  try:
    subs = [str(ctx.message.server.get_member(line.rstrip('\n'))).split("#")[0] for line in open(f)]
    msg = "Subscribed to you: " + ", ".join(subs)
    await bot.send_message(ctx.message.author, msg)
  except Exception as e:
    msg = "No one is currently subbed to you"
    await bot.send_message(ctx.message.author, msg)


@bot.command(pass_context=True)
async def mydms(ctx):
  dms = []
  members = [str(x).replace("#", "-") for x in ctx.message.server.members]
  for member in members:
    try:
      f = member + ".txt"
      if str(ctx.message.author.id) in [line.rstrip('\n') for line in open(f)]:
        dms.append(member.split("-")[0])
    except Exception as e:
      pass
  msg = "You are getting DMs for: " + ", ".join(dms)
  await bot.send_message(ctx.message.author, msg)




#keep_alive()
bot.run(token)