from app import db
from app.models.planet import Planet
from flask import Blueprint,jsonify, make_response,request,abort

#CREATE BP/ENDPOINT
planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

# #HELPER FUNCTION
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"},400))
    
    planet = Planet.query.get(planet_id)

    if not planet:
        abort(make_response({"message":f"planet {planet_id} invalid"},400))
    
    return planet 

#WAVE 1
#create endpoint:receive a list of planets with details
@planets_bp.route("", methods=["GET"])
def handle_planets():
    planets = Planet.query.all()
    planet_list = [] 
    
    for planet in planets:
        planet_list.append(planet.make_planet_dict())
    
    return jsonify(planet_list),200


#WAVE 2
#create endpoint: READ: receive one particular planet with info
@planets_bp.route("<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_planet(planet_id)
    
    return planet.make_dict(),200


#WAVE 3
#send request with new valid `planet` data/get a success response: API saved the planet data
@planets_bp.route("",methods = ["POST"])
def create_planet():
    if request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body or "description" not in request_body or "temp" not in request_body:
            return make_response("Invalid Request",400)
        
        new_planet = Planet(
            # id=request_body["id"],
            name=request_body["name"],
            description=request_body["description"],
            temp=request_body["temp"])

        db.session.add(new_planet)
        db.session.commit()

        return make_response(f"Planet {new_planet.name} successfully created",201)

#get all existing `planets`:return list of planets:id/name/description/etc
@planets_bp.route("",methods=["GET"])
def read_all_planets():
    planets = Planet.query.all()
    planets_list = []

    for planet in planets:
        planets_list.append(dict(
            id = planet.id,   
            name = planet.name,
            description = planet.description,
            temp = planet.temp
        ))
    return jsonify(planets_list)

#WAVE4 
#REQUEST To get one existing `planet`, see the `id`, `name`, `description`,ETC
@planets_bp.route("<planet_id>",methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "temp":planet.temp
    }


# #REQUEST to update one existing `planet, get a success response: API updated the `planet` data.
@planets_bp.route("<planet_id>",methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.temp = request_body["temp"]

    db.session.commit()

    return make_response(f"Planet #{planet_id} successfully created")

# #REQUEST TO delete one existing `planet`,get a success response:API deleted the `planet` data
#         #endpoints respond:`404` for non-existing planets/`400` for invalid `planet_id`
@planets_bp.route("<planet_id>",methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet_id} successfully deleted"),200