import requests
from bs4 import BeautifulSoup
import sqlite3
import os

url = 'https://www.thewhiskyexchange.com/c/32/irish-whiskey?'
payloads = {
    'pg': 1
}

current_dir = os.path.abspath(os.path.dirname(__file__))
database_file = os.path.join(current_dir, 'instance', 'whiskeys.sqlite')


def parse_whiskey_data():
    # while payloads['pg'] < 2:
    response = requests.get(url, payloads)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    grid = soup.find('div', class_='product-grid')
    items = grid.find_all('li', class_='product-grid__item')

    with sqlite3.connect(database_file, check_same_thread=False) as con:
        cur = con.cursor()
        for each in items:
            name = each.p.text.strip()
            alc_percentage = each.find('p', class_="product-card__meta").text.strip()
            price = each.find('p', class_="product-card__price").text.strip().replace('£', 'GBP ')
            image_link = each.img.attrs['src']

            # inserting data into whiskeys.sqlite file
            cur.execute('insert into whiskeys (name, alc_percentage, price, image_link) values (?, ?, ?, ?)',
                        [name, alc_percentage, price, image_link])


def whiskey_data():
    whiskeys_tracking = []
    whiskeys = []
    with sqlite3.connect(database_file, check_same_thread=False) as con:
        cur = con.cursor()
        data = cur.execute("select * from whiskeys").fetchall()
        for each in data:
            id = each[0]
            name = each[1]
            alc_per = each[2]
            price = each[3]
            image_link = each[4]

            # avoiding duplicate entries
            if name not in whiskeys_tracking:
                whiskeys_tracking.append(name)

                whiskey = {
                    'id': id,
                    'name': name,
                    'alc_percentage': alc_per,
                    'price': price,
                    'image_link': image_link
                }
                whiskeys.append(whiskey)

    return whiskeys
