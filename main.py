import discord
import random
import requests
import time
import json
import math
import asyncio
import os

from discord.ext import commands
from pymongo import MongoClient

bot = commands.Bot(command_prefix='$')
token_file = "token.txt"

try:
    with open(token_file) as f:
        TOKEN = f.read()
except:
    TOKEN = os.environ.get('TOKEN')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def roll(ctx, dice, *argv): 
    try:
        if dice == "d20":
            result = random.randint(1, 20)
            await ctx.send("{}!".format(result))

        if dice == "d6":
            result = random.randint(1, 6)
            await ctx.send("{}!".format(result))
        if dice == "2d6":
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6)
            rf = r1+r2
            await ctx.send("{}! ({} + {})".format(rf, r1, r2))
        if dice == "3d6":
            r1 = random.randint(1, 6)
            r2 = random.randint(1, 6)
            r3 = random.randint(1, 6)
            rf = r1 + r2 + r3
            await ctx.send("{}! ({} + {} + {})".format(rf, r1, r2, r3))
    except expression as identifier:
        pass



bot.run(TOKEN)