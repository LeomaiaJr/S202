from database import Database
from helper.writeAJson import writeAJson

class Pokedex():
    
    def __init__(self, database: Database):
        self.db = database
        
    def getPokemonByName(self, name: str):
        pokemon =  self.db.collection.find({"name": name})
        writeAJson(pokemon, "pokemon_by_name")
        
    def getPokemonByType(self, types: list):
        pokemon =  self.db.collection.find({"type": {"$in": types}})
        writeAJson(pokemon, "pokemon_by_type")
        
    def getGhostPokemon(self):
        pokemon =  self.db.collection.find({"type": "Ghost"})
        writeAJson(pokemon, "ghost_pokemon")
        
    def getFireWeakness(self):
        pokemon =  self.db.collection.find({"weaknesses": "Fire"})
        writeAJson(pokemon, "fire_weaknesses")
        
    def getWaterWeaknessesOrType(self):
        pokemon =  self.db.collection.find({"$or": [{"type":"Water"},{"weaknesses": "Water"}]})
        writeAJson(pokemon, "water_weaknesses_or_type")
        