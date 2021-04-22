import discord
from discord.ext import commands
from datetime import datetime, timezone

class blackjack(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def helen(self, ctx):
        await ctx.send("HELENA <:helenium:829301282220015676>")
        

def setup(client):
    client.add_cog(blackjack(client))