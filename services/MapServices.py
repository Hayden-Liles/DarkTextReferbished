from AppState import appState


class MapServices:
    def __init__(self):
        pass

    def loadMap(self):
        appState.load_state('save.json')
        map = appState.get_data('curMap')
        return map

    def saveMap(self, mapData):
        map_data_to_save = mapData.getMapData()
        # Creating border
        for item in map_data_to_save["area_map"]:
            coords = tuple(map(int, item['coords'].split(',')))

            xCord, yCord = coords
            if xCord == 23 or xCord == 0 or yCord == 23 or yCord == 0:
                item['coordType'] = 'outer'
                item['cellColor'] = 'black'
        
        appState.set_data('curMap', map_data_to_save)
        appState.save_state('save.json')

    def getMap(self):
        map = appState.get_data('curMap')
        return map
    
    def getInnerArea(self):
        map = self.getMap()["area_map"]
        inner = []
        for x in map:
            if x['coordType'] == 'inner':
                inner.append(x)
        return inner


mapServices = MapServices()