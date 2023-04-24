from flask import Blueprint, jsonify

#create Planet Class
class Planet:
    def __init__(self,id,name,description,temp):
        self.id = id
        self.name = name
        self.description = description
        self.temp = temp

#create list of Planet instances:
planets = [
    Planet(5,"Jupiter","fifth planet from the Sun","-166F"), 
    Planet(6,"Saturn","sixth planet from the Sun","-285F"),
    Planet(7,"Uranus","seventh planet from the Sun","-353F"),
    Planet(8,"Neptune","eigth planet from the Sun","-373F"),
    Planet(9,"Pluto","ninth planet from the Sun","-387F")
]
#create endpoint - READ: receive a list of planets with details
planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("/<planet_id>", methods=["GET"])
def handle_planets(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        return {"message":f"planet {planet_id} invalid"},400

    for planet in planets:
        if planet.id == planet_id:
            return {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "temp": planet.temp
            }
    
    return {"message": f"planet {planet_id} not found"},404
