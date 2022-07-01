from jaraco.docker import is_docker
import json
from discord.ext import commands, tasks
import discord
import logging
import os
from datetime import datetime
import pickle
from history import History

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

HISTORY = History()

bot = commands.Bot(PREFIX)


@bot.event
async def on_ready():
    logging.log(logging.INFO, f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Map History"))
    queryServer.start()


@tasks.loop(seconds=INTERVAL)
async def queryServer():

    logging.log(logging.DEBUG, "Entering Query loop")
    try:
        logging.log(
            logging.INFO, f"Connecting to {SERVERADDRESS[0]}:{SERVERADDRESS[1]}")

        
        logging.log(logging.INFO, f"Current map: {HISTORY.query(SERVERADDRESS)}")
        logging.log(logging.INFO, f"Last map: {HISTORY.getLastMap()}")

        try:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Map History | {HISTORY.getCurrentMap()}"))
        except:
            pass
    except Exception as e:
        logging.log(logging.ERROR, f"Couldnt complete a2s query. {e}")

    finally:
        try:
            await update_staticEmbed()
        except:
            pass


async def generate_embed():
    embed = discord.Embed(title=f"Map History for `{HISTORY.getServerName()}`", description="", color=0xff0000)
    embed.set_author(name="Map History Bot",
                     url="https://github.com/immervoll/maphistory-bot")
    embed.add_field(name="📍 Current Map",
                    value=f"""{HISTORY.getFormattedCurrentMap()}""", inline=False)
    embed.add_field(name="⌛ Previous Map",
                    value=f"""{HISTORY.getFormattedLastMap()}""", inline=False)
    embed.add_field(name="🗺️ Last 10 Maps",
                    value=f"{HISTORY.getFormattedLast10Maps()}", inline=False)
    embed.add_field(name="⌚ Last refresh", value=f"<t:{HISTORY.getLastUpdate()}:R>")
    embed.set_footer(text="by immervoll")
    return embed


async def update_staticEmbed():
    with open('embed.pickle', 'rb') as embedPickleFile:
        staticEmbedInfo = pickle.load(embedPickleFile)

    message = await bot.get_channel(staticEmbedInfo[0]).fetch_message(staticEmbedInfo[1])

    embed = await generate_embed()
    await message.edit(embed=embed)


@bot.command(name="history", aliases=["maps"])
async def history(ctx: commands.Context):
    logging.log(logging.INFO, f"{ctx.author} requested the map history")
    embed = await generate_embed()
    await ctx.send(f">>> {ctx.author.mention} here is the servers map history", embed=embed)


@bot.command(name="setup",
             aliases=["set"],
             usage="!setup <channel> - sets up a the channel to host the perma history info",
             description="sets up a channel to host a self updating embed showing the server history")
@commands.guild_only()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 2, commands.BucketType.member)
async def setup(ctx: commands.Context, *, channelID: int):

    channel = discord.utils.get(bot.get_all_channels(), id=channelID)

    embed = await generate_embed()
    message = await channel.send(embed=embed)

    staticEmbedInfo = [channel.id, message.id]
    with open('embed.pickle', 'wb') as embedPickleFile:
        pickle.dump(staticEmbedInfo, embedPickleFile)

    await ctx.send(f"Set up embed in {channel.mention}")
bot.run(TOKEN)
