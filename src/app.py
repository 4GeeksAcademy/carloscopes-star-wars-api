"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#  USERS

#  Get all users ✅
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    if all_users == None:
        return {"Message": "No users created"}, 400
    return jsonify(all_users), 200

#  Get all user favorites ❌
@app.route('/users/favorites', methods=['GET'])
def get_favorites_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#  CHARACTERS

#  Get all characters ✅
@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200

#  Get a specific character by id ✅
@app.route('/people/<int:character_id>', methods=['GET'])
def get_specific_character(character_id):
     character = Character.query.get(character_id)
     if character == None:
        return {"Error": "Character not found"}, 400
     return jsonify(character.serialize()), 200

#  Post/create a character ✅
@app.route('/people', methods=['POST'])
def create_character():

    body = request.get_json()

    name = body.get("name", None)
    url = body.get("url", None)
    height = body.get("height", None)
    mass = body.get("mass", None)
    hair_color = body.get("hair_color", None)
    skin_color = body.get("skin_color", None)
    eye_color = body.get("eye_color", None)
    birth_year = body.get("birth_year", None)
    gender = body.get("gender", None)
    img = body.get("img", None)

    try:
        new_character = Character(name=name, url=url, height=height, mass=mass, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color, birth_year=birth_year, gender=gender, img=img)

        db.session.add(new_character)
        db.session.commit()

        return new_character.serialize(), 200
    
    except ValueError as err:
        return { "Message" : " An unexpected error has ocurred " + err }, 500

#  Post a character as a favorite
@app.route('/favorite/people/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    character = Character.query.get(character_id)




#  Delete a character ✅
@app.route('/people/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    try:
        specific_character = Character.query.get(character_id)
        if specific_character == None:
            return {"message": f"Characte with id {character_id} doesn't exist"}, 400
        else:
            db.session.delete(specific_character)
            db.session.commit()
            return {"message": f"{specific_character.serialize()['name']} has been deleted"}

    except ValueError as err:
        return {"message": "Character deletion failed"}, 500


#  Delete a character from Favorites ❌

#  PLANETS

#  Get all planets ✅
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

#  Get a specific planet by id ✅
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_specific_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet == None:
        return {"Error": "Planet not found"}, 400
    return jsonify(planet.serialize()), 200

#  Post/create a planet ✅
@app.route('/planet', methods=['POST'])
def planet():

    body = request.get_json()

    name = body.get("name", None)
    url = body.get("url", None)
    diameter = body.get("diameter", None)
    gravity = body.get("gravity", None)
    population = body.get("population", None)
    climate = body.get("climate", None)
    terrain = body.get("terrain", None)
    surface_water = body.get("surface_water", None)
    img = body.get("img", None)    

    try:
        new_planet = Planet(name=name, url=url, diameter=diameter, gravity=gravity, population=population, climate=climate, terrain=terrain, surface_water=surface_water, img=img)

        db.session.add(new_planet)
        db.session.commit()

        return new_planet.serialize(), 200
    
    except ValueError as err:
        return { "Message" : " An unexpected error has ocurred " + err }, 500


#  Post a planet as a favorite ❌
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet():
    pass

#  Delete a planet ✅
@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        specific_planet = Planet.query.get(planet_id)
        if specific_planet == None:
            return {"message": f"Characte with id {planet_id} doesn't exist"}, 400
        else:
            db.session.delete(specific_planet)
            db.session.commit()
            return {"message": f"{specific_planet.serialize()['name']} has been deleted"}
    except ValueError as err:
        return {"message": "Planet deletion failed"}, 500

#  Delete a planet from Favorites ❌
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
