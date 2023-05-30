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


bots = {"Pata": PataChatBot.instance(), "Yvon": YvonChatBot.instance()}

def get_chat_bot(name):
    return bots[name]

def set_session_state_variables():
    if 'prender_ia' not in st.session_state:
        st.session_state['prender_ia'] = False
    if 'ia_seleccionada' not in st.session_state:
        st.session_state['ia_seleccionada'] = "Seleccione una IA"

def get_ia_selection(opciones_ia):
    return st.sidebar.selectbox('Selecciona una IA:', opciones_ia, 
                                index=opciones_ia.index(st.session_state['ia_seleccionada']),
                                key='seleccion_ia_key12345')

def initialize_chat_bot(seleccion_ia, chat_bot, info_message):
    if not st.session_state['prender_ia']:
        info_message.info("Encendiendo la IA... por favor espere.")
        st.session_state['prender_ia'] = True
    chat_bot.prender_ia()
    st.session_state['prender_ia'] = False

def send_receive_text(chat_bot):
    texto_usuario = st.text_input('Introduce tu texto aquí:', key='2')
    if texto_usuario:
        chat_bot.envia_texto(texto_usuario)
        chat_bot.recibe_texto()

def shutdown_chat_bot(seleccion_ia, chat_bot, mensaje_estado):
    if st.sidebar.button('Apagar IA') and chat_bot.driver is not None:
        chat_bot.apagar_ia()
        st.session_state['ia_seleccionada'] = "Seleccione una IA"
        mensaje_estado.info(f"Estado de la IA: {chat_bot.estado}")

def main():
    st.title("Aplicación de Chat")

    set_session_state_variables()
    
    opciones_ia = ["Seleccione una IA", "Pata: IA de Patagonia", "Yvon"]
    seleccion_ia = get_ia_selection(opciones_ia)

    info_message = st.empty()
    mensaje_estado = st.sidebar.empty()

    if seleccion_ia and seleccion_ia != "Seleccione una IA":
        name = seleccion_ia.split(':')[0]
        st.session_state['ia_seleccionada'] = seleccion_ia
        chat_bot = get_chat_bot(name)

        if chat_bot.driver is None:
            initialize_chat_bot(seleccion_ia, chat_bot, info_message)

        info_message.empty()
        mensaje_estado.info(f"Estado de la IA: {chat_bot.estado}")
        
        send_receive_text(chat_bot)

        shutdown_chat_bot(seleccion_ia, chat_bot, mensaje_estado)
    
    else:
        st.session_state['ia_seleccionada'] = "Seleccione una IA"
        encendida = [name for name, bot in bots.items() if bot.driver is not None]
        mensaje_estado.info(f"La IA {', '.join(encendida)} está encendida" if encendida else "Todas las IA están apagadas")

if __name__ == '__main__':
    main()
