import random
import tkinter as tk
import customtkinter
from services.MapServices import mapServices


mapSize = 624
cellSize = 26
cellBorderSize = 1
groundRatio = .5
maxGround = int((mapSize // cellSize) * (mapSize // cellSize) * groundRatio)
borderColor = "black"
voidColor = "black"
groundColor = "gray"


def setMap(map_frame):
    map_frame.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nw")


class MapFrameController:
    def __init__(self):
        pass

    def createStartPoint(self):
        startPoint = random.randint(0, mapSize // cellSize - 1)
        return startPoint

    def createAreaMap(self):
        area_map = []
        current_point = (self.createStartPoint(), self.createStartPoint())
        area_map.append({'coords': f'{current_point[0]},{current_point[1]}', 'coordType': "inner", 'cellColor': groundColor})
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while len([item for item in area_map if item['coordType'] == "inner"]) < maxGround:
            dx, dy = random.choice(directions)
            x, y = current_point
            x += dx
            y += dy

            if 0 <= x < mapSize // cellSize and 0 <= y < mapSize // cellSize:
                current_point = (x, y)
                coord_key = f'{current_point[0]},{current_point[1]}'
                if not any(item['coords'] == coord_key for item in area_map):
                    area_map.append({'coords': coord_key, 'coordType': "inner", 'cellColor': groundColor})

        return area_map

    def drawMap(self, canvas, area_map, rectangles):
        area_map_dict = {item['coords']: (item['coordType'], item['cellColor']) for item in area_map}
        for i in range(mapSize // cellSize):
            for j in range(mapSize // cellSize):
                x1 = i * (cellSize + cellBorderSize)
                y1 = j * (cellSize + cellBorderSize)
                x2 = x1 + cellSize
                y2 = y1 + cellSize

                is_border = i == 0 or j == 0 or i == (mapSize // cellSize - 1) or j == (mapSize // cellSize - 1)
                coord_key = f'{i},{j}'

                if is_border:
                    color = voidColor
                elif coord_key in area_map_dict:
                    area_type, color = area_map_dict[coord_key]
                else:
                    area_type, color = "outer", voidColor

                rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=borderColor)
                rectangles[coord_key] = rect

mapFrameController = MapFrameController()

class MapFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rectangles = {}

        self.map_frame_controller = MapFrameController()

        canvas_width = (mapSize // cellSize) * (cellSize + cellBorderSize) - 3
        canvas_height = (mapSize // cellSize) * (cellSize + cellBorderSize) - 3

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.area_map = self.map_frame_controller.createAreaMap()
        self.map_frame_controller.drawMap(self.canvas, self.area_map, self.rectangles)

    def getMapData(self):
        return {
            "area_map": self.area_map
        }

    def loadMapData(self, map_data):
        self.area_map = map_data["area_map"]
        self.map_frame_controller.drawMap(self.canvas, self.area_map, self.rectangles)
        return self
    
    def updateCell(self, cell):
        coords = cell["coords"]
        cellColor = cell["cellColor"]
        area_map = mapServices.getMap()
        found = False
        for item in area_map["area_map"]:
            if item['coords'] == coords:
                item['cellColor'] = cellColor
                # TODO add more properties here if needed
                found = True
                break
        if not found:
            pass
        self.canvas.itemconfigure(self.rectangles[coords], fill=cellColor)



class MapController:
    def __init__(self):
        pass

    def checkMapExists(self, master):
        map = mapServices.loadMap()
        if (map == None):
            self.map_frame = self.createNewMap(master)
            return self.map_frame
        else:
            self.map_frame = MapFrame(master)
            map = mapServices.getMap()
            setMap(self.map_frame.loadMapData(map))
            return self.map_frame

    def createNewMap(self, master):
        self.map_frame = MapFrame(master)
        mapServices.saveMap(self.map_frame)
        map = mapServices.getMap()
        setMap(self.map_frame.loadMapData(map))
        return self.map_frame


mapController = MapController()