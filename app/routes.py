from app import db
from app.models.planet import Planet
from flask import Blueprint,jsonify, make_response,request,abort

#create Planet Class
# class Planet:
#     def __init__(self,id,name,description,temp):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.temp = temp

# #what is the purpose of this function
#     def make_planet_dict(self):
#         return dict(
#             id = self.id,
#             name = self.name,
#             description = self.description,
#             temp = self.temp
#         )
    
# #create list of Planet instances:
planets = [
    # Planet(5,"Jupiter","fifth planet from the Sun","-166F"), 
    # Planet(6,"Saturn","sixth planet from the Sun","-285F"),
    # Planet(7,"Uranus","seventh planet from the Sun","-353F"),
    # Planet(8,"Neptune","eigth planet from the Sun","-373F"),
    # Planet(9,"Pluto","ninth planet from the Sun","-387F")
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


#WAVE 3
#send a request with new valid `planet` data and get a success response, so that 
# #I know the API saved the planet data
@planets_bp.route("",methods = ["POST"])
def create_planet():
    request_body = request.get_json()
    print(request_body)
    new_planet = Planet(
        # id=request_body["id"],
        name=request_body["name"],
        description=request_body["description"],
        temp=request_body["temp"])

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created",201)

#get all existing `planets`, so that I can see a list of planets, with their 
#`id`, `name`, `description`, and other data of the `planet`.
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