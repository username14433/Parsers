import random
from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
import json
import check_proxies as ch_p



URL = 'https://www.pleer.ru/fullcatalog.html'
HEADERS = {'User-agent': 'curl/7.64.1'}
proxies_list = []


def get_session(valid_proxies):
    session = requests.Session()
    proxy = random.choice(valid_proxies)
    if len(proxy) != 0 and proxy!= None:
        session.proxies = {"http": proxy, "https": proxy}
    return session


ch_p.parse(ch_p.get_proxy_html(), proxies_list)


def main_parser(html, valid_proxies, session):
    """Main parser, parse web shop."""
    data = []
    HEADER = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'}
    soup = BeautifulSoup(html, 'lxml')
    main_categories = soup.find_all('div', class_='top-menu-category')
    for category in main_categories:
        data.append(
            {
                'main_categories': category.text,
            }
        )

    all_uls = soup.find_all('ul', class_='top-menu-catalog')
    for ul in all_uls:
        all_items = ul.find_all('li')

        with open('products_links.txt', 'r') as file:

            for line in file:
                response2 = get_session(proxies_list).get(url=line)

            soup2 = BeautifulSoup(response2, 'lxml')

            product_photo_links = soup2.find_all('div', class_='product_photo')
            for product_photo_link in product_photo_links:
                data.append(
                    {
                        'photo_link': product_photo_link.find('a', class_='product_preview_img').get('href')
                    }
                )

main_parser(get_session(ch_p.validate_proxy(proxies_list, ch_p.get_session(proxies_list))).get(url=URL).text,
            ch_p.validate_proxy(proxies_list, ch_p.get_session(proxies_list)),
            get_session(ch_p.validate_proxy(proxies_list, ch_p.get_session(proxies_list))))








