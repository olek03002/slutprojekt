import discord
import youtube_dl
import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands
from datetime import datetime, timezone

class musik(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def play(self, ctx, url, help= "spela en låt"):
        voice_channel = ctx.author.voice.channel
        voice = await voice_channel.connect()
        source = FFmpegPCMAudio("slutprojekt/rick.mp3")
        player = voice.play(source)
        #author = ctx.message.author
        #player = await voice.create_ytdl_player(url)
        #player.start()

    @commands.command()
    async def kys(self, ctx, help= "koppla ifrån boten"):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        try:
            await voice.disconnect()
            await ctx.message.add_reaction('🆗')
        except:
            await ctx.send("jag är inte i en röstkanal 😥")
            await ctx.message.add_reaction('😥')

        
def setup(client):
    client.add_cog(musik(client))
