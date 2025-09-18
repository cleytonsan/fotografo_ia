import os
import cv2
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import google.generativeai as genai

# Configuração da IA
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CameraApp(App):
    def build(self):
        self.img = Image()
        self.label = Label(text="Iniciando câmera...", font_size="18sp")
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.img)
        layout.add_widget(self.label)

        # Abre a câmera
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS
        return layout

    def analisar_iluminacao(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brilho = gray.mean()
        if brilho < 80:
            return "⚠️ Muito escuro! Tente se aproximar de uma luz."
        elif brilho > 200:
            return "⚠️ Muito claro! Ajuste a posição ou reduza a luz."
        else:
            return "✅ Iluminação boa!"

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Analisa iluminação
            dica = self.analisar_iluminacao(frame)
            self.label.text = dica

            # Mostra imagem no app
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    CameraApp().run()
