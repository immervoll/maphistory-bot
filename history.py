import pickle
import os
import time
import a2s


class History(object):
    """History class represents the history of maps played on a server."""
    server_name: str
    current_map: str
    last_map: str
    last_maps: list
    last_update: int

    def __init__(self):
        if os.path.exists("./history.pickle"):
            with open("./history.pickle", "rb") as historyPickleFile:
                self.last_maps = pickle.load(historyPickleFile)
                self.current_map = self.last_maps[-1][0]
                self.last_map = None
                self.last_update = self.last_maps[-1][2]
        else:
            self.last_maps = []
            self.current_map = None
            self.last_update = int(time.time())

    def store(self):

        with open("./history.pickle", "wb") as historyPickleFile:
            pickle.dump(self.last_maps, historyPickleFile)

    def writeUpdate(self, map_name, players):
        assert map_name != self.current_map
        self.last_map = self.current_map
        self.current_map = map_name
        ctime = int(time.time())
        self.last_maps.append((map_name,players,  ctime))
        self.store()

    def query(self, serveraddress: tuple):
        query = a2s.info(serveraddress)
        if query.map_name != self.current_map:
            self.writeUpdate(query.map_name, query.player_count)
            
        if query.server_name != None:
            self.server_name = query.server_name
            
        self.last_update = int(time.time())
        return self.getCurrentMap()

    def getCurrentMap(self):
        return self.current_map

    def getLastMap(self):
        return self.last_map

    def getLast10Maps(self):
        return self.last_maps

    def getFormattedCurrentMap(self):
        return f"`{self.current_map}` with `{self.last_maps[-1][1]}` players - since: <t:{self.last_maps[-1][2]}:R>"

    def getFormattedLastMap(self):
        try:
            return f"`{self.last_map}` with `{self.last_maps[-2][1]}` players - since: <t:{self.last_maps[-2][2]}:R>"
        except:
            return "`No previous map`"
        
    def getFormattedLast10Maps(self):
        formattedText = ""
        for map_name, players, timestamp in reversed(self.last_maps[-10:]):
            formattedText += ((f"`{map_name}` with `{players}` players - since: <t:{timestamp}:R>\n"))
        return formattedText

    def getLastUpdate(self):
        return self.last_update

    def getServerName(self):
        return self.server_name