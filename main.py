from jaraco.docker import is_docker
import json
from discord.ext import commands, tasks
import discord
import logging
import os
from datetime import datetime
import pickle
from guild import Guild
from history import History
import re

logging.basicConfig(level=logging.INFO)

if is_docker():
    TOKEN = os.environ['TOKEN']
    PREFIX = os.environ['PREFIX']
    SERVERADDRESS = (os.environ['IP'], int(os.environ["PORT"]))
    INTERVAL = float(os.environ['INTERVAL'])

else:
    with open("configuration.json", "r") as config:
        DATA = json.load(config)
        TOKEN = DATA["TOKEN"]
        PREFIX = DATA["PREFIX"]
        SERVERADDRESS = (DATA["SERVER"]["IP"], DATA["SERVER"]["PORT"])
        INTERVAL = DATA["INTERVAL"]

GUILDS: list[Guild]

bot = commands.Bot(PREFIX)


@bot.event
async def on_ready():
    logging.log(logging.INFO, f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Map History"))
    queryServer.start()


@tasks.loop(seconds=INTERVAL)
async def queryServer():

    logging.log(logging.DEBUG, "Entering Query loop")
    for guild in GUILDS:
        this = GUILDS.index(guild)
        try:
            logging.log(logging.DEBUG, f"Querying server for {this}")
            guild.updateEmbeds()
        except Exception as e:
            logging.log(logging.ERROR, f"Error in queryServer: {this}\n\n{e}")


@bot.group()
async def setup(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid setup command passed...')


@setup.command()
async def guild(ctx):
    await ctx.send(f"Setting up guild {ctx.guild.name}")
    pass


@setup.command()
async def history(ctx, ip: str, port: int):
    assert re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                    ip), "Invalid IP address"
    assert port > 0 and port < 65536, "Invalid port"
    await ctx.send(f"Setting up history for {ip}:{port}")
    pass


@setup.command()
async def embed(ctx, channel: discord.TextChannel, historyid: int):
    await ctx.send(f"Setting up embed for {channel.name} with history {historyid}")
    pass


@setup.command()
async def show(ctx):
    await ctx.send(f"Showing setup")
    pass


@setup.command()
async def guide(ctx):
    await ctx.send(f"Setup guide")
    pass


@setup.command()
async def clear(ctx):
    await ctx.send(f"Clearing setup for guild {ctx.guild.name}")
    pass
bot.run(TOKEN)
