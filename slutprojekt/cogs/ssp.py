import discord
import random
import json
from discord.ext import commands
from datetime import datetime, timezone

class ssp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name= "ssp", help= "sten sax påse mot boten med bet")
    async def ssp(self, ctx, *bet):
        economy = self.client.get_cog("Economy")
        await economy.addProbability("totalssp")
        saldo = economy.getBalance(ctx.author)

        try: 
            if str(bet[0]) == "all":
                bet = int(saldo) 
            else:
                bet = int(bet[0])
        except:
            bet = 0

        if int(bet) > int(saldo):
            await ctx.send("Du har inte så mycket pengar \nSpela igen")
            return
        await economy.withdrawMoney(ctx.author, int(bet))
        if int(bet) != 0:
            await ctx.send(ctx.message.author.mention + "\nSten sax eller påse? Bet: $" + str(bet))
        else:
            await ctx.send(ctx.message.author.mention + "\nSten sax eller påse? No bet")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author and m.content in ["sten", "sax", "påse"]

        ssplist = ["sten", "sax", "påse"]
        botsvar = random.choice(ssplist)
        
        print(botsvar)

        try:
            msg = await self.client.wait_for("message", timeout=30.0, check=check)
        except:
            await ctx.send("Timed out!")

        if msg.content in ("sten", "sax", "påse"):
            
            checklist = [["sten", "sax", "påse"], ["påse", "sax", "sten"], ["sax", "sten", "påse"]] # tar ett random svar ur ssplist och jämför med indexet i checklist
            checklist = checklist[ssplist.index(msg.content)]
            resultat = checklist.index(botsvar)
            print(resultat)

            if str(botsvar) == "sten":  # lägger till ett antal i sannolikhets json filen. 
                await economy.addProbability("rock")
            elif str(botsvar) == "sax":
                await economy.addProbability("paper")
            elif str(botsvar) == "påse":
                await economy.addProbability("scissors")
            
            if resultat == 0:
                if bet == 0:
                    await ctx.send("Valde " + botsvar + "\nDu förlorade!")
                else:
                    await ctx.send("Valde " + botsvar + "\nDu förlorade!\nFörlorade bet på $" + str(int(bet)))
            elif resultat == 1:
                if bet == 0:
                    await ctx.send("Valde " + botsvar + "\nLika!")
                else:
                    await ctx.send("Valde " + botsvar + "\nLika!\nBet retunerat")
                    await economy.depositMoney(ctx.author, int(bet))
            elif resultat == 2:
                
                if bet == 0:
                    await ctx.send("Valde " + botsvar + "\nDu vann!")
                else:
                    await ctx.send("Valde " + botsvar + "\nDu vann!\nBet dubblerat, vann: $" + str(int(bet)*2))
                    await economy.depositMoney(ctx.author, int(bet)*2)
            
def setup(client):
    client.add_cog(ssp(client))