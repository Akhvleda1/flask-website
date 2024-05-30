from flask import Blueprint, render_template, redirect, url_for
from data_scraper import whiskey_data

other_routes = Blueprint('other_routes', __name__)

cards = whiskey_data()


@other_routes.route('/')
@other_routes.route('/home')
def home():
    return render_template('home.html')


@other_routes.route('/about/item_id=<int:item_id>')
def about_item(item_id):
    item = next((card for card in cards if card['id'] == item_id), None)
    if item:
        return render_template('about.html', title='About Item', item=item)
    else:
        return redirect(url_for('shop'))


@other_routes.route('/shop')
def shop():
    return render_template('shop.html', title='Shop', cards=cards)

