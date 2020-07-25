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

@bot.event
async def on_member_join(member):
    guild = member.guild
    roles = guild.roles
    player_role = None
    for role in roles:
        if role.name == "Player":
            player_role = role
            break
    if player_role != None:
        await member.add_roles(player_role)

def get_main_char(user_id):
        try:
            char = db.char_sheets.find_one({"user":user_id, "main":"true"})
            if char != None:
                return char
            else:
                return {}
        except expression as identifier:
            return {}

def generate_char(name, user_id):
        elements = ["fire", "air", "earth", "water"]
        affinity = random.choice(elements)
        char = {
            "name":name,
            "user": user_id,
            "status": "alive",
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
            "cp":0,
            "gold":0,
            "ip":0,
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
            title = char["name"],
            color = 0xfcba03
        )
        embed.add_field(name = "STR", value = char["str"])
        embed.add_field(name = "DEX", value = char["dex"])
        embed.add_field(name = "VIT", value = char["vit"])
        embed.add_field(name = "INT", value = char["int"])
        embed.add_field(name = "PER", value = char["per"])
        embed.add_field(name = "CHA", value = char["cha"])
        embed.add_field(name = "DEF", value = char["def"])
        embed.add_field(name = "HP", value = char["hp"])
        embed.add_field(name = "MP", value = char["mp"])
        embed.add_field(name = "CP", value = char["cp"])
        embed.add_field(name = "IP", value = char["ip"])
        embed.add_field(name = "Gold", value = char["gold"])
        embed.set_footer(text = "LV: {}\nXP: {}/{}\naffinity: {}\nstatus: {}"
        .format(char["lv"], char["xp"], char["lv"]*10, char["affinity"], char["status"] ))

        return embed

def save_char(char):
        db.char_sheets.insert_one(char)
        print("Saved '{}' for user_id '{}'".format(char["name"], char["user"]))

