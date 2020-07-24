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
    def add_modifier(value, *argv):
        try:
            if argv != None:
                if "+" in argv[0]:
                    mod = int(argv[0][1])
                    result = value + mod
                    return "{}! ({} + {})".format(result, value, mod)
                elif "-" in argv[0]:
                    mod = int(argv[0][1])
                    result = value - mod
                    return "{}! ({} - {})".format(result, value, mod)
            return "{}!".format(value)
        except expression as identifier:
            return "{}!".format(value)
    try:
        if dice == "d20":
            result = random.randint(1, 20)
            result = add_modifier(result, argv)
            await ctx.send(result)

        if dice == "d6":
            result = random.randint(1, 6)
            result = add_modifier(result, argv)
            await ctx.send(result)
        if dice == "2d6":
            result = random.randint(1, 6) + random.randint(1, 6)
            result = add_modifier(result, argv)
            await ctx.send(result)
        if dice == "3d6":
            result = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
            result = add_modifier(result, argv)
            await ctx.send(result)
    except expression as identifier:
        await ctx.send("Something is not right :c")



bot.run(TOKEN)