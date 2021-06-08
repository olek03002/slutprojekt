import discord
from discord.ext import commands
from datetime import datetime, timezone

class system(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.client.user} är online!')
        activity = discord.Game(name="World domination simulator", type=3)
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        #mememes = client.get_channel(685606448327294990)    \
        #await mememes.send("redo")                          /  -- skickar i en viss textkanal att boten är online

    @commands.command(name= "ping", help= "ping för boten och api") 
    async def ping(self,ctx):
        dt = datetime.now(tz=timezone.utc)
        naive = dt.replace(tzinfo=None)
        await ctx.send(f":ping_pong: Bot Latency is {round((naive - ctx.message.created_at).total_seconds() * 1000)}ms. API Latency is {round(self.client.latency * 1000)}ms")

def setup(client):
    client.add_cog(system(client))