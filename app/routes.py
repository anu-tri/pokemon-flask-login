import requests
from flask import render_template, request, redirect, url_for
from app import app
from .forms import LoginForm, PokemonForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

#homepage
@app.route('/')
@login_required
def index():
    return render_template('index.html.j2')
    

#login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = request.form.get("email").lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        
        if u and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            return redirect(url_for('index'))
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)

    return render_template("login.html.j2", form=form)


#logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))


#register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            #create an empty user
            new_user_object = User()
            #build user with form data
            new_user_object.from_dict(new_user_data)
            #save user to db
            new_user_object.save()
        except:
            error_string="There was an error creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        # registered successfully 
        return redirect(url_for('login'))
    return render_template('register.html.j2',form=form)


#pokemon search 
@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    
    if request.method == 'POST':
        name = request.form.get('name').lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        pokemon_details = []

        if response.ok:
                #request worked
                if not response.json():
                    return "Error loading pokemon details."
                pokemon = response.json()
                
                pokemon_data={
                    'id': pokemon['id'],
                    'name': pokemon['name'],
                    'order': pokemon['order'],
                    'hp': pokemon['stats'][0]['base_stat'],
                    'defense': pokemon['stats'][2]['base_stat'],
                    'attack': pokemon['stats'][1]['base_stat'],
                    'url': pokemon['sprites']['front_shiny']
                }
                pokemon_details.append(pokemon_data)
        else:
            # The request fail
            error_string = "<br><h6>We have a problem. Please search for another pokemon.<h6>"
            return render_template('pokemon.html.j2', error = error_string, form=form)
                
        return render_template('pokemon.html.j2', pokemon=pokemon_details, form=form)   
    return render_template('pokemon.html.j2', form=form)  
