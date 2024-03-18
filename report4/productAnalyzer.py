from database import Database
from helper.writeAJson import writeAJson

db = Database(database="mercado", collection="compras")


class ProductAnalyzer:

    def __init__(self, database: Database):
        self.db = database

    def totalVendasDoDia(self):
        result = self.db.collection.aggregate(
            [{"$group": {"_id": "$data_compra", "total": {"$count": {}}}}]
        )
        writeAJson(result, "total_vendas_dia")

    def produtosEmMaisDeUmaCompra(self):
        result = db.collection.aggregate(
            [
                {"$unwind": "$produtos"},
                {"$group": {"_id": "$produtos.descricao", "total": {"$count": {}}}},
            ]
        )
        writeAJson(result, "produtos_mais_de_uma_compra")

    def produtoMaisVendido(self):
        result = db.collection.aggregate(
            [
                {"$unwind": "$produtos"},
                {
                    "$group": {
                        "_id": "$produtos.descricao",
                        "total": {"$sum": "$produtos.quantidade"},
                    }
                },
                {"$sort": {"total": -1}},
                {"$limit": 1},
            ]
        )
        writeAJson(result, "produto_mais_vendido")

    def clienteMaisGasto(self):
        result = db.collection.aggregate(
            [
                {"$unwind": "$produtos"},
                {
                    "$group": {
                        "_id": "$cliente_id",
                        "total": {
                            "$sum": {
                                "$multiply": ["$produtos.quantidade", "$produtos.preco"]
                            }
                        },
                    }
                },
                {"$sort": {"total": -1}},
                {"$limit": 1},
            ]
        )
        writeAJson(result, "cliente_maior_gasto")
