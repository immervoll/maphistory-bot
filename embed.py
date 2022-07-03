from email import message
from history import History
import discord
from main import generate_embed, history
class Embed(object):
    """Class representing an embeded selfrefreshing message."""
    channel: discord.TextChannel
    message: discord.Message
    history: History
    def __init__(self, channel: discord.TextChannel, history: History):
        self.channel = channel
        self.history = history
        self.message = None
        self.updateEmbed()
        
    def updateEmbed(self):
        if self.message is None:
            self.message = self.channel.send(embed=self.generateEmbed())
        else:
            self.message.edit(embed=self.generateEmbed())
        return self.message
        
    def generateEmbed(self):
        embed = discord.Embed(
                title=f"Map History for `{self.history.getServerName()}`", description="", color=0xff0000)
        embed.set_author(name="Map History Bot",
                        url="https://github.com/immervoll/maphistory-bot")
        embed.add_field(name="📍 Current Map",
                        value=f"""{self.history.getFormattedCurrentMap()}""", inline=False)
        embed.add_field(name="⌛ Previous Map",
                        value=f"""{self.history.getFormattedLastMap()}""", inline=False)
        embed.add_field(name="🗺️ Last 10 Maps",
                        value=f"{self.history.getFormattedLast10Maps()}", inline=False)
        embed.add_field(name="⌚ Last refresh",
                        value=f"<t:{self.history.getLastUpdate()}:R>")
        embed.set_footer(text="by immervoll")
        return embed
