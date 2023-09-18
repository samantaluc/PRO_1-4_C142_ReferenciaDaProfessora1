from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# URL dos Exoplanetas da NASA
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

# Inicialização do WebDriver do Chrome
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

# Espera de 10 segundos para permitir o carregamento completo da página
time.sleep(10)

# Lista para armazenar os dados dos planetas
planets_data = []

# Função para realizar a raspagem dos dados
def scrape():
    for i in range(1, 2):  # Loop para iterar pelas páginas (neste caso, apenas uma página)
        while True:
            time.sleep(2)

            soup = BeautifulSoup(browser.page_source, "html.parser")

            # Verifique o número da página atual
            current_page_num = int(soup.find_all("input", attrs={"class": "page_num"})[0].get("value"))

            if current_page_num < i:
                # Clique no botão "Próxima Página" se a página atual for menor que a página desejada
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                # Clique no botão "Página Anterior" se a página atual for maior que a página desejada
                browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        # Itera pelas informações dos exoplanetas na página
        for ul_tag in soup.find_all("ul", attrs={"class": "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    # Nome do exoplaneta
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")

            # Obtenha a Tag do Hiperlink
            hyperlink_li_tag = li_tags[0]

            # URL do exoplaneta
            temp_list.append("https://exoplanets.nasa.gov" + hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            planets_data.append(temp_list)

        # Clique no botão "Próxima Página" para acessar a próxima página
        browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

        print(f"Coleta de dados da página {i} concluída")

# Chama a função de raspagem
scrape()

# Define o cabeçalho das colunas do DataFrame
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink"]

# Cria um DataFrame Pandas com os dados coletados
planet_df_1 = pd.DataFrame(planets_data, columns=headers)

# Salva os dados em um arquivo CSV
planet_df_1.to_csv('updated_scraped_data.csv', index=True, index_label="id")
