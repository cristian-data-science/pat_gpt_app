
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
from typing import Optional


class Singleton:
    _instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance


class BaseChatBot(Singleton):

    def __init__(self):
        self.driver = None
        self.estado = "Apagada"

    def prender_ia(self, url):
        if self.driver is None:
            options = webdriver.ChromeOptions()
            #user_data_dir = r'C:\Users\Cristian Gutierrez\AppData\Local\Google\Chrome\User Data\Profile 1'          
            #options.add_argument('--user-data-dir=' + user_data_dir)
            options.add_argument("--start-maximized")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--log-level=3")
            self.driver = uc.Chrome(enable_cdp_events=True, headless=False, version_main=112,  options=options)
            self.driver.get(url)
            sleep(3)
        self.estado = "Encendida"

    def apagar_ia(self):
        if self.driver is not None:
            self.driver.quit()
            self.driver = None
            self.estado = "Apagada"

    def envia_texto(self, texto_usuario):
        if self.driver is None:  # Cambiado de 'driver' a 'self.driver'
            raise Exception("No se ha iniciado la IA")

        input_text = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[3]/div[2]/div[2]/div/div[1]/div/div/div')  # Cambiado de 'driver' a 'self.driver'
        input_text.click()
        segment_size = 50
        segments = [texto_usuario[i:i+segment_size] for i in range(0, len(texto_usuario), segment_size)]
        for segment in segments:
            input_text.send_keys(segment)
            sleep(0.5)
        input_text.send_keys(Keys.ENTER)

    def recibe_texto(self):
        if self.driver is None:  # Cambiado de 'driver' a 'self.driver'
            raise Exception("No se ha iniciado la IA")

        respuesta = ''
        output = st.empty()
        palabra_parcial = ''
        texto_cache = ''

        while True:
            sleep(3)
            try:
                elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[3]/div[1]/div[4]/div/div[2]/div[1]'))
                )
                nueva_respuesta = ' '.join([element.text for element in elements])

                if nueva_respuesta != respuesta:
                    dif_respuesta = nueva_respuesta[len(respuesta.rstrip('.')):]

                    if dif_respuesta == "":
                        break

                    for letra in dif_respuesta:
                        if letra == ' ':
                            texto_cache += palabra_parcial + ' '
                            output.text(textwrap.fill(texto_cache, 80))
                            palabra_parcial = ''
                            sleep(0.1)
                        else:
                            palabra_parcial += letra
                            respuesta = nueva_respuesta
                else:
                    sleep(2)
                    elements = self.driver.find_elements(By.XPATH, '/html/body/div[1]/main/div[2]/div[3]/div[1]/div[4]/div/div[2]/div[1]')
                    nueva_respuesta = ' '.join([element.text for element in elements])

                    if nueva_respuesta == respuesta:
                        break
                    else:
                        dif_respuesta = nueva_respuesta[len(respuesta):]

                        if dif_respuesta == "":
                            break

                        for letra in dif_respuesta:
                            if letra == ' ':
                                texto_cache += palabra_parcial + ' '
                                output.text(textwrap.fill(texto_cache, 80))
                                palabra_parcial = ''
                                sleep(0.1)
                            else:
                                palabra_parcial += letra
                        respuesta = nueva_respuesta
            except:
                pass

        if palabra_parcial:
            texto_cache += palabra_parcial
        output.text(textwrap.fill(texto_cache, 80))


class PataChatBot(BaseChatBot):

    def prender_ia(self):
        super().prender_ia('https://chat.forefront.ai')  # Ejemplo de URL para la IA de Pata

    def apagar_ia(self):
        super().apagar_ia()


class YvonChatBot(BaseChatBot):

    def prender_ia(self):
        super().prender_ia('https://chat.forefront.ai/') 

    def apagar_ia(self):
        super().apagar_ia()



        #self.driver.close() 
            

        