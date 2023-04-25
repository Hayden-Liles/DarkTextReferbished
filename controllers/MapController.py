import random
import tkinter as tk
import customtkinter
from services.MapServices import mapServices


mapSize = 624
cellSize = 26
cellBorderSize = 1
groundRatio = .6
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
        return random.randint(0, mapSize // cellSize - 1)

    def createAreaMap(self):
        area_map = {}

        current_point = (self.createStartPoint(), self.createStartPoint())
        area_map[current_point] = ("inner", groundColor)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while len([coord for coord, (area_type, _) in area_map.items() if area_type == "inner"]) < maxGround:
            dx, dy = random.choice(directions)
            x, y = current_point
            x += dx
            y += dy

            if 0 <= x < mapSize // cellSize and 0 <= y < mapSize // cellSize:
                current_point = (x, y)
                area_map[current_point] = ("inner", groundColor)
        
        map_data = []

        for coordinates, (coord_type, cell_color) in area_map.items():
            coord_dict = {
                'coordinates': f'{coordinates[0]},{coordinates[1]}',
                'coordType': coord_type,
                'cellColor': cell_color,
            }
            map_data.append(coord_dict)

        result = map_data
        return result

    def drawMap(self, canvas, area_map):
        for i in range(mapSize // cellSize):
            for j in range(mapSize // cellSize):
                x1 = i * (cellSize + cellBorderSize)
                y1 = j * (cellSize + cellBorderSize)
                x2 = x1 + cellSize
                y2 = y1 + cellSize

                is_border = i == 0 or j == 0 or i == (
                    mapSize // cellSize - 1) or j == (mapSize // cellSize - 1)

                if is_border:
                    color = voidColor
                elif (i, j) in area_map:
                    area_type, color = area_map[(i, j)]
                else:
                    area_type, color = "outer", voidColor

                canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=borderColor)


mapFrameController = MapFrameController()


class MapFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_frame_controller = MapFrameController()

        canvas_width = (mapSize // cellSize) * (cellSize + cellBorderSize) - 3
        canvas_height = (mapSize // cellSize) * (cellSize + cellBorderSize) - 3

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.area_map = self.map_frame_controller.createAreaMap()
        self.map_frame_controller.drawMap(self.canvas, self.area_map)

    def getMapData(self):
        return {
            "area_map": self.area_map
        }

    def loadMapData(self, map_data):
        self.area_map = {}
        for item in map_data["area_map"]:
            coords = tuple(map(int, item['coordinates'].split(',')))
            coord_type = item['coordType']
            cell_color = item['cellColor']
            self.area_map[coords] = (coord_type, cell_color)

        self.map_frame_controller.drawMap(self.canvas, self.area_map)
        return self


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