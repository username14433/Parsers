import requests
from bs4 import BeautifulSoup
import json
import csv

data = []


def request(url, headers):
    response = requests.get(url=url, headers=headers)
    return response.text


def parse(resp):
    soup = BeautifulSoup(resp, 'lxml')

    laptop_html = soup.find_all('div', class_='product-card__wrapper')
    for all_main_divs in laptop_html:
        data.append(
            {
                'description': all_main_divs.find('span', class_='goods-name').text +
                               all_main_divs.find('div', class_='product-card__brand-name').find('strong',
                                                                                                 class_='brand-name').text,

                'laptop_img': all_main_divs.find('div', class_='product-card__img-wrap')
                    .find('img', class_='j-thumbnail thumbnail').get('src')
            }
        )

        print(all_main_divs)


def make_json(info_json):
    with open('wildberries.json', 'w', newline='') as file:
        json.dump(info_json, file, indent=3, ensure_ascii=False)


def make_csv(info_csv, path):
    with open(path, 'w', newline='') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(('Описание ноутбука', 'Цена ноутбука'))
        for elem in info_csv:
            w.writerow((elem['description'], elem['laptop_img']))


def main():
    URL = f"https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki"
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.383 Yowser/2.5 Safari/537.36',
        'path': '/api/v1/tr.json/translate?translateMode=auto&id=17be52be28b50bf1-4-0&srv=yabrowser&text=Open%20menu&text=menu&lang=en-ru&format=html&options=2&'
    }
    parse(request(URL, HEADERS))
    make_json(data)
    make_csv(data, 'files/wildberries.csv')


if __name__ == '__main__':
    main()
