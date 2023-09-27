from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(50), nullable=False)
    mass = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    skin_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Character {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "img": self.img,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.String(50), nullable=False)
    gravity = db.Column(db.String(50), nullable=False)
    population = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)
    surface_water = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Planet {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "img": self.img,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer(), db.ForeignKey("character.id"))
    planet_id = db.Column(db.Integer(), db.ForeignKey("planet.id"))

    user = db.relationship("User")
    character = db.relationship("Character")
    planet = db.relationship("Planet")


    def __repr__(self):
        return f"<Favorite {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.people_id,
            "character": self.people.name,
            "planet_id": self.planet_id,
            "planet": self.planet.name
        }
