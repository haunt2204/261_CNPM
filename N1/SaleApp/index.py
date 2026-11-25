from flask import render_template, request, redirect, session, jsonify
import dao
from SaleApp import app, login, admin, utils
from flask_login import login_user, current_user, logout_user



@app.route("/")
def index():
    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    return render_template("index.html", prods=dao.load_products(q=q, cate_id=cate_id))

@app.route("/product/<int:id>")
def details(id):
    return render_template("prod_detail.html", prod=dao.get_product_by_id(id))

@app.route("/login", methods=["get","post"])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")

    err_msg = None
    if request.method.__eq__("POST"):
        user = request.form.get("username")
        password = request.form.get("password")

        u = dao.auth_user(username=user, password=password)

        if u:
            login_user(u)
            return redirect("/")
        else:
            err_msg = "Tài khoản hoặc mật khẩu chưa đúng!"

    return render_template("login.html", err_msg=err_msg)

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.context_processor
def common_attribute():
    return {
        "cates": dao.load_categories()
    }

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route("/login-admin", methods=["POST"])
def admin_login_process():
    user = request.form.get("username")
    password = request.form.get("password")

    u = dao.auth_user(username=user, password=password)

    if u:
        login_user(u)
        return redirect("/admin")
    else:
        err_msg = "Tài khoản hoặc mật khẩu chưa đúng!"


@app.route("/cart")
def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "Iphone 18",
    #         "price": 30000,
    #         "quantity": 3
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "Iphone Pro Max 15",
    #         "price": 29000000,
    #         "quantity": 1
    #     }
    # }

    return render_template("cart.html")

@app.route("/api/carts", methods=["post"])
def add_to_cart():
    cart = session.get('cart')

    if not cart:
        cart = {}

    id = request.json.get('id')

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": request.json.get('name'),
            "price": request.json.get('price'),
            "quantity": 1
        }

    session['cart'] = cart

    print(cart)

    return jsonify(utils.count_cart(cart))

if __name__=="__main__":
    app.run(debug=True)