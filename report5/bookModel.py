from pymongo import MongoClient
from bson.objectid import ObjectId

class BookModel:
    def __init__(self, database):
        self.db = database

    def create_book(self, titulo: str, autor: str, ano: int, preco: float):
        try:
            res = self.db.collection.insert_one({
                "titulo": titulo,
                "autor": autor,
                "ano": ano,
                "preco": preco
            })
            print(f"Livro criado com id:{res.inserted_id}")
            return res.inserted_id
        except Exception as e:
            print(f"Erro ao criar livro: {e}")
            return None

    def read_book_by_id(self, id: str):
        try:
            res = self.db.collection.find_one({"_id": ObjectId(id)})
            print(f"Livro encontrado:{res}")
            return res
        except Exception as e:
            print(f"Erro ao buscar livro: {e}")
            return None
    
    def update_book(self, id: str, titulo: str, autor: str, ano: int, preco: float):
        try:
            res = self.db.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {
                    "titulo": titulo,
                    "autor": autor,
                    "ano": ano,
                    "preco": preco
                }}
            )
            print(f"Livro atualizado: {res.modified_count} documento(s) modificado(s)")
            return res.modified_count
        except Exception as e:
            print(f"Erro ao atualizar livro: {e}")
            return None

    def delete_book(self, id: str):
        try:
            res = self.db.collection.delete_one({"_id": ObjectId(id)})
            print(f"Livro deletado: {res.deleted_count} documento(s) deletado(s)")
            return res.deleted_count
        except Exception as e:
            print(f"Erro ao deletar livro: {e}")
            return None