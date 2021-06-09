import discord
import youtube_dl
import asyncio
import os
import time
from discord import FFmpegPCMAudio
from discord.ext import commands
from datetime import datetime, timezone

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)
        player = player

ydl_opts = {                                          # inställningar för nedladdnings bibliotek
                "format": "bestaudio/best",
                "download_archive:": "./låtar/",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }

class musik(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, help= "spela en låt")
    async def play(self, ctx, url:str):
        voice_channel = ctx.author.voice.channel
        try: 
            voice = await voice_channel.connect()
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
            source = FFmpegPCMAudio("song.mp3")
            player = voice.play(source)
            player = player

        except:
            try:    # provar detta och om ger felmeddelande så gör den det som finns i "except" istället
                os.remove("song.mp3")
                time.sleep(1)
                voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                source = FFmpegPCMAudio("song.mp3")
                player = voice.play(source)
            except:
                voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                source = FFmpegPCMAudio("song.mp3")
                player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        guild_id = ctx.message.guild.id 
        
        if voice.is_playing():
            if guild_id in queues:
                queues[guild_id].append(source)
            else:
                queues[guild_id] = [source]
            #await ctx.send("Added to queue!")


    @commands.command(pass_context=True, help= "återuppta")
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Inget ljud pausat!")

    @commands.command(pass_context=True, help= "pausa")
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Inget ljud spelas!")

    @commands.command(pass_context=True, help= "stoppa")
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        try:
            time.sleep(1)
            os.remove("song.mp3")
        except:
            print("kunde inte ta bort song.mp3")

    @commands.command(help= "koppla ifrån boten")
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild = ctx.guild)
        try:
            try:
                await voice.disconnect()
                await ctx.message.add_reaction('🆗')
                time.sleep(1)
                os.remove("song.mp3")
            except:
                await voice.disconnect()
                await ctx.message.add_reaction('🆗')
        except:
            await ctx.send("jag är inte i en röstkanal 😥")
            await ctx.message.add_reaction('😥')

def setup(client):
    client.add_cog(musik(client))
