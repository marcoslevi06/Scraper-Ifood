import pandas as pd
from time import sleep
from code.scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random


class Microrregiao(Scraper):
    '''
    '''
    def __init__(self, nome_cidade : str, uf_estado : str = None, codcidade : str = None):
        self.nome_cidade = nome_cidade
        self.codcidade = codcidade
        self.uf_estado = uf_estado # Atualmente não está sendo utilizado, mas pode ser útil para futuras implementações.
        self.BASE_URL = "https://www.ifood.com.br/inicio"
        self.ponto_de_referencia = "Praça"
        self.bairro = "Centro"


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

    
    def verifica_cidades_com_ifood(self,  dataframe : pd.DataFrame, 
                                   nome_da_cidade_da_microrregiao : str = None,
                                #    codcidade : str = None
                                   ):
        '''
            Método para verificar as cidades com farmácias e mercados 
            atuantes no iFood.
        '''

        if nome_da_cidade_da_microrregiao is not None:
            self.nome_cidade = nome_da_cidade_da_microrregiao

        time_a = random.uniform(1.5, 2.5)
        time_b = random.uniform(1.5, 2.5)

        farmacia = False
        mercado = False

        navegador = self.create_browser()
        navegador.get(self.BASE_URL)
        sleep(2)

        # Clicando no botão de busca por endereço.
        button = navegador.find_element(By.CSS_SELECTOR, "button.address-search-input__button[aria-label='Buscar endereço e número']")
        button.click()
        # print("Clicou no botão de busca.")
        sleep(random.uniform(time_a, time_b))

        
        # iframes = navegador.find_elements(By.TAG_NAME, "iframe")
        # print(f"Total de iframes: {len(iframes)}")
        input_selector = "body > div:nth-child(13) > div > div > div > div > div > div:nth-child(2) > div > div.address-search-step > div.address-search-input.address-search-input--sticky > input"
        encontrou = False
        # for indice, iframe in enumerate(iframes):
        #     try:
        #         navegador.switch_to.frame(iframe)
        #         # print(f"Trocou para o iframe {indice}")
        #         input_field = navegador.find_element(By.CSS_SELECTOR, input_selector)
        #         print("Encontrou o campo dentro do iframe!")
        #         encontrou = True
        #         break
        #     except:
        #         navegador.switch_to.default_content()  # Volta para o contexto principal
        #         continue

        if not encontrou:
            navegador.switch_to.default_content()  
            input_field = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, input_selector))
            )
            # print("Encontrou o campo de busca no contexto principal!")

        # O nome da cidade precisa estar como: Nome_Cidade - UF, para evitar erros na sugestão do IFOOD.
        # self.nome_cidade = self.nome_cidade + " - " + self.uf_estado
        input_field.send_keys(self.nome_cidade)

        wait = WebDriverWait(navegador, 10)

        # Clicando na primeira opção de cidade sugerida.
        primeiro_botao = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".address-search-list li:first-child button"))
        )
        primeiro_botao.click()
        sleep(random.uniform(time_a, time_b))

        # Clicandona confirmação de local.
        botao_confirmar_localizacao = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn--default.btn--size-m.address-maps__submit"))
        )
        botao_confirmar_localizacao.click()

        # Verificando se o bairro foi exibido. Não necessariamente ele é pedido em todas as cidades.
        try:
            wait_bairro = WebDriverWait(navegador, 3)
            campo_input_bairro = wait_bairro.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-input__field[name='district']"))
            )
            campo_input_bairro.send_keys(self.bairro)
        except:
            print("Bairro não foi solicitado.")
            pass

        # Passando um ponto de localização obrigatório.
        campo_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".form-input__field[name='reference']"))
        )
        sleep(random.uniform(time_a, time_b))

        campo_input.send_keys(self.ponto_de_referencia)
        campo_input.send_keys(Keys.RETURN)
        # sleep(100)

        sleep(random.uniform(time_a, time_b))

        soup = BeautifulSoup(navegador.page_source, "html.parser")
        bloco_categorias = soup.find("div", class_="desktop-category-selector__horizontal")
        lista_categorias = bloco_categorias.find_all("li", class_="desktop-category-links__item")

        for categoria in lista_categorias:
            categoria = categoria.text.strip().upper()

            if categoria == "MERCADOS":
                mercado = True

            if categoria == "FARMÁCIAS":
                farmacia = True

        # print("Mercado: ", mercado)
        # print("Farmácia: ", farmacia)

        existe_mercados = False
        existe_farmacias = False

        if mercado:
            navegador.get("https://www.ifood.com.br/mercados"); sleep(random.uniform(time_a, time_b))
            soup = BeautifulSoup(navegador.page_source, "html.parser")
            lista_de_mercados = soup.find_all("div", class_="merchant-list-v2__item-wrapper")
            if len(lista_de_mercados) > 0:
                existe_mercados = True

        if farmacia:
            navegador.get("https://www.ifood.com.br/farmacia"); sleep(random.uniform(time_a, time_b))
            soup = BeautifulSoup(navegador.page_source, "html.parser")
            lista_de_farmacias = soup.find_all("div", class_="merchant-list-v2__item-wrapper")
            if len(lista_de_farmacias) > 0:
                existe_farmacias = True

        # print("Existem mercados: ", existe_mercados)
        # print("Existem farmácias: ", existe_farmacias)
        sleep(2)
        navegador.quit()

        existe_farmacias = "✅" if existe_farmacias else "❌"
        existe_mercados = "✅" if existe_mercados else "❌"

        dataframe.loc[dataframe["Nome_Município"] == self.nome_cidade, "Mercados"] = existe_mercados
        dataframe.loc[dataframe["Nome_Município"] == self.nome_cidade, "Farmácias"] = existe_farmacias

        print(f"{self.nome_cidade.upper()}")
        print(f"IFOOD Mercados: {existe_mercados}")
        print(f"IFOOD Farmácias: {existe_farmacias}")
        print("-" * 100)
        return dataframe