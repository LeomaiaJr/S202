from database import Database
from helper.writeAJson import writeAJson
from pokedex import Pokedex

db = Database(database="pokedex", collection="pokemons")
pokedex = Pokedex(db)

pokedex.getPokemonByName("Dragonite")
pokedex.getPokemonByType(["Psychic", "Fairy"])
pokedex.getGhostPokemon()
pokedex.getFireWeakness()
pokedex.getWaterWeaknessesOrType()