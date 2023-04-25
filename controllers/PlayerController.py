from services.PlayerServices import playerServices
from services.MapServices import mapServices

class PlayerController:
    def __init__(self):
        pass
    
    def checkPlayer(self, master):
        playerServices.checkPlayer()
        self.drawPlayer(master)
    
    def drawPlayer(self, master):
        playerDetails = playerServices.getPlayerDetails()
        master.updateCell(playerDetails)
        mapServices.saveMap(master)

    # key is the keypressed
    def movePlayer(self, key, master):
        playerDetails = playerServices.getPlayerDetails()
        playerLocation = playerDetails["coords"].split(',')
        x, y = playerLocation
        x = int(x)
        y = int(y)
        
        match key:
            case "Up":
                y -= 1
            case "Down":
                y += 1
            case "Left":
                x -= 1
            case "Right":
                x += 1

        newLocation = f'{x},{y}'
        print(type(newLocation))

playerController = PlayerController()
