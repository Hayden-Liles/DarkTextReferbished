from AppState import appState
from services.MapServices import mapServices
import random

class PlayerServices:
    def __init__(self):
        pass

    def checkPlayer(self):
        player = appState.get_data('player')
        if player == None:
            player = self.createPlayer()

    def createPlayer(self):
        inner = mapServices.getInnerArea()
        startLocationData = self.chooseStartLocation(inner)
        player = {
            "name": "tempName",
            "coords": f"{startLocationData['coords']}",
            "cellColor": "green"
        }
        appState.set_data('player', player)
        # FIXME uncomment out when done
        # appState.save_state('save.json')

    def chooseStartLocation(self, innerMap):
        location = random.choice(innerMap)
        return location
    
    def getPlayerDetails(self):
        player = appState.get_data('player')
        return player


playerServices = PlayerServices()