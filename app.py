import streamlit as st
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import sys
import textwrap
#from funciones import ChatBot

from funciones import PataChatBot, YvonChatBot


bots = {
    "Pata": PataChatBot.instance(),
    "Yvon": YvonChatBot.instance(),
}

def get_chat_bot(name):
    return bots[name]

def main():
    st.title("Aplicación de Chat")

    if 'prender_ia' not in st.session_state:
        st.session_state['prender_ia'] = False

    if 'ia_seleccionada' not in st.session_state:
        st.session_state['ia_seleccionada'] = "Seleccione una IA"

    opciones_ia = ["Seleccione una IA", "Pata: IA de Patagonia", "Yvon"]
    seleccion_ia = st.selectbox('Selecciona una IA:', opciones_ia, index=opciones_ia.index(st.session_state['ia_seleccionada']))

    info_message = st.empty()
    mensaje_estado = st.empty()

    if seleccion_ia and seleccion_ia != "Seleccione una IA":
        name = seleccion_ia.split(':')[0]
        st.session_state['ia_seleccionada'] = seleccion_ia
        chat_bot = get_chat_bot(name)

        if chat_bot.driver is None:
            if not st.session_state['prender_ia']:
                info_message.info("Encendiendo la IA... por favor espere.")
                st.session_state['prender_ia'] = True
            chat_bot.prender_ia()
            info_message.empty()
            st.session_state['prender_ia'] = False
            main()

        mensaje_estado.info(f"Estado de la IA: {chat_bot.estado}")

        texto_usuario = st.text_input('Introduce tu texto aquí:', key='texto_usuario_key')

        if texto_usuario:
            chat_bot.envia_texto(texto_usuario)
            chat_bot.recibe_texto()

        if st.button('Apagar IA'):
            if seleccion_ia == "Pata: IA de Patagonia" and chat_bot.driver is not None:
                chat_bot.apagar_ia()
                st.session_state['ia_seleccionada'] = "Seleccione una IA"

            if seleccion_ia == "Yvon" and chat_bot.driver is not None:
                chat_bot.apagar_ia()
                st.session_state['ia_seleccionada'] = "Seleccione una IA"

            mensaje_estado.info(f"Estado de la IA: {chat_bot.estado}")
    
    else:
        st.session_state['ia_seleccionada'] = "Seleccione una IA"
        # Verificar si alguna IA está encendida
        encendida = [name for name, bot in bots.items() if bot.driver is not None]
        if encendida:
            mensaje_estado.info(f"La IA {', '.join(encendida)} está encendida")
        else:
            # Si no se ha seleccionado ninguna IA y todas están apagadas
            mensaje_estado.info("Todas las IA están apagadas")

if __name__ == '__main__':
    main()