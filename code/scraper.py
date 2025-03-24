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
        
        options.add_argument("--headless")
        
        options.add_argument("--incognito")
        
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        
        options.add_argument("--start-maximized")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        
        options.add_argument("--disable-application-cache")
        options.add_argument("--disable-cache")
        options.add_argument("disable-http-cache")

        navegador = webdriver.Chrome(options=options)

        return navegador
    

    def verificar_cidades_microrregiao(self):
        '''
            ["python", "adicionar_concorrentes.py", "'SAO-JOAO-DE-MERETI-RJ'"]

            Devolve um dataframe com as cidades da microrregião baseado no código da cidade.
        '''

        codcidade = self.codcidade

        df = pd.read_csv("Files/dados.csv")
        
        microregiao = df[df["Código Município Completo"] == codcidade].iloc[0]["Nome_Microrregião"]

        df_cidades = df[df["Nome_Microrregião"] == microregiao][["Nome_UF", "Nome_Microrregião", "Código Município Completo", "Nome_Município"]]
        cidades_reorganizado = df_cidades[["Nome_Município", "Código Município Completo", "Nome_UF", "Nome_Microrregião"]]
        cidades_reorganizado["Código Município Completo"] = cidades_reorganizado["Código Município Completo"].astype(str).astype(str).replace(",", "", regex=True)
        cidades_reorganizado["Nome_Município"] = cidades_reorganizado["Nome_Município"] + " - " + cidades_reorganizado["Nome_UF"]
        
        return cidades_reorganizado