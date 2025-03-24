# Scraper-Ifood

Este projeto de estudo utiliza Python, Selenium e BeautifulSoup (bs4) para praticar conceitos de Web Scraping. O código analisa quais cidades de uma determinada microrregião possuem empreendimentos farmacêuticos e/ou supermercados cadastrados no aplicativo iFood.

# 📌 Funcionalidades

Coleta informações sobre farmácias e supermercados em diferentes cidades.

Gera um arquivo .xlsx com os resultados na pasta Cidades.

Utiliza técnicas para minimizar a detecção de automação pelo iFood.

# 🚀 Como Utilizar

Instale as dependências:

pip install -r requirements.txt

Execute o script main.py:

python main.py <cod_cidade> [nome_cidade]

Se passar apenas <cod_cidade>, o script buscará os dados da cidade correspondente.

Se passar <cod_cidade> nome_cidade, o arquivo gerado terá o nome especificado.

# ⚠️ Notas Importantes

O iFood possui uma forte detecção de bots e automações. Para evitar bloqueios, o código implementa pausas aleatórias entre as requisições.

Caso encontre dificuldades, tente alterar os tempos de espera e revisar os cabeçalhos de requisição do Selenium.


# 🛠 Tecnologias Utilizadas

Python

Selenium

BeautifulSoup (bs4)

Pandas (para manipulação de dados e geração de arquivos .xlsx)

# 🎥 Link de demonstração de execução:

https://photos.app.goo.gl/VJ5p5cgPwKyscveMA