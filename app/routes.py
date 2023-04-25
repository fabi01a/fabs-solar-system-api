from flask import Blueprint, jsonify, abort, make_response

#create Planet Class
class Planet:
    def __init__(self,id,name,description,temp):
        self.id = id
        self.name = name
        self.description = description
        self.temp = temp

#what is the purpose of this function
    def make_planet_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            description = self.description,
            temp = self.temp
        )
    
#create list of Planet instances:
planets = [
    Planet(5,"Jupiter","fifth planet from the Sun","-166F"), 
    Planet(6,"Saturn","sixth planet from the Sun","-285F"),
    Planet(7,"Uranus","seventh planet from the Sun","-353F"),
    Planet(8,"Neptune","eigth planet from the Sun","-373F"),
    Planet(9,"Pluto","ninth planet from the Sun","-387F")
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

#Wave 1
#create endpoint - READ: receive a list of planets with details
@planets_bp.route("", methods=["GET"])
def handle_planets():
    planet_list = [] 
    for planet in planets:
        planet_list.append(planet.make_planet_dict())
    return jsonify(planet_list)

# Handle Error responses: 404 response Not Found and any invalid ids get a 400 response Invalid ID
def validate_planets(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"},400))
    
    for planet in planets:
        if planet.id == planet_id:
            return planet
    
    abort(make_response({"message": f"planet {planet_id} not found"},404))


#WAVE 2
#create endpoint: READ: receive one particular planet with info
@planets_bp.route("<planet_id>", methods=["GET"])
def handle_planet(planet_id):
    planet = validate_planets(planet_id)
    return planet.make_planet_dict()
