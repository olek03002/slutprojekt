import os
import discord
from discord.ext import commands

TOKEN = open("slutprojekt/secret3.key").read()

help_command = commands.DefaultHelpCommand(no_category = "Commands")
client = commands.Bot(command_prefix=commands.when_mentioned_or("-", "play "), case_insensitive=True, help_command=help_command)

# ctx.author = namnet på personen som skriver meddelandet i discord.

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
for fileName in os.listdir("./slutprojekt/cogs"):
    if fileName.endswith(".py"):
            client.load_extension(f"cogs.{fileName[:-3]}")

client.run(TOKEN)