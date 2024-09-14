"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle

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

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# User endpoints
@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all()
    users = list(map(lambda user: user.serialize(), all_users))
    return jsonify(users), 200

@app.route("/user/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Missing name or email"}), 400

    user = User(
        name=data.get("name"),
        email=data.get("email")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("get_user"))

    return render_template("user/delete.html", user=user)

# Character endpoints
@app.route('/character', methods=['GET'])
def get_character():
    all_characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), all_characters))
    return jsonify(characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    
    if character is None:
        return jsonify({"error": "Character not found"}), 404

    return jsonify(character.serialize()), 200

@app.route("/character/", methods=["POST"])
def create_character():
    data = request.get_json()
    if not data.get("name") or not data.get("description") or not data.get("race"):
        return jsonify({"error": "Missing character data"}), 400

    character = Character(
        name=data.get("name"),
        description=data.get("description"),
        race=data.get("race")
    )
    
    db.session.add(character)
    db.session.commit()
    return jsonify(character.serialize()), 200

@app.route("/character/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Character.query.get(character_id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    db.session.delete(character)
    db.session.commit()
    
    return jsonify({"message": "Character deleted successfully"}), 200

# Planet endpoints
@app.route('/planet', methods=['GET'])
def get_planet():
    all_planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), all_planets))
    return jsonify(planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200

@app.route("/planet/", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data.get("name") or not data.get("climate") or not data.get("terrain"):
        return jsonify({"error": "Missing planet data"}), 400

    planet = Planet(
        name=data.get("name"),
        climate=data.get("climate"),
        terrain=data.get("terrain")
    )
    
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route("/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    
    return jsonify({"message": "Planet deleted successfully"}), 200

# Vehicle endpoints
@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    all_vehicles = Vehicle.query.all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(), all_vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(vehicle.serialize()), 200

@app.route("/vehicle/", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    if not data.get("name") or not data.get("model") or not data.get("manufacturer") or not data.get("cost_in_credits"):
        return jsonify({"error": "Missing vehicle data"}), 400

    vehicle = Vehicle(
        name=data.get("name"),
        model=data.get("model"),
        manufacturer=data.get("manufacturer"),
        cost_in_credits=data.get("cost_in_credits")
    )
    
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route("/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)

    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404

    db.session.delete(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle deleted successfully"}), 200

# Favorites endpoints
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    favorites = [favorite.serialize() for favorite in user.favorites]
    return jsonify(favorites), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        return jsonify({"message": "User or Planet not found"}), 404

    favorite = Favourite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    person = Character.query.get(people_id)

    if not user or not person:
        return jsonify({"message": "User or Character not found"}), 404

    favorite = Favourite(user_id=user_id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    favorite = Favourite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_people(people_id):
    user_id = request.json.get('user_id')
    favorite = Favourite.query.filter_by(user_id=user_id, character_id=people_id).first()

    if not favorite:
        return jsonify({"message": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite removed successfully"}), 200

# Run the app
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
