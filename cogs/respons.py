import discord
from discord.ext import commands
from datetime import datetime, timezone

class respons(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name= "helen3", help= "helena och helenium")
    async def helen3(self, ctx):
        await ctx.send("HELENA <:helenium:829301282220015676>")
        

def setup(client):
    client.add_cog(respons(client))