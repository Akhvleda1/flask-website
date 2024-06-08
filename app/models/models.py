from database.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    phone = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, nullable=False, index=True)
    address = db.Column(db.String)
    password = db.Column(db.String)

    def __str__(self):
        return f"id: {self.id}; username: {self.username}; phone: {self.phone}; email: {self.email}"


class Whiskeys(db.Model):
    __bind_key__ = 'whiskeys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    alc_percentage = db.Column(db.String)
    price = db.Column(db.Integer)
    image_link = db.Column(db.String)

    def __str__(self):
        return f"id: {self.id}; name: {self.name}; alc_per: {self.alc_percentage}; price: {self.price}"

