import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Scraper():

    def create_browser(self):
        '''
            Cria uma instância do navegador.
        '''
        options = Options()
        
        # Ativar o modo incognito (sem histórico, cache, cookies)
        options.add_argument("--incognito")
        
        # Definir User-Agent (para evitar detecção de automação)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        
        # Maximizar a janela
        options.add_argument("--start-maximized")
        
        # Desabilitar opções que podem afetar o comportamento do navegador em servidores (como no Docker)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        
        # Para não usar cache de memória e cookies antigos
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-cache")
        options.add_argument("disable-http-cache")
        
        # Usar um perfil de navegador limpo (sem cookies ou cache)
        options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Definir o diretório de dados de usuário temporário
        
        navegador = webdriver.Chrome(options=options)

        return navegador