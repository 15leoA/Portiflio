from kivy.app import App
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Line
from plyer import gps
import requests

API_KEY = "SUA_CHAVE_API"  # OpenWeatherMap
UPDATE_INTERVAL = 5  # segundos para atualizar clima
MIN_TIME_GPS = 1000  # ms
MIN_DISTANCE_GPS = 0

class MapApp(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # MapView
        self.mapview = MapView(zoom=15, lat=-23.5505, lon=-46.6333)
        self.add_widget(self.mapview)

        # Label clima
        self.clima_label = Label(text="Carregando clima...", size_hint=(None, None),
                                 pos=(20, 20))
        self.add_widget(self.clima_label)

        # Lista de pontos do trajeto
        self.pontos = []
        self.marker = None

        # GPS real
        try:
            gps.configure(on_location=self.atualizar_posicao)
            gps.start(minTime=MIN_TIME_GPS, minDistance=MIN_DISTANCE_GPS)
        except NotImplementedError:
            self.clima_label.text = "GPS não suportado neste dispositivo."

        # Atualiza clima periodicamente
        Clock.schedule_interval(self.atualizar_clima, UPDATE_INTERVAL)

    def atualizar_posicao(self, **kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        # Atualiza mapa
        self.mapview.center_on(lat, lon)

        # Atualiza ponteiro verde
        if not self.marker:
            self.marker = MapMarker(lat=lat, lon=lon, source="green_marker.png")
            self.mapview.add_widget(self.marker)
        else:
            self.marker.lat = lat
            self.marker.lon = lon

        # Adiciona ponto à linha
        self.pontos.append((lat, lon))
        self.desenhar_trajeto()

    def desenhar_trajeto(self):
        # Desenhar linha verde pontilhada
        self.mapview.canvas.after.clear()
        if len(self.pontos) > 1:
            with self.mapview.canvas.after:
                Color(0, 1, 0)
                # MapView não converte direto lat/lon -> tela
                # Então usamos a função interna get_window_xy_from
                Line(points=[coord for ponto in self.pontos
                             for coord in self.mapview.get_window_xy_from(*ponto)],
                     width=2, dash_offset=3)

    def atualizar_clima(self, dt):
        if not self.pontos:
            return
        lat, lon = self.pontos[-1]
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
            data = requests.get(url).json()
            temp = data['main']['temp']
            weather = data['weather'][0]['description']
            uv_index = data.get('uvi', 0)
            alerta = self.sugerir_alerta(temp, uv_index)
            self.clima_label.text = f"Temp: {temp}°C | {weather}\n{alerta}"
        except:
            self.clima_label.text = "Erro ao consultar clima."

    def sugerir_alerta(self, temp, uv):
        if uv > 6:
            return "⚠ UV alto! Evite exposição."
        elif temp > 35:
            return "⚠ Calor extremo! Hidrate-se."
        elif temp < 5:
            return "⚠ Frio intenso! Use agasalho."
        else:
            return "Clima ok para pedalar."

class TrajetoApp(App):
    def build(self):
        return MapApp()

if __name__ == "__main__":
    TrajetoApp().run()
