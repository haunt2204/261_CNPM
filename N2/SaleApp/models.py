import json

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from SaleApp import app, db


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=True, unique=True)

    def __str__(self):
        return self.name


class Category(Base):
    products = relationship('Product', backref='category', lazy=True)


class Product(Base):
    price = Column(Float, default=0.0)
    image = Column(String(300), default="https://res.cloudinary.com/dy1unykph/image/upload/v1729842193/iPhone_15_Pro_Natural_1_ltf9vr.webp")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=True)


if __name__=='__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Laptop")
        # c3 = Category(name="Tablet")
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # print(c1)

        with open("data/products.json", encoding="utf-8") as f:
            prods = json.load(f)

            for p in prods:
                db.session.add(Product(**p))
        db.session.commit()