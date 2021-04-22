import discord
from discord.ext import commands
from datetime import datetime, timezone

botsvar = ["sten", "sax", "påse"]

class ssp(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def helen2(self, ctx):
        await ctx.send("HELENA <:helenium:829301282220015676>")

    @commands.command()
    async def ssp(self, ctx, svar):
        botsvar.remove(svar)
        print("hrggdfgej")
        

def setup(client):
    client.add_cog(ssp(client))