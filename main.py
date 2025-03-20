from code.cidades_microrregiao import Microrregiao

if __name__ == "__main__":

    codcidade_verificada = 2304103
    cidade_verificada = "Crateús"
    uf = "CE"
    
    cidades_microrregiao = Microrregiao(
                            nome_cidade=cidade_verificada, 
                            uf_estado=uf, 
                            codcidade=codcidade_verificada
                        )
    
    print("Iniciando o projeto de verificação de cidades de uma microrregião.")

    df = cidades_microrregiao.verificar_cidades_microrregiao()
    dicionario_cidades = dict(zip(df["Nome_Município"], df["Código Município Completo"]))
    df.to_excel(f"{codcidade_verificada}_{cidade_verificada}.xlsx", index=False)

    dicionario_cidades = {
        "Crateús - Ceará": 2304103,
        "Novo Oriente - Ceará": 2309409,
    }
    for cidade, codcidade in dicionario_cidades.items():
        temp_df = cidades_microrregiao.verifica_cidades_com_ifood(dataframe=df,
                                                                  nome_da_cidade_da_microrregiao=cidade,
                                                                #   codcidade=codcidade
                                                        )
        df = temp_df


    df = df[["Nome_UF", "Nome_Microrregião", "Nome_Município", "Código Município Completo", "Mercados", "Farmácias"]]
    df.to_excel(f"{codcidade_verificada}_{cidade_verificada}.xlsx", index=False)

    