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

con = sqlite3.connect(database_file, check_same_thread=False)
cur = con.cursor()


def whiskey_data():
    whiskeys_tracking = []
    whiskeys = []
    # while payloads['pg'] < 2:
    response = requests.get(url, payloads)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    grid = soup.find('div', class_='product-grid')
    items = grid.find_all('li', class_='product-grid__item')

    for each in items:
        name = each.p.text.strip()
        alc_percentage = each.find('p', class_="product-card__meta").text.strip()
        price = each.find('p', class_="product-card__price").text.strip().replace('£', 'GBP ')
        image_link = each.img.attrs['src']

        # avoiding duplicate entries
        if name not in whiskeys_tracking:
            # inserting data into whiskeys.sqlite file
            cur.execute('insert into whiskeys (name, alc_percentage, price, image_link) values (?, ?, ?, ?)', [name, alc_percentage, price, image_link])
            whiskeys_tracking.append(name)

            id = 1

            # creating list of dictionaries to return from a function
            whiskey = {
                'id': id,
                'name': name,
                'alc_percentage': alc_percentage,
                'price': price,
                'image_link': image_link
            }
            whiskeys.append(whiskey)
            id += 1

    con.commit()
    con.close()
    return whiskeys

