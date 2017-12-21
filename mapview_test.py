from kivy.garden.mapview import MapView
from kivy.app import App

class MapViewApp(App):
    def build(self):
        # mapview = MapView(zoom=11, lat=50.6394, lon=3.057)
        mapview = MapView(zoom=11, lat=39.92, lon=116.46)
        return mapview

MapViewApp().run()