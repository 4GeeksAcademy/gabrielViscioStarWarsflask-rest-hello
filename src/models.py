from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

    # Relación con la tabla Favourite
    favorites = db.relationship("Favourite", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    race = db.Column(db.String(250))

    # Relación con la tabla Favourite
    favorites = db.relationship("Favourite", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "race": self.race
        }


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250)) 
    max_speed = db.Column(db.Integer)

    # Relación con la tabla Favourite
    favorites = db.relationship("Favourite", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "max_speed": self.max_speed
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))

    # Relación con la tabla Favourite
    favorites = db.relationship("Favourite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain
        }


class Favourite(db.Model):
    __tablename__ = 'favourite'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Cambié 'usuario_id' a 'user_id' para consistencia

    user = db.relationship("User", back_populates="favorites")
    character = db.relationship("Character", back_populates="favorites")
    vehicle = db.relationship("Vehicle", back_populates="favorites")
    planet = db.relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "vehicle_id": self.vehicle_id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }


    def __repr__(self):
        return '<Favourite %r>' % self.id
