from flask import Blueprint, render_template, redirect, url_for
from data_scraper import whiskey_data

routes = Blueprint('routes', __name__, static_folder='static', template_folder='templates')

cards = whiskey_data()


@routes.route('about/item_id=<int:item_id>')
def about_item(item_id):
    item = next((card for card in cards if card['id'] == item_id), None)
    if item:
        return render_template('routes/about.html', title='About Item', item=item)
    else:
        return redirect(url_for('routes.shop'))


@routes.route('shop')
def shop():
    return render_template('routes/shop.html', title='Shop', cards=cards)

