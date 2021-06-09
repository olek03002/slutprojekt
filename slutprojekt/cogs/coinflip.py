import discord
import random
import json
from discord.ext import commands
from datetime import datetime, timezone

from discord.ext.commands import bot

class coinflip(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name= "cf", aliases=["coinflip"], help= "singla slant bet/no bet")
    async def cf(self, ctx, *bet):
        economy = self.client.get_cog("Economy")
        saldo = economy.getBalance(ctx.author)
        await economy.addProbability("totalcf")
        try: 
            if str(bet[0]) == "all":
                bet = int(saldo) 
            else:
                bet = int(bet[0])
        except:
            bet = 0
        
        if int(bet) > int(saldo):
            await ctx.send("Not enough money \nplay again")
            return
        
        cflist = ["heads", "tails"]
        botsvar = random.choice(cflist)
        print(botsvar)

        if str(botsvar) == "heads": # lägger till antal i sannoliks json filen
            await economy.addProbability("heads")
        elif str(botsvar) == "tails":
            await economy.addProbability("tails")

        await economy.withdrawMoney(ctx.author, int(bet))
        if bet == 0:
            await ctx.send(ctx.message.author.mention + "\nHeads or tails? No bet")
        else:
            await ctx.send(ctx.message.author.mention + "\nHeads or tails? Bet: $" + str(bet))
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content in ["heads", "tails"]
        try:
            msg = await self.client.wait_for("message", timeout=30.0, check=check)
        except:
            await ctx.send("Timed out!")

        if msg.content in ("heads", "tails"):
            
            checklist = [["heads", "tails"], ["tails", "heads"]] # fungerar likadant som i ssp
            checklist = checklist[cflist.index(msg.content)]
            resultat = checklist.index(botsvar)
            
            if resultat == 0:
                await economy.addStreak(ctx.author)
                streak = economy.getStreak(ctx.author)
                if bet == 0:
                    await ctx.send("You won! \nStreak: " + str(streak))
                else:
                    await ctx.send("You won!\nBet doubled, won: $" + str(int(bet)*2) + "\nStreak: " + str(streak))
                    await economy.depositMoney(ctx.author, int(bet)*2)
            elif resultat == 1:
                if bet == 0:
                    await ctx.send("You lost!" + "\nStreak lost")
                    await economy.resetStreak(ctx.author)
                else:
                    await ctx.send("You lost!\nLost bet of $" + str(int(bet) + "\nStreak lost"))
                    await economy.resetStreak(ctx.author)

def setup(client):
    client.add_cog(coinflip(client))