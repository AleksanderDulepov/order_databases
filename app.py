from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import utils
import datetime as dt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///order_db"
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app)

# исходные данные для БД
users_json = utils.get_data_from_json("jsons/users.json")
offers_json = utils.get_data_from_json("jsons/offers.json")
orders_json = utils.get_data_from_json("jsons/orders.json")

# редактируем формат даты
orders_json = utils.edit_date_format(orders_json)

# создаем модели
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    # order = db.relationship("Order")

class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("orders.executor_id"))

    # orders = db.relationship("Order")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # user = relationship('User', foreign_keys=[customer_id])
    # executor = relationship('User', foreign_keys=[executor_id])
    # offers=db.relationship("Offer")


db.drop_all()
db.create_all()


# создаем обьекты классов из json
users_list = utils.get_objects_list(users_json, User)
offers_list = utils.get_objects_list(offers_json, Offer)
orders_list = utils.get_objects_list(orders_json, Order)


# заполняем таблицы данными
with db.session.begin():
    db.session.add_all(users_list)
    db.session.add_all(offers_list)
    db.session.add_all(orders_list)


# главная страница
@app.route("/")
def index_page():
    return render_template("index_page.html")

# все пользователи
@app.route("/users", methods=["GET"])
def get_all_users():
    query = User.query.all()
    output_list = []
    for item in query:
        cur_dict = {}
        cur_dict['id'] = item.id
        cur_dict['first_name'] = item.first_name
        cur_dict['last_name'] = item.last_name
        cur_dict['age'] = item.age
        cur_dict['email'] = item.email
        cur_dict['role'] = item.role
        cur_dict['phone'] = item.phone
        output_list.append(cur_dict)
    return jsonify(output_list)

# один пользователь по идентификатору
@app.route("/users/")
def get_user_by_id():
    id = request.args.get("id")
    query = User.query.get(id)

    cur_dict = {}
    cur_dict['id'] = query.id
    cur_dict['first_name'] = query.first_name
    cur_dict['last_name'] = query.last_name
    cur_dict['age'] = query.age
    cur_dict['email'] = query.email
    cur_dict['role'] = query.role
    cur_dict['phone'] = query.phone

    return jsonify(cur_dict)

# все заказы
@app.route("/orders")
def get_all_orders():
    query = Order.query.all()
    output_list = []
    for item in query:
        cur_dict = {}
        cur_dict['id'] = item.id
        cur_dict['name'] = item.name
        cur_dict['description'] = item.description
        cur_dict['start_date'] = item.start_date
        cur_dict['end_date'] = item.end_date
        cur_dict['address'] = item.address
        cur_dict['price'] = item.price
        cur_dict['customer_id'] = item.customer_id
        cur_dict['executor_id'] = item.executor_id
        output_list.append(cur_dict)
    return jsonify(output_list)

# один заказ по идентификатору
@app.route("/orders/")
def get_order_by_id():
    id = request.args.get("id")
    query = Order.query.get(id)

    cur_dict = {}
    cur_dict['id'] = query.id
    cur_dict['name'] = query.name
    cur_dict['description'] = query.description
    cur_dict['start_date'] = query.start_date
    cur_dict['end_date'] = query.end_date
    cur_dict['address'] = query.address
    cur_dict['price'] = query.price
    cur_dict['customer_id'] = query.customer_id
    cur_dict['executor_id'] = query.executor_id

    return jsonify(cur_dict)


# все офферы
@app.route("/offers")
def get_all_offers():
    query = Offer.query.all()
    output_list = []
    for item in query:
        cur_dict = {}
        cur_dict['id'] = item.id
        cur_dict['order_id'] = item.order_id
        cur_dict['executor_id'] = item.executor_id
        output_list.append(cur_dict)
    return jsonify(output_list)


# один оффер по идентификатору
@app.route("/offers/")
def get_offer_by_id():
    id = request.args.get("id")
    query = Offer.query.get(id)

    cur_dict = {}
    cur_dict['id'] = query.id
    cur_dict['order_id'] = query.order_id
    cur_dict['executor_id'] = query.executor_id

    return jsonify(cur_dict)

