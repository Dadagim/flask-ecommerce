from flask_login import UserMixin
from . import db
from werkzeug.security import  generate_password_hash, check_password_hash
import datetime


class Producer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    producer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    hash_password = db.Column(db.String(1000), nullable=False)
    phone_number = db.Column(db.String(22), nullable=False)
    bio  = db.Column(db.String(1000))
    is_producer = db.Column(db.Boolean(), default=True)
    profile_picture = db.Column(db.String(1000))
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.utcnow)



    products = db.relationship('Product', backref=db.backref('producer', lazy=True))

    @property
    def password(self):
        raise TypeError("Password is invisible")

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.hash_password, password)

#how to interact it with order and products in produced and it would be the best if the user can see its product and history like and subscribe it
# is it better to use flask form than html forms why? what is the advantage of using it

class Customers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    hash_password = db.Column(db.String(1000), nullable=False)
    phone_number = db.Column(db.String(22), nullable=False)
    is_producer = db.Column(db.Boolean(), default=False)
    location = db.Column(db.String(100),  nullable=False)
    date_joined = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    carts = db.relationship('Cart', backref=db.backref("customer", lazy=True))
    orders = db.relationship("Order", backref=db.backref('customer', lazy=True))

    @property
    def password(self):
        raise TypeError("Password is invisible")

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.hash_password, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000))
    product_picture = db.Column(db.String(1000), nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    flash_sale = db.Column(db.Boolean(), default=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    producer_link = db.Column(db.Integer, db.ForeignKey("producer.id"))



# cart is for the user not for the producer
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    customer_link = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    producer_link = db.Column(db.Integer, db.ForeignKey('producer.id'), nullable=False)





# orders table is must
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_link = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    customer_link = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

# history of the transaction and history of sells is recorded in history table
# the user can give comment and ratings for the producer about the product
