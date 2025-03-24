from code.cidades_microrregiao import Microrregiao
from time import sleep
import random

if __name__ == "__main__":
    '''
        ENTRADA:
            - Código da cidade
            - Nome da cidade
            - UF
        SAÍDA:
            - Planilha com as cidades da microrregião com farmácias e mercados

        O projeto apenas necessida que você informe o codcidade_IBGE, nome da cidade e UF,
        desse modo, o projeto irá verificar todas as cidades da microrregião e verificar se
        possuem farmácias e mercados listados no Ifood.

        Ao final, será gerado uma planilha com as cidades da microrregião irformando
        quais cidades possuem farmácias e mercados.
    '''

    codcidade_verificada = 2304400
    cidade_verificada = "Fortaleza"
    
    cidades_microrregiao = Microrregiao(
                            nome_cidade=cidade_verificada, 
                            codcidade=codcidade_verificada
                        )
    
    print("Iniciando o projeto de verificação de cidades de uma microrregião.")

    df = cidades_microrregiao.verificar_cidades_microrregiao()
    dicionario_cidades = dict(zip(df["Nome_Município"], df["Código Município Completo"]))
    df.to_excel(f"Cidades/{cidade_verificada}_{codcidade_verificada}.xlsx", index=False)

    for cidade, codcidade in dicionario_cidades.items():
        time_sleep = random.randint(2, 3)
        sleep(time_sleep)
        try:
            df = cidades_microrregiao.verifica_cidades_com_ifood(dataframe=df,nome_da_cidade_da_microrregiao=cidade)

        except Exception as erro:
            print(f"Erro ao verificar a cidade {cidade}.")
            print(f"{erro}")    
            continue

    df = df[["Nome_UF", "Nome_Microrregião", "Nome_Município", "Código Município Completo", "Mercados", "Farmácias"]]
    df.to_excel(f"Cidades/{cidade_verificada}_{codcidade_verificada}.xlsx", index=False)


    