# создание пользователя User
@app.route("/users", methods=["POST"])
def add_user_to_db():
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    age = request.form.get('age', None)
    email = request.form.get('email', None)
    role = request.form.get('role', None)
    phone = request.form.get('phone', None)

    user = User(first_name=first_name, last_name=last_name, age=age, email=email, role=role, phone=phone)

    # заполняем таблицы данными
    with db.session.begin():
        db.session.add(user)

    return ("Пользователь успешно добавлен!")

# обновление информации о пользователе User
@app.route("/users/<int:id>", methods=["PUT"])
def edit_user(id):
    user_to_edit = request.json
    current_user = User.query.get(id)
    # проще создать новый обьект, чем переприсваивать атрибуты
    edited_user = utils.get_objects_list(user_to_edit, User)[0]
    edited_user.id = id  # чтобы заменить в том же id

    db.session.delete(current_user)
    db.session.add(edited_user)
    db.session.commit()

    return (f"Пользователь c id {id} успешно обновлен!")

# удаление пользователя User
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    current_user = User.query.get(id)

    db.session.delete(current_user)
    db.session.commit()

    return (f"Пользователь c id {id} удален из базы данных!")

# создание заказа Order
@app.route("/orders", methods=["POST"])
def add_order_to_db():
    name = request.form.get('name', None)
    description = request.form.get('description', None)
    start_date = request.form.get('start_date', None)
    # форматирование ввода даты
    start_date = dt.datetime.strptime(start_date, '%m/%d/%Y')
    end_date = request.form.get('end_date', None)
    # форматирование ввода даты
    end_date = dt.datetime.strptime(end_date, '%m/%d/%Y')
    address = request.form.get('address', None)
    price = request.form.get('price', None)
    customer_id = request.form.get('customer_id', None)
    executor_id = request.form.get('executor_id', None)

    order = Order(name=name, description=description, start_date=start_date, end_date=end_date, address=address,
                  price=price, customer_id=customer_id, executor_id=executor_id)

    # заполняем таблицы данными
    with db.session.begin():
        db.session.add(order)

    return ("Заказ успешно добавлен!")


# обновление информации о заказе Order
@app.route("/orders/<int:id>", methods=["PUT"])
def edit_order(id):
    order_to_edit = request.json
    # форматирование ввода даты
    order_to_edit = utils.edit_date_format(order_to_edit)
    current_order = Order.query.get(id)
    # проще создать новый обьект, чем переприсваивать атрибуты
    edited_order = utils.get_objects_list(order_to_edit, Order)[0]
    edited_order.id = id  # чтобы заменить в том же id

    db.session.delete(current_order)
    db.session.add(edited_order)
    db.session.commit()

    return (f"Заказ c id {id} успешно обновлен!")


# удаление заказа Order
@app.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    current_order = Order.query.get(id)

    db.session.delete(current_order)
    db.session.commit()

    return (f"Заказ c id {id} удален из базы данных!")

# создание предложения Offer
@app.route("/offers", methods=["POST"])
def add_offer_to_db():
    order_id = request.form.get('order_id', None)
    executor_id = request.form.get('executor_id', None)

    offer = Offer(order_id=order_id, executor_id=executor_id)

    # заполняем таблицы данными
    with db.session.begin():
        db.session.add(offer)

    return ("Предложение успешно добавлено!")


# обновление информации о предложении Offer
@app.route("/offers/<int:id>", methods=["PUT"])
def edit_offer(id):
    offer_to_edit = request.json
    current_offer = Offer.query.get(id)
    # проще создать новый обьект, чем переприсваивать атрибуты
    edited_offer = utils.get_objects_list(offer_to_edit, Offer)[0]
    edited_offer.id = id  # чтобы заменить в том же id

    db.session.delete(current_offer)
    db.session.add(edited_offer)
    db.session.commit()

    return (f"Предложение c id {id} успешно обновлено!")

# удаление предложения Offer
@app.route("/offers/<int:id>", methods=["DELETE"])
def delete_offer(id):
    current_offer = Offer.query.get(id)

    db.session.delete(current_offer)
    db.session.commit()

    return (f"Предложение c id {id} удалено из базы данных!")


if __name__ == '__main__':
    app.run(debug=True)
