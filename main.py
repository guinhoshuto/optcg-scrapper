import requests
import pandas as pd
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=[
    'code', 
    'code_variant',
    'rarity', 
    'type', 
    'life',
    'name', 
    'color', 
    'cost', 
    'power', 
    'counter', 
    'feature', 
    'character_type', 
    'description', 
    'trigger',
    'image'
])


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    collections = soup.find('select', id='series')
    series = collections.find_all('option')
    series = [{'id': option['value'], 'name': option.get_text()} for option in series]
    print(series)

    
    data = []
    for item in soup.find_all('dl', class_="modalCol"):
        dt = item.find('dt')
        dd = item.find('dd')
        front_col = dd.find('div', class_="frontCol")
        back_col = dd.find('div', class_="backCol")
        info_cols = back_col.find_all('div', {"class":"col2"})
        card_title = dt.find('div', class_="infoCol").get_text(strip=True),
        card_title = card_title[0].split("|")

        code = card_title[0]
        rarity = card_title[1]
        card_type = card_title[2]
        card_name =  dt.find('div', class_="cardName").get_text(strip=True)

        code_variant = item.get('id')

        print(card_title, card_name)
        character_type = info_cols[0].find('div', class_="attribute").get_text(strip=True) 
        character_type = character_type.split("Attribute")[1]

        feature = back_col.find('div', class_="feature").get_text(strip=True)
        feature = feature.split("Type")[1]

        cost = info_cols[0].find('div', class_="cost").get_text(strip=True)
        if(card_type == 'LEADER'):
            life = cost.split("Life")[1]
            cost = ''
        else: 
            life = ''
            cost = cost.split("Cost")[1]

        power = info_cols[1].find('div', class_="power").get_text(strip=True)
        power = power.split("Power")[1]

        counter = info_cols[1].find('div', class_="counter").get_text(strip=True)
        counter = counter.split("Counter")[1]

        color = back_col.find('div', class_="color").get_text(strip=True)
        color = color.split("Color")[1]

        description = back_col.find('div', class_="text").get_text(strip=True)
        description = description.split("Effect")[1]

        try:
            trigger = back_col.find('div', class_="trigger").get_text()
            trigger = trigger.split("[Trigger]")[1]
        except:
            trigger = ''

        imagem = front_col.find('img').get('src')
        df.loc[len(df.index)] = [
            code, 
            code_variant,
            rarity, 
            card_type, 
            life,
            card_name, 
            color,
            cost,
            power,
            counter,
            feature, 
            character_type,
            description, 
            trigger,
            "https://en.onepiece-cardgame.com"+ imagem
        ]

    return data

def scrape_all_pages(base_url, start_page, end_page):
    """Faz o scraping de várias páginas, gerenciando a paginação."""
    # all_data = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    collections = soup.find('select', id='series')
    series = collections.find_all('option')
    series = [{'id': option['value'], 'name': option.get_text()} for option in series]
    for serie in series:
        if serie['id'] == '':
            continue
        print(serie)
        serie_url = "https://en.onepiece-cardgame.com/cardlist/?series=" + serie['id']
        response_serie = requests.get(serie_url)
        serie_page = BeautifulSoup(response_serie.content, 'html.parser')

        for page_number in range(start_page, end_page + 1):
            url = f"{serie_url}?page={page_number}"
            scrape_page(serie_url)
            # page_data = scrape_page(url)
            # all_data.extend(page_data)
            print(f"Dados coletados da página {page_number}")


# Exemplo de como usar as funções
base_url = "https://en.onepiece-cardgame.com/cardlist/"
start_page = 1
end_page = 1
scrape_all_pages(base_url, start_page, end_page)
print(df)
df.to_csv('output.csv', index=False)