def update_char(char):
    db.char_sheets.update_one({ "_id" : char["_id"] }, {"$set":char})
    print("Updated '{}' for user_id '{}'".format(char["name"], char["user"]))

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
    try:
        name = ''
        if len(argv) > 0:
            for word in argv:
                name += word + ' '

            char = generate_char(name, ctx.author.id)
            main = get_main_char(ctx.author.id)
            if main == {}:
                char["main"] = "true"
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
async def char(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.char_sheets.find({"user":ctx.author.id}):
            if i == ( int(index)-1 ):
                embed = embed_sheet(char)
                await ctx.send(embed = embed)
                found = True
                break
            i += 1
        if found == False:
            await ctx.send("Character was not found")
    except:
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

@bot.command()
async def test(ctx, type, *argv):
    try:
        char = get_main_char(ctx.author.id)
        blocked_status = ["dead", "unconscious"]
        if char["status"] not in blocked_status:
            if type == "str":
                value = random.randint(1, 20) 
                result = value + char["str"]
                await ctx.send("{} attempts a Test of Strength!!\n{}!! ({} + {})".format(char["name"], result, value, char["str"]))
            if type == "dex":
                value = random.randint(1, 20) 
                result = value + char["dex"]
                await ctx.send("{} attempts a Test of Dexterity!!\n{}!! ({} + {})".format(char["name"], result, value, char["dex"]))
            if type == "vit":
                value = random.randint(1, 20) 
                result = value + char["vit"]
                await ctx.send("{} attempts a Test of Vitality!!\n{}!! ({} + {})".format(char["name"], result, value, char["vit"]))
            if type == "int":
                value = random.randint(1, 20) 
                result = value + char["int"]
                await ctx.send("{} attempts a Test of Intelligence!!\n{}!! ({} + {})".format(char["name"], result, value, char["int"]))
            if type == "per":
                value = random.randint(1, 20) 
                result = value + char["per"]
                await ctx.send("{} attempts a Test of Perception!!\n{}!! ({} + {})".format(char["name"], result, value, char["per"]))
            if type == "cha":
                value = random.randint(1, 20) 
                result = value + char["cha"]
                await ctx.send("{} attempts a Test of Charisma!!\n{}!! ({} + {})".format(char["name"], result, value, char["cha"]))
        else:
            await ctx.send("{} is unable to test because it's {}.".format(char["name"], char["status"]))
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def hit(ctx, player, damage, *argv):
    try:
        guild = ctx.guild
        user = guild.get_member_named( player )
        if user != None:
            char = get_main_char( user.id )
            char["hp"] -= int(damage)
            if char["hp"] > 0:
                await ctx.send("{} has taken {}pts of damage! It now has {}hp.".format(char["name"], damage, char["hp"]))
            else:#Dying
                successes = 0
                fails = 0
                while True:
                    roll = random.randint(1, 20)
                    if roll >= 10:
                        successes += 1
                        if successes == 3:
                            char["hp"] = 0
                            char["status"] = "unconscious"
                            update_char(char)
                            await ctx.send("{} is unconscious and very weak now!".format(char["name"]))
                            break
                    else:
                        fails += 1
                        if fails == 3:
                            char["hp"] = 0
                            char["status"] = "dead"
                            update_char(char)
                            await ctx.send("{} has taken {}pts of damage! It is now dead.".format(char["name"], damage))
                            break
            update_char(char)
        else:
            await ctx.send("{} was not found. You might have forgot capital letters.".format(player))
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def rest(ctx, *argv):
    try:
        blocked_status = ["dead"]
        char = get_main_char(ctx.author.id)
        if char["status"] not in blocked_status:
            char["hp"] = 12 + char["vit"]
            char["mp"] = 10 + char["int"]
            char["status"] = "alive"
            await ctx.send("{} is now resting...".format(char["name"]))
            update_char(char)
        else:
            await ctx.send("{} can't rest because it is {} right now.".format(char["name"], char["status"]))
    except:
        await ctx.send("Something didn't go well :|")

@bot.command()
async def res(ctx, username, *argv):
    try:
        isGM = False
        for role in ctx.author.roles:
            if role.name == "Game Master":
                isGM = True
                break
        if isGM:
            player = ctx.guild.get_member_named(username)
            if player != None:
                char = get_main_char(player.id)
                if char != {}:
                    char["status"] = "alive"
                    char["hp"] = 12 + char["vit"]
                    char["mp"] = 10 + char["int"]
                    update_char(char)
                    await ctx.send("{} came back from the dead.".format(char["name"]))
                else:
                    await ctx.send("No character was found.")
            else:
                await ctx.send("{} was not found.".format(username))
        else:
            await ctx.send("You must be a Game Master to use this command.")
    except expression as identifier:
        await ctx.send("Something didn't go well :|")

@bot.command()
async def givexp(ctx, xp, *argv):
    try:
        isGM = False
        for role in ctx.author.roles:
            if role.name == "Game Master":
                isGM = True
                break
        if isGM:
            names = ""
            levelup_messages = []
            for username in argv:
                player = ctx.guild.get_member_named(username)
                if player != None:
                    char = get_main_char(player.id)
                    if char != None:
                        char["xp"] += int(xp)
                        if char["xp"] >= ( char["lv"] * 10 ):
                            left = char["xp"] - ( char["lv"] * 10 )
                            char["xp"] = left
                            char["lv"] += 1
                            char["ip"] += 1
                            if char["lv"] % 2 != 0:
                                char["cp"] += 1
                            levelup_messages.append( "{} leveled up! Level {} now!".format(char["name"], char["lv"]) )
                        update_char(char)
                        names += username + ", "
            if names != "":
                names = names[:-2]
            await ctx.send("{}xp was given to {}!".format(xp, names))
            for msg in levelup_messages:
                await ctx.send(msg)
        else:
            await ctx.send("It's necessary to be a Game Master in order to execute this command.")
    except expression as identifier:
        await ctx.send("Something didn't go well :|")

@bot.command()
async def givegold(ctx, gold, *argv):
    # try:
        isGM = False
        for role in ctx.author.roles:
            if role.name == "Game Master":
                isGM = True
                break
        if isGM:
            names = ""
            for username in argv:
                player = ctx.guild.get_member_named(username)
                if player != None:
                    char = get_main_char(player.id)
                    if char != None:
                        char["gold"] += int(gold)
                        update_char(char)
                        names += username + ", "
            if names != "":
                names = names[:-2]
            await ctx.send("{} of gold was given to {}.".format(gold, names))
        else:
            await ctx.send("You must be a Game Master in order to use this command.")
    # except expression as identifier:
        # await ctx.send("Something didn't go well :|")

bot.run(TOKEN)