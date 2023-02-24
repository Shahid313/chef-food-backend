from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import socket
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import text

app = Flask(__name__)

app.app_context().push()

app.config['SECRET_KEY'] = 'asjd9792nasd887a8dA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chefffood'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
ma = Marshmallow(app)
CORS(app)

def remove_file(file, type):
    file_name = file
    folder = os.path.join(app.root_path, "static/" + type + "/"+file_name)
    os.remove(folder)
    return 'File Has Been Removed'


def save_file(file, type):
    file_name = secure_filename(file.filename)
    file_ext = file_name.split(".")[1]
    folder = os.path.join(app.root_path, "static/" + type + "/")
    file_path = os.path.join(folder, file_name)
    try:
        file.save(file_path)
        return True, file_name
    except:
        return False, file_name


class User(db.Model):
    user_id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    role = db.Column(db.String(200))
    password = db.Column(db.String(300))

    def __init__(self,name,email,role,password):
        self.name = name
        self.email = email
        self.role = role
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'email','role', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer(), primary_key=True)
    recipe_name = db.Column(db.String(300))
    recipe_picture = db.Column(db.String(300))
    recipe_description = db.Column(db.String(300))
    recipe_ingredients = db.Column(db.String(300))
    recipe_price = db.Column(db.Integer)
    delivery_price = db.Column(db.Integer)
    time = db.Column(db.String(300))
    chef_name = db.Column(db.String(300))
    added_by = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    date = db.Column(db.Date(),default=datetime.now())
    
    def __init__(self,recipe_name,recipe_picture,recipe_description,recipe_ingredients,recipe_price,delivery_price,time,chef_name, added_by):
        self.recipe_name = recipe_name
        self.recipe_picture = recipe_picture
        self.recipe_description = recipe_description
        self.recipe_ingredients = recipe_ingredients
        self.recipe_price = recipe_price
        self.delivery_price = delivery_price
        self.time = time
        self.chef_name = chef_name
        self.added_by = added_by

class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('recipe_id', 'recipe_name', 'recipe_picture','recipe_description','recipe_ingredients','recipe_price','delivery_price','time','chef_name','added_by','date')

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)


class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True)
    customer_name = db.Column(db.String(100))
    ordered_recipe_name = db.Column(db.String(200))
    ordered_recipe_picture = db.Column(db.String(200))
    address = db.Column(db.String(300))
    order_quantity = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    delivery_price = db.Column(db.Integer)
    recipe_ingredients = db.Column(db.String(300))
    chef_name = db.Column(db.String(300))
    time = db.Column(db.String(200))
    status = db.Column(db.String(300))
    date = db.Column(db.Date(),default=datetime.now())
    
    def __init__(self,customer_name,ordered_recipe_name,ordered_recipe_picture,address,order_quantity,total_price,delivery_price,recipe_ingredients,chef_name,time,status):
        self.customer_name = customer_name
        self.ordered_recipe_name = ordered_recipe_name
        self.ordered_recipe_picture = ordered_recipe_picture
        self.address = address
        self.order_quantity = order_quantity
        self.total_price = total_price
        self.delivery_price = delivery_price
        self.recipe_ingredients = recipe_ingredients
        self.chef_name = chef_name
        self.time = time
        self.status = status

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'customer_name','ordered_recipe_name','ordered_recipe_picture', 'address','order_quantity','total_price','delivery_price','recipe_ingredients','chef_name','time','status','date')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

   

@app.route('/get_all_recipes')
def get_all_recipes():
    recipes = Recipe.query.all()
    results = recipes_schema.dump(recipes)
    return jsonify({
        "recipes":results
    })

@app.route('/get_all_orders')
def get_all_orders():
    orders = Order.query.all()
    results = orders_schema.dump(orders)
    return jsonify({
        "orders":results
    })

@app.route('/get_recipes_by_user_id')
def get_recipes_by_user_id():
    user_id = request.args.get("user_id")
    recipes = Recipe.query.filter_by(added_by=user_id).all()
    results = recipes_schema.dump(recipes)
    return jsonify({
        "recipes":results
    })

@app.route("/get_recipe_by_id")
def GetRecipeById():
    recipe_id = request.args.get("recipe_id")
    recipe = Recipe.query.get(recipe_id)
    result = recipe_schema.dump(recipe)
    return jsonify({
        "recipe": result
    })


@app.route("/get_order_by_id")
def get_order_by_id():
    order_id = request.args.get("order_id")
    order = Order.query.get(order_id)
    result = order_schema.dump(order)
    return jsonify({
        "order": result
    })

