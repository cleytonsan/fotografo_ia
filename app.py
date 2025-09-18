import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Fotógrafo Inteligente", page_icon="📸")

st.title("📸 Fotógrafo Inteligente em Tempo Real")
st.write("Seu assistente fotográfico que analisa a iluminação e dá dicas instantâneas.")

# Usar câmera do celular
img_file_buffer = st.camera_input("Tire uma foto")

if img_file_buffer is not None:
    # Carregar imagem
    image = Image.open(img_file_buffer)
    img_array = np.array(image)

    # Converter para escala de cinza
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    brilho = gray.mean()

    # Análise de iluminação
    if brilho < 80:
        st.error("⚠️ Muito escuro! Tente se aproximar de uma fonte de luz.")
    elif brilho > 200:
        st.warning("⚠️ Muito claro! Ajuste a posição ou reduza a luz.")
    else:
        st.success("✅ Iluminação boa! Perfeito para fotografar.")

    # Mostrar imagem capturada
    st.image(image, caption="Prévia da foto", use_column_width=True)
