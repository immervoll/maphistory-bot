from jaraco.docker import is_docker
import json
from discord.ext import commands, tasks
import discord
import a2s
import logging
import os
from datetime import datetime
logging.basicConfig(level=logging.INFO)

if is_docker():
    TOKEN = os.environ['TOKEN']
    PREFIX = os.environ['PREFIX']
    SERVERADDRESS = (os.environ['IP'], os.environ["PORT"])

else:
    with open("configuration.json", "r") as config:
        DATA = json.load(config)
        TOKEN = DATA["TOKEN"]
        PREFIX = DATA["PREFIX"]
        SERVERADDRESS = (DATA["SERVER"]["IP"], DATA["SERVER"]["PORT"])
        MESSAGEID = DATA["MESSAGEID"]

INTERVAL = 600.0  # Interval in seconds to check the server
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
        embed=discord.Embed(title="Map History", description="", color=0xff0000)
        embed.set_author(name="Map History Bot", url="https://github.com/immervoll/maphistory-bot", icon_url="icon")
        embed.add_field(name="Current Map", value=f"{current_map}", inline=False)
        embed.add_field(name="Last 10 Maps", value=f"{last_map}", inline=False)
        from datetime import datetime
        embed.set_footer(text=f"Last update: {datetime.now()}")
        
        await ctx.send(embed=embed)

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

bot.run(TOKEN)
