import character

import discord
import random
import asyncio
import os

import gamesystem

from discord.ext import commands
from pymongo import MongoClient

def open_database():
    try:
        db_file = open("./db.txt", "r").read().split("\n")
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
token_file = "./token.txt"
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
    if player_role:
        await member.add_roles(player_role)

def get_main_char(user_id):
        try:
            char = db.characters.find_one({"_Character__user":user_id, "_Character__main": True})
            if not char:
                return {}
            return char
        except expression as identifier:
            return {}

def generate_char(name, user_id):
        char = character.Human(name, user = user_id)
        return char

def embed_sheet(char):
        attributes = char.get_attributes()
        embed = discord.Embed(
            title = char.get_name(),
            color = 0xfcba03
        )
        embed.add_field(name = "STR", value = attributes["str"])
        embed.add_field(name = "DEX", value = attributes["dex"])
        embed.add_field(name = "VIT", value = attributes["vit"])
        embed.add_field(name = "INT", value = attributes["int"])
        embed.add_field(name = "PER", value = attributes["per"])
        embed.add_field(name = "CHA", value = attributes["cha"])
        embed.add_field(name = "DEF", value = char.get_def())
        embed.add_field(name = "HP", value = char.get_hp())
        embed.add_field(name = "MP", value = char.get_mp())
        embed.add_field(name = "CP", value = char.get_cp())
        embed.add_field(name = "IP", value = char.get_ip())
        embed.add_field(name = "Gold", value = char.get_gold())
        embed.set_footer(text = "LV: {}\nXP: {}/{}\naffinity: {}\nstatus: {}"
        .format(char.get_lv(), char.get_xp(), char.get_lv()*10, char.get_affinity(), char.get_status() ))

        return embed

def save_char(char):
        dict_char = char.dump()
        db.characters.insert_one(dict_char)
        print("Saved '{}' for user_id '{}'".format(char.get_name(), char.get_user()))

def update_char(char):
    db.characters.update_one({ "_id" : char["_id"] }, {"$set":char})
    print("Updated '{}' for user_id '{}'".format(char["_Character__name"], char["_Character__user"]))

@bot.command()
async def roll(ctx, dice, *argv): 
    def add_modifier(value, *argv):
        try:
            if argv:
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
            if not main:
                char.set_main()
            save_char(char)
            embed = embed_sheet(char)

            await ctx.send(embed = embed)
        else:
            await ctx.send("No name was given.")
    except:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def chars(ctx, *argv):
    try:
        chars = []
        allchars = []
        n = 1
        for char in db.characters.find({"_Character__user":ctx.author.id}):
            chars.append(char)
            if char["_Character__main"]:
                allchars.append("{}. {} [MAIN]\n".format(n, char["_Character__name"]))
            else:
                allchars.append("{}. {}\n".format(n, char["_Character__name"]))
            n += 1
            
        embed = discord.Embed(
            title = "All {}'s Characters".format(ctx.author.name),
            color = 0xfcba03,
            description = "".join(allchars)
        )
        await ctx.send(embed = embed)
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def char(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.characters.find({"_Character__user":ctx.author.id}):
            if i == ( int(index)-1 ):
                new_char = character.Human("humano", ctx.author.id)
                new_char.load(char)
                embed = embed_sheet(new_char)
                await ctx.send(embed = embed)
                found = True
                break
            i += 1
        if not found:
            await ctx.send("Character was not found")
    except:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def setmain(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.characters.find({"_Character__user":ctx.author.id}):
            if i == ( int(index) - 1 ):
                db.characters.update_many({"_Character__user":ctx.author.id}, {"$set":{ "_Character__main": False }})
                db.characters.update_one({ "_id" : char["_id"] }, {"$set":{ "_Character__main": True }})
                found = True
                await ctx.send("Character {} is now the main".format(char["_Character__name"]))
                break
            i += 1
        if not found:
            await ctx.send("Character was not found")
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def delchar(ctx, index, *argv):
    try:
        i = 0
        found = False
        for char in db.characters.find({"_Character__user":ctx.author.id}):
            if i == ( int(index) - 1 ):
                db.characters.delete_one({ "_id" : char["_id"] })
                found = True
                await ctx.send("Character {} has been removed".format(char["_Character__name"]))
                break
            i += 1
        if not found:
            await ctx.send("Character was not found")
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def test(ctx, type, *argv):
    try:
        char = get_main_char(ctx.author.id)
        blocked_status = ["dead", "unconscious"]
        if char["_Character__status"] not in blocked_status:
            attributes = char["_Character__attributes"]
            if type == "str":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__str"]
                await ctx.send("{} attempts a Test of Strength!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__str"]))
            if type == "dex":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__dex"]
                await ctx.send("{} attempts a Test of Dexterity!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__dex"]))
            if type == "vit":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__vit"]
                await ctx.send("{} attempts a Test of Vitality!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__vit"]))
            if type == "int":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__int"]
                await ctx.send("{} attempts a Test of Intelligence!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__int"]))
            if type == "per":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__per"]
                await ctx.send("{} attempts a Test of Perception!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__per"]))
            if type == "cha":
                value = random.randint(1, 20) 
                result = value + attributes["_Attributes__cha"]
                await ctx.send("{} attempts a Test of Charisma!!\n{}!! ({} + {})".format(char["_Character__name"], result, value, attributes["_Attributes__cha"]))
            else:
                await ctx.send("This test is invalid!")
        else:
            await ctx.send("{} is unable to test because it's {}.".format(char["_Character__name"], char["_Character__status"]))
    except expression as identifier:
        await ctx.send("Something didn't go well :| ")

