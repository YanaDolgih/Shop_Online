from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    view = db.Column(db.String(20), nullable=False)
    seasons = db.Column(db.String(5), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.name

@app.route('/')
def home():
    items = Item.query.order_by(Item.price).all()
    return render_template('home.html', data=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    items = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": items.price
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        view = request.form['view']
        price = request.form['price']
        seasons = request.form['seasons']

        item = Item(name=name, view=view, price=price, seasons=seasons)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')

        except:
            return 'Произошла ошибка.'

    else:
        return render_template('add.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)