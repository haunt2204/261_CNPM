import hashlib
import json
from models import Category, Product, User
from SaleApp import app, db

def load_categories():
    # with open("data/cates.json", encoding="utf-8") as f:
    #     return json.load(f)
    return Category.query


def add_user(name, username, password,avatar):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()

def auth_user(username,password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()

def get_user_by_id(id):
    return User.query.get(id)

def load_products(q=None, cate_id=None):
    # with open("data/products.json", encoding="utf-8") as f:
    #     prods = json.load(f)
    #
    #     if q:
    #         prods = [p for p in prods if p["name"].find(q)>=0]
    #
    #     if cate_id:
    #         prods = [p for p in prods if p["cate_id"].__eq__(int(cate_id))]
    #
    #     return prods
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    if cate_id:
        query = query.filter(Product.cate_id.__eq__(int(cate_id)))

    return query.all()

def get_product_by_id(id):
    # with open("data/products.json", encoding="utf-8") as f:
    #     prods = json.load(f)
    #     for p in prods:
    #         if p["id"]==id:
    #             return p
    return Product.query.get(id)


if __name__=="__main__":
    with app.app_context():
        # add_user(name="User2", username="user2", password="123", avatar="https://res.cloudinary.com/dy1unykph/image/upload/v1740037805/apple-iphone-16-pro-natural-titanium_lcnlu2.webp")
        print(auth_user(username="user2", password="123"))