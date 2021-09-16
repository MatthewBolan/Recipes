
from models.recipes import Recipe

import re

from models.users import User

from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)

app.secret_key = 'ServerKey'

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)



@app.route('/')
def index():

    return redirect("/register/login")




@app.route('/register/login')
def register_login_page():

    return render_template("register_login.html")





@app.route('/user/register', methods=['POST'])
def registered_user():

    if not User.validate(request.form):

        return redirect('/')

    data = {

        "first_name": request.form ['first_name'],

        "last_name": request.form ['last_name'],

        "email": request.form ['email'],

        "password": bcrypt.generate_password_hash(request.form['password']) 

    }

    id = User.save_user(data)

    session['user_id'] = id

    return redirect ('/welcome')





@app.route('/welcome')
def welcome():

    if 'user_id' not in session:

        return redirect ('/logout')

    data = {

        'id': session ['user_id']

    }

    return render_template("welcome.html", user = User.user_by_id_recipes(data))



@app.route('/user/login', methods=['POST'])
def login_user():

    user = User.user_by_email(request.form)


    if not user:

        flash ("Email Not Valid. Please Try Again!" , "login")

        return redirect ('/')


    if not bcrypt.check_password_hash (user.password, request.form ['password']):

        flash ("Password Not Valid. Please Try Again!", "login")

        return redirect ('/')


    session ['user_id'] = user.id

    return redirect('/welcome')





@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')









@app.route('/add/recipe')
def recipe_add():

    if 'user_id' not in session:

        return redirect ('/logout')

    data = {

        'id': session ['user_id']

    }

    return render_template("add_recipe.html")






@app.route('/recipe/added', methods=['POST'])
def added_recipe():

    if 'user_id' not in session:

        return redirect ('/logout')

    if not Recipe.validate_recipe(request.form):

            return redirect('/add/recipe')

    data = {

        "name": request.form["name"],

        "description": request.form["description"],

        "instruction": request.form["instruction"],

        "under_30": int(request.form["under_30"]),

        "date_made": request.form["date_made"],

        "user_id": session ["user_id"]

    }

    Recipe.save_recipe(data)

    return redirect ('/welcome')






@app.route('/edit/recipe/<int:id>')
def recipe_edit(id):

    if 'user_id' not in session:

        return redirect ('/logout')

    data = {

        'id':id 

    }

    user_data = {


        'id': session ['user_id']

    }



    return render_template("edit_recipe.html",edit=Recipe.get_one_recipe(data), user = User.user_by_id(user_data))



@app.route('/recipe/edited/<int:id>', methods=['POST'])
def edited_recipe(id):

    if 'user_id' not in session:

        return redirect ('/logout')

    if not Recipe.validate_recipe(request.form):

        return redirect(f'/edit/recipe/{id}')

    

    data = {

        "name": request.form["name"],

        "description": request.form["description"],

        "instruction": request.form["instruction"],

        "under_30": int(request.form["under_30"]),

        "date_made": request.form["date_made"],

        "id":id

    }


    Recipe.edit_recipe(data)

    return redirect ('/welcome')




@app.route('/show/recipe/<int:id>')
def recipe_show(id):

    if 'user_id' not in session:

        return redirect ('/logout')

    data = {

        'id':id 

    }

    user_data = {


        'id': session ['user_id']

    }



    return render_template("show_recipe.html",show=Recipe.get_one_recipe(data), user = User.user_by_id(user_data))









@app.route('/recipe/delete/<int:id>')
def recipe_deleted(id):
    data = {

        'id':id

    }

    Recipe.delete_recipe(data)

    return redirect('/welcome')






if __name__ == "__main__":
    app.run(debug=True)