@bot.command()
async def hit(ctx, player, damage, *argv):
    try:
        guild = ctx.guild
        user = guild.get_member_named( player )
        blocked_status = ["dead", "unconscious"]
        if user:
            char = get_main_char( user.id )
            char["_Character__hp"] -= int(damage)
            if char["_Character__hp"] > 0:
                await ctx.send("{} has taken {}pts of damage! It now has {}hp.".format(char["_Character__name"], damage, char["_Character__hp"]))
            else:#Dying
                successes = 0
                fails = 0
                while True:
                    roll = random.randint(1, 20)
                    if roll >= 10:
                        successes += 1
                        if successes == 3 and char["_Character__status"] not in blocked_status:
                            char["_Character__hp"] = 0
                            char["_Character__status"] = "unconscious"
                            update_char(char)
                            await ctx.send("{} is unconscious and very weak now!".format(char["_Character__name"]))
                            break
                    else:
                        fails += 1
                        if fails == 3:
                            char["_Character__hp"] = 0
                            char["_Character__status"] = "dead"
                            update_char(char)
                            await ctx.send("{} has taken {}pts of damage! It is now dead.".format(char["_Character__name"], damage))
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
        if char["_Character__status"] not in blocked_status:
            char["_Character__hp"] = 12 + char["_Character__vit"]
            char["_Character__mp"] = 10 + char["_Character__int"]
            char["_Character__status"] = "alive"
            await ctx.send("{} is now resting...".format(char["_Character__name"]))
            update_char(char)
        else:
            await ctx.send("{} can't rest because it is {} right now.".format(char["_Character__name"], char["_Character__status"]))
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
            if player:
                char = get_main_char(player.id)
                if char:
                    char["_Character__status"] = "alive"
                    attr = char["_Character__attributes"]
                    char["_Character__hp"] = 12 + attr["_Attributes__vit"]
                    char["_Character__mp"] = 10 + attr["_Attributes__int"]
                    update_char(char)
                    await ctx.send("{} came back from the dead.".format(char["_Character__name"]))
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
            names = []
            levelup_messages = []
            for username in argv:
                player = ctx.guild.get_member_named(username)
                if player:
                    char = get_main_char(player.id)
                    if char:
                        char["_Character__xp"] += int(xp)
                        while char["_Character__xp"] >= ( char["_Character__lv"] * 10 ):
                            left = char["_Character__xp"] - ( char["_Character__lv"] * 10 )
                            char["_Character__xp"] = left
                            char["_Character__lv"] += 1
                            char["_Character__ip"] += 1
                            if char["_Character__lv"] % 2 != 0:
                                char["_Character__cp"] += 1
                            levelup_messages.append( "{} leveled up! Level {} now!".format(char["_Character__name"], char["_Character__lv"]) )
                        update_char(char)
                        names.append( username + ", " )
            names = "".join(names)
            if names:
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
    try:
        isGM = False
        for role in ctx.author.roles:
            if role.name == "Game Master":
                isGM = True
                break
        if isGM:
            names = []
            for username in argv:
                player = ctx.guild.get_member_named(username)
                if player:
                    char = get_main_char(player.id)
                    if char:
                        char["_Character__gold"] += int(gold)
                        update_char(char)
                        names.append( username + ", " )
            names = "".join(names)
            if names:
                names = names[:-2]
                await ctx.send("{} of gold was given to {}.".format(gold, names))
        else:
            await ctx.send("You must be a Game Master in order to use this command.")
    except expression as identifier:
        await ctx.send("Something didn't go well :|")

@bot.command()
async def iattr(ctx, attr, *argv):
    try:
        char = get_main_char(ctx.author.id)
        if char:
            if char["_Character__cp"] > 0:
                attrs = ['str', 'dex', 'int', 'vit', 'per', 'cha']
                char_attrs = char["_Character__attributes"]
                if attr in attrs:
                    char_attrs["_Attributes__"+attr] += 1
                    char["_Character__def"] = 10+char_attrs["_Attributes__dex"]+char_attrs["_Attributes__vit"]
                    char["_Character__hp"] = 12+char_attrs["_Attributes__vit"]
                    char["_Character__mp"] = 10+char_attrs["_Attributes__int"]
                    char["_Character__cp"] -= 1
                    update_char(char)
                    await ctx.send("{} points was increased with success!".format(attr))
                else:
                    await ctx.send("Attribute {} does not exists.".format(attr))

            else:
                await ctx.send("You don't have enough CP to use.")
        else:
            await ctx.send("You don't have a main character.")
    except expression as identifier:
        await ctx.send("Something didn't go well :|")

bot.run(TOKEN)