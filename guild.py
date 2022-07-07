from embed import Embed
from history import History
import discord


class Guild(discord.Guild):
    """Guild class"""
    guild: discord.Guild
    embeds: list[Embed]
    histories: list[History]

    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self.embeds = []
        self.histories = []

    def addEmbedToChannel(self, channel: discord.TextChannel):
        embed = Embed(channel, self.histories[0])
        return self.addEmbed(embed)
        

    def addEmbed(self, embed: Embed, historyid = 0):
        assert historyid < len(self.histories), "historyid out of range"
        self.embeds.append((embed, historyid))
        return embed

    def removeEmbed(self, embed: Embed):
        self.embeds.remove(embed)
        return True
        
    def removeEmbedByMessageID(self, messageid: int):
        for embed in self.embeds:
            if embed.message.id == messageid:
                self.removeEmbed(embed)
                return True
        return False

    def addHistory(self, history: History):
        self.histories.append(history)
        return self.histories.index(history)

    def removeHistory(self, history: History):
        self.histories.remove(history)
        return True
    
    def hasHistory(self, ip: str, port: int):
        for history in self.histories:
            if history.ip == ip and history.port == port:
                return True
    
    def removeHistoryByID(self, historyid: int):
        self.histories.pop(historyid)
        return True

    def updateEmbeds(self):
        for embed in self.embeds:
            embed.updateEmbed()
        