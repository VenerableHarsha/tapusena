from flask import Flask, request, flash, jsonify
from ScrapeData import search_field, place_lst
from main import Shops
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from sqlalchemy import create_engine
my_conn = create_engine("mysql+mysqldb://krishhashia:aarav@localhost/shop_owner_db")

# @app.route('/random/<int:hotel_id>')
# def put_hotels(start_pt, end_pt):
#     search_field.send_keys(start_pt, end_pt)
#     for i in place_lst:
#         new_hotel = Shops(Shop_name=i, password=generate_password_hash(request.form.get('Password'),  method='pbkdf2:sha256',salt_length=8))
#         if Shops.query.filter_by(Shop_name=i).first():
#             flash(message='this shop is already registered!')
#         else:
#             db.session.add(new_hotel)
#             db.session.commit()
#     return place_lst


@app.route('/hotels/<start_pt>/<end_pt>')     # params should be specified in both def and route
def get_put_hotels(start_pt, end_pt):
    search_field.send_keys(start_pt, end_pt)
    for i in place_lst:
        try:
            query = "INSERT INTO  `shop_owner_db`.`shop_name` ('id')  VALUES(%s,%s)"
            my_data = [(place_lst[i], i)]
            id = my_conn.execute(query, my_data)
            print("Rows Added  = ", id.rowcount)
        except:
            print("Database error ")
        # request.form.get('Password')
        # new_hotel = Shops(Shop_name=i, Password=generate_password_hash('sjacnsaxb',  method='pbkdf2:sha256',salt_length=8))
        # if Shops.query.filter_by(Shop_name=i).first():
        #     # flash(message='this shop is already registered!')
        #     pass
        # else:
    #     #     db.session.add_all(new_hotel)
    #     id = my_conn.execute("INSERT INTO  `shop_owner_db`.`student` (`name` ,`class` ,`mark` ,`sex`) \
    #                       VALUES ('King1',  'Five',  '45',  'male')")
    #     print("Row Added  = ", id.rowcount)
    # db.session.commit()

    return jsonify(username=[i for i in place_lst],
                   email='krishhashia19@gmail.com',
                   id=[i for i in range(len(place_lst))])


if __name__=='__main__':
    app.run(debug=True)