@app.route("/delete_recipe")
def delete_recipe():
    recipe_id = request.args.get("recipe_id")
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({
        "msg": "recipe deleted successfully"
    })


@app.route("/add_recipe",methods=["POST"])
def add_recipe():
    recipe_name = request.form.get("recipe_name")
    recipe_price = request.form.get("recipe_price")
    recipe_description = request.form.get("recipe_description")
    recipe_picture = request.files.get("recipe_picture")
    delivery_price = request.form.get("delivery_price")
    recipe_time = request.form.get("recipe_time")
    recipe_ingredients = request.form.get("recipe_ingredients")
    chef_name = request.form.get("chef_name")
    user_id = request.form.get("user_id")
    isSaved, file_name = save_file(recipe_picture,"uploads")
    new_recipe = Recipe(recipe_name,file_name,recipe_description,recipe_ingredients,recipe_price,delivery_price,recipe_time,chef_name,user_id)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({
        "msg":"Added Successfully"
    })

@app.route("/add_order",methods=["POST"])
def add_order():
    ordered_recipe_id = request.form.get("ordered_recipe_id")
    recipes = Recipe.query.filter_by(recipe_id=ordered_recipe_id).first()
    result = recipe_schema.dump(recipes)
    customer_name = request.form.get("customer_name")
    address = request.form.get("address")
    order_quantity = request.form.get("order_quantity")
    total_price = request.form.get("total_price")
    status = request.form.get("status")
    new_order = Order(customer_name,result['recipe_name'],result['recipe_picture'],address,order_quantity,total_price,result['delivery_price'],result['recipe_ingredients'],result['chef_name'],result['time'],status)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({
        "msg":"Ordered Successfully"
    })

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    recipe_name = request.form.get("recipe_name")
    recipe_price = request.form.get("recipe_price")
    recipe_description = request.form.get("recipe_description")
    recipe_picture = request.files.get("recipe_picture")
    delivery_price = request.form.get("delivery_price")
    recipe_time = request.form.get("recipe_time")
    recipe_ingredients = request.form.get("recipe_ingredients")
    chef_name = request.form.get("chef_name")
    recipe_id = request.form.get("recipe_id")
    recipe = Recipe.query.get(recipe_id)
    
    if recipe_picture:
        save_file(recipe_picture,"uploads")
        recipe.recipe_picture = recipe_picture.filename
        print(recipe_picture)
        recipe.recipe_name = recipe_name
        recipe.recipe_price = recipe_price
        recipe.delivery_price = delivery_price
        recipe.chef_name = chef_name
        recipe.recipe_ingredients = recipe_ingredients
        recipe.recipe_description = recipe_description
        recipe.recipe_time = recipe_time
        db.session.commit()
    else:
        recipe.recipe_name = recipe_name
        recipe.recipe_price = recipe_price
        recipe.delivery_price = delivery_price
        recipe.chef_name = chef_name
        recipe.recipe_ingredients = recipe_ingredients
        recipe.recipe_description = recipe_description
        recipe.time = recipe_time
        db.session.commit()
    
    return jsonify({
        "msg":"Updated Successfully"
    })


@app.route("/update_profile", methods=["POST"])
def update_profile():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    userId = request.form.get("userId")
    user = User.query.get(userId)
    
    if password:
        hashed_password = generate_password_hash(password)
        user.name = name
        user.email = email
        user.password = password
        db.session.commit()
    else:
        user.name = name
        user.email = email
        db.session.commit()
    
    return jsonify({
        "msg":"Profile Updated Successfully"
    })


@app.route("/mark_order_as_delivered", methods=["POST"])
def mark_order_as_delivered():
    order_id = request.form.get("order_id")
    order = Order.query.get(order_id)
    order.status = "delivered"
    db.session.commit()
    
    return jsonify({
        "msg":"Marked as delivered"
    })


@app.route("/login",methods=["POST"])
def Login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password,password):
        user_data = user_schema.dump(user)
        return jsonify({
            "user":user_data,
            "msg":"logged in successfully",
        })
    else:
        return jsonify({
            "msg":"Invalid Email or Password"
        })




@app.route("/register", methods=["POST"])
def Register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({
            "msg":"Email already exist"
        })
    else:
        new_user = User(name,email,"normal_user",generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "msg":"Successfully registered"
        })

hostname = socket.gethostname()

ip_address = socket.gethostbyname(hostname)

if __name__ == '__main__':
    app.run(host=ip_address,debug=True)