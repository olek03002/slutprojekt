import discord
import random
import json
from discord.ext import commands
from datetime import datetime, timezone

# def loadData():
#     with open("slutprojekt/poäng.json", "r") as f:
#         data = json.load(f)
#     return data

# def saveData(data):
#     with open("slutprojekt/poäng.json", "w") as f:
#         json.dump(data, f, sort_keys=True, indent=4)

# def getUser(member):
#     data = loadData()

#     try: # Test if member exist in data already
#         user = data[str(member.id)]

#     except: # If they don't create member
#         data[str(member.id)] = {}
#         saveData(data)
#         return getUser(member)

#     else: # If they do return member data
#         return user

# def getGameElo(member, game):
#     user = getUser(member)

#     try: # Test if user have rating in game 
#         elo = user[game] + 1

#     except:
#         data = loadData()
#         data[str(member.id)][game] = 1
#         saveData(data)

#         return getGameElo(member, game)

#     else:
#         return elo

class ssp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name= "ssp", help= "sten sax påse mot boten")
    async def ssp(self, ctx, svar):
        svar = svar.lower()
        if svar in ("sten", "sax", "påse"):
            ssplist = ["sten", "sax", "påse"]
            checklist = [["sten", "sax", "påse"], ["påse", "sax", "sten"], ["sax", "sten", "påse"]]
            botsvar = random.choice(ssplist)
            checklist = checklist[ssplist.index(svar)]
            resultat = checklist.index(botsvar)
            #print(botsvar, svar, resultat)
            if resultat == 0:
                await ctx.send("lika!")
            elif resultat == 1:
                await ctx.send("du vann!")
                #vinster = getGameElo(ctx.author, "vinster")
            elif resultat == 2:
                await ctx.send("du förlorade!")
            

def setup(client):
    client.add_cog(ssp(client))