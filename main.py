from jaraco.docker import is_docker
import json
from discord.ext import commands, tasks
import discord
import a2s
import logging
import os
from datetime import datetime
import time
import pickle

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

FIELPATH = "./history.txt"  # Path to the file to save the history


bot = commands.Bot(PREFIX)
last_map: str = ""


@bot.event
async def on_ready():
    logging.log(logging.INFO, f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Map History"))
    queryServer.start()


@tasks.loop(seconds=INTERVAL)
async def queryServer():
    global last_map
    logging.log(logging.DEBUG, "Entering Query loop")
    try:
        logging.log(
            logging.INFO, f"Connecting to {SERVERADDRESS[0]}:{SERVERADDRESS[1]}")

        query = a2s.info(SERVERADDRESS)
        current_map = query.map_name

        if not current_map == last_map:
            with open(FIELPATH, "a") as file:
                file.write(f"{current_map}\n")
                logging.log(logging.INFO, f"Saved map to File")
                logging.log(logging.INFO, f"Current map: {current_map}")
                logging.log(logging.INFO, f"Last map: {last_map}")

            last_map = current_map
        else:
            logging.log(logging.INFO, f"Current map: {current_map}")

        try:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Map History | {current_map}"))
        except:
            pass
    except Exception as e:
        logging.log(logging.ERROR, f"Couldnt complete a2s query. {e}")

    finally:
        try:
            await update_staticEmbed()
        except:
            pass


async def update_staticEmbed():
    with open('embed.pickle', 'rb') as embedPickleFile:
        staticEmbedInfo = pickle.load(embedPickleFile)

    message = await bot.get_channel(staticEmbedInfo[0]).fetch_message(staticEmbedInfo[1])

    last_10_maps = "".join(get_last_10_maps())
    embed = discord.Embed(title="Map History", description="", color=0xff0000)
    embed.set_author(name="Map History Bot",
                     url="https://github.com/immervoll/maphistory-bot")
    embed.add_field(name="Current Map", value="".join(
        get_current_map()), inline=False)
    embed.add_field(name="Last 10 Maps", value=f"{last_10_maps}", inline=False)
    embed.add_field(name="Last refresh", value=f"<t:{int(time.time())}:R>")
    embed.set_footer(text="by immervoll")
    embed.timestamp = datetime.now()
    await message.edit(embed=embed)


def get_last_10_maps():
    with open(FIELPATH, "r") as file:
        return file.readlines()[-10:]


def get_current_map():
    with open(FIELPATH, "r") as file:
        return file.readlines()[-1]


@bot.command(name="history", aliases=["maps"])
async def history(ctx: commands.Context):
    logging.log(logging.INFO, f"{ctx.author} requested the map history")
    last_10_maps = "".join(get_last_10_maps())
    embed = discord.Embed(title="Map History", description="", color=0xff0000)
    embed.set_author(name="Map History Bot",
                     url="https://github.com/immervoll/maphistory-bot")
    embed.add_field(name="Current Map", value="".join(
        get_current_map()), inline=False)
    embed.add_field(name="Last 10 Maps", value=f"{last_10_maps}", inline=False)
    embed.set_footer(text="by immervoll")
    await ctx.send(f"{ctx.author.mention} here is the servers map history", embed=embed)


@bot.command(name="setup",
             aliases=["set"],
             usage="!setup <channel> - sets up a the channel to host the perma history info",
             description="sets up a channel to host a self updating embed showing the server history")
@commands.guild_only()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 2, commands.BucketType.member)
async def setup(ctx: commands.Context, *, channelID: int):

    channel = discord.utils.get(bot.get_all_channels(), id=channelID)

    last_10_maps = "".join(get_last_10_maps())
    embed = discord.Embed(title="Map History", description="", color=0xff0000)
    embed.set_author(name="Map History Bot",
                     url="https://github.com/immervoll/maphistory-bot")
    embed.add_field(name="Current Map", value="".join(
        get_current_map()), inline=False)
    embed.add_field(name="Last 10 Maps", value=f"{last_10_maps}", inline=False)
    embed.add_field(name="Last refresh", value=f"<t:{int(time.time())}:R>")
    embed.set_footer(text="by immervoll")
    embed.timestamp = datetime.now()
    message = await channel.send(embed=embed)

    staticEmbedInfo = [channel.id, message.id]
    with open('embed.pickle', 'wb') as embedPickleFile:
        pickle.dump(staticEmbedInfo, embedPickleFile)

    await ctx.send(f"Set up embed in {channel.mention}")
bot.run(TOKEN)
