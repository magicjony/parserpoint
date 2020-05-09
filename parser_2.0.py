import requests

from bs4 import BeautifulSoup
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://technopoint.ru'

import csv
from multiprocessing import Pool
#получаем адрес
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r.text

#получаем список ссылок на каждый телефон
def get_all_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    items = soup.find_all('div', class_='catalog-item')
    

    links = []
    n = 0
    
    for item in items:
            if n < 10:
                a = item.find('a', class_='ui-link').get('href')
                link = HOST + a   
                links.append(link) 
                n += 1
        
    return links    
# составлем список данных которые будем "парсить""   
def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.find('h1', class_='page-title price-item-title').get_text(strip=True)   
    serial = soup.find('div', class_='price-item-code').find_next('span').get_text(strip=True)
    price = soup.find('div', class_='price_g').find_next('span').get_text(strip=True)
    img = soup.find('div', class_='img').find('img').get('src')

    data = {'name': name, 'serial': serial, 'price': price, 'img': img}
    return data            
            
   
    
#запись в документ
def write_csv(data):
    with open('list.csv','a', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['наименование', 'серийный номер', 'цена', 'ссылка на изображение'])
        writer.writerow(( data['name'],data['serial'],data['price'],data['img']))
        print(data['name'], 'parsed')  
# сборка всех нужных нам данных и запись их в файл    
def make_all(url):
    html = get_html(url)
        
    data = get_page_data(html)
    write_csv(data)
#собираем всю эту матрешку   
def main():
    
    url = 'https://technopoint.ru/catalog/recipe/e351231ca6161134/2020-goda/'

    all_links = get_all_links(get_html(url))
    # for url in all_links:
    #     print(url)
    #     html = get_html(url)
        
    #     data = get_page_data(html)
    #     print(data)
    #     write_csv(data)

    with Pool(10) as p:
        p.map(make_all, all_links)
if __name__ == '__main__':
    main()
