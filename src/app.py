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


#  Users

#  Get all users
@app.route('/users', methods=['GET'])
def get_users():

    allusers = User.query.all()
    userlist = list(map(lambda p: p.serialize(), allusers))

    if userlist == []:
        return {"msg": "no hay usuarios creados"}, 400
    return jsonify(userlist), 200

#  Get all user favorites
@app.route('/users/favorites', methods=['GET'])
def get_favorites_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#  CHARACTERS

#  Get all charactes
@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200

#  Get a specific character by id
@app.route('/people/<int:character_id>', methods=['GET'])
def get_specific_character(character_id):
     character = Character.query.get(character_id)
     if character == None:
        return {"Error": "Character not found"}, 400
     return jsonify(character.serialize()), 200

#  Post a character as a favorite
@app.route('/favorite/people/<int:character_id>', methods=['POST'])
def add_favorite_character():
    return None

#  Delete a character
@app.route('/favorite/people/<int:character_id>', methods=['DELETE'])
def delete_character():
        pass

#  PLANETS

#  Get all planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

#  Get a specific planet by id
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_specific_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet == None:
        return {"Error": "Planet not found"}, 400
    return jsonify(planet.serialize()), 200

#  Post a planet as a favorite
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet():
        pass

#  Delete a planet
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet():
        pass
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
