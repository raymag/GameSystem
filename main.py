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

def open_database():
    try:
        db_file = open("db.txt", "r").read().split("\n")
        username = db_file[0]
        password = db_file[1]
        database_id = db_file[2]
        
    except:
        username = os.environ.get("DATABASE_USERNAME")
        password = os.environ.get("DATABASE_PASSWORD")
        database_id = os.environ.get("DATABASE_NAME")
    client = MongoClient("mongodb+srv://"+username+":"+password+"@gamesystem.xuigc.mongodb.net/"+database_id+"?retryWrites=true&w=majority")
    return client.server

bot = commands.Bot(command_prefix='$')
token_file = "token.txt"
db = open_database()

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
        if dice == "d8":
            result = random.randint(1, 8)
            result = add_modifier(result, argv)
            await ctx.send(result)
    except expression as identifier:
        await ctx.send("Something is not right :c")

@bot.command()
async def newchar(ctx, *argv):
    def generate_char(name, user_id):
        elements = ["fire", "air", "earth", "water"]
        affinity = random.choice(elements)
        char = {
            "name":name,
            "user": user_id,
            "str":0,
            "dex":0,
            "vit":0,
            "int":0,
            "per":0,
            "cha":random.randint(-2, 2),
            "def":0,
            "hp":0,
            "mp":0,
            "lv":1,
            "xp":0,
            "affinity": affinity,
            "main": "false"
        }
        if affinity == "fire":
            char["str"] += 1
            char["int"] -= 1
        if affinity == "water":
            char["int"] += 1
            char["str"] -= 1
        if affinity == "air":
            char["dex"] += 1
            char["vit"] -= 1
        if affinity == "earth":
            char["vit"] += 1
            char["dex"] -= 1
        char["def"] = 10+char["dex"]+char["vit"]
        char["hp"] = 12+char["vit"]
        char["mp"] = 10+char["int"]

        return char
    def embed_sheet(char):
        embed = discord.Embed(
            title = name,
            color = 0xfcba03
        )
        embed.add_field(name = "str", value = char["str"])
        embed.add_field(name = "dex", value = char["dex"])
        embed.add_field(name = "vit", value = char["vit"])
        embed.add_field(name = "int", value = char["int"])
        embed.add_field(name = "per", value = char["per"])
        embed.add_field(name = "cha", value = char["cha"])
        embed.add_field(name = "DEF", value = char["def"])
        embed.add_field(name = "HP", value = char["hp"])
        embed.add_field(name = "MP", value = char["mp"])
        embed.set_footer(text = "LV: {}\nXP: {}/{}\naffinity: {}".format(char["lv"], char["xp"], char["lv"]*10, char["affinity"] ))

        return embed

    def save_char(char):
        db.char_sheets.insert_one(char)
        print("Saved '{}' for user_id '{}'".format(char["name"], char["user"]))
    try:
        name = ''
        if len(argv) > 0:
            for word in argv:
                name += word + ' '

            char = generate_char(name, ctx.author.id)
            save_char(char)
            embed = embed_sheet(char)

            await ctx.send(embed = embed)
        else:
            await ctx.send("No name given")
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def chars(ctx, *argv):
    try:
        chars = []
        allchars = ""
        n = 1
        for char in db.char_sheets.find({"user":ctx.author.id}):
            chars.append(char)
            if char["main"] != "false":
                allchars += "{}. {} [MAIN]\n".format(n, char["name"])
            else:
                allchars += "{}. {}\n".format(n, char["name"])
            n += 1
            
        embed = discord.Embed(
            title = "All {}'s Characters".format(ctx.author.name),
            color = 0xfcba03,
            description = allchars
        )
        await ctx.send(embed = embed)
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def setmain(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.char_sheets.find({"user":ctx.author.id}):
            if i == ( int(index) - 1 ):
                db.char_sheets.update_many({"user":ctx.author.id}, {"$set":{ "main":"false" }})
                db.char_sheets.update_one({ "_id" : char["_id"] }, {"$set":{ "main":"true" }})
                found = True
                await ctx.send("Character {} is now the main".format(char["name"]))
                break
            i += 1
        if found == False:
            await ctx.send("Character was not found")
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def delchar(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.char_sheets.find({"user":ctx.author.id}):
            if i == ( int(index) - 1 ):
                db.char_sheets.delete_one({ "_id" : char["_id"] })
                found = True
                await ctx.send("Character {} has been removed".format(char["name"]))
                break
            i += 1
        if found == False:
            await ctx.send("Character was not found")
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

bot.run(TOKEN)