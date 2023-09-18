# Importação das bibliotecas necessárias
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# URL dos Exoplanetas da NASA
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Configuração do Webdriver do Chrome
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

# Pausa para aguardar o carregamento da página
time.sleep(10)

# Lista para armazenar os dados coletados
new_planets_data = []

# Função para coletar dados detalhados a partir de um hyperlink
def scrape_more_data(hyperlink):
    try:
        # Faz uma solicitação HTTP para o hyperlink
        page = requests.get(hyperlink)
      
        # Analisa o HTML da página
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        # Itera sobre as linhas da tabela com a classe "fact_row"
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            # Itera sobre as células da linha
            for td_tag in td_tags:
                try: 
                    # Extrai o valor das células com a classe "value" e adiciona à lista
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        # Adiciona os dados da página à lista global
        new_planets_data.append(temp_list)

    except:
        # Em caso de erro, aguarda 1 segundo e tenta novamente
        time.sleep(1)
        scrape_more_data(hyperlink)

# Lê um arquivo CSV existente para obter os hiperlinks
planet_df_1 = pd.read_csv("updated_scraped_data.csv")

# Loop para coletar dados detalhados para cada planeta
for index, row in planet_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])
    print(f"Coleta de dados do hiperlink {index+1} concluída")

# Lista para armazenar os dados limpos
scrapped_data = []

# Limpa os dados, removendo quebras de linha
for row in new_planets_data:
    replaced = []
    for el in row: 
        el = el.replace("\n", "")
        replaced.append(el)
    scrapped_data.append(replaced)

# Cabeçalho das colunas do DataFrame
headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

# Cria um DataFrame do Pandas com os dados e o salva em um arquivo CSV
new_planet_df_1 = pd.DataFrame(scrapped_data, columns=headers)
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")
