import os
import discord
from discord.ext import commands

TOKEN = open("discordbot/keys/secret3.key").read()

client = commands.Bot(command_prefix=["-"], case_insensitive=True)

mememes = client.get_channel(685606448327294990)
isaksightseeing = client.get_channel(811957878448455742)
meet = client.get_channel(702054967808360449)
kod = client.get_channel(758333123338436618)
photoshop = client.get_channel(807232533032599653)
thottierlistt = client.get_channel(830053241915703306)
thotspam = client.get_channel(830765962273488897)

@client.command(name="Load", aliases=["reload"])
async def load(ctx, extension):
    try:
        client.load_extension(f"cogs.{extension}")
    except:
        try:
            client.unload_extension(f"cogs.{extension}")
            client.load_extension(f"cogs.{extension}")
        except:
            await ctx.message.add_reaction("👎")
        else:
            await ctx.message.add_reaction("🔄")
    else:
        await ctx.message.add_reaction("👍")

# Unload extension
@client.command(name="Unload")
async def unload(ctx, extension):
        client.unload_extension(f"cogs.{extension}")

# Load all Cogs on startup
for fileName in os.listdir("./Discordbot/cogs"):
    if fileName.endswith(".py"):
            client.load_extension(f"cogs.{fileName[:-3]}")

client.run(TOKEN)