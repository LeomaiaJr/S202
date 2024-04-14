from pymongo import MongoClient
import sys
from bson import ObjectId


class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client["av1"]


class MotoristaDAO:
    def __init__(self, db):
        self.db = db

    def create_motorista(self, motorista):
        return self.db.Motoristas.insert_one(motorista.to_dict())

    def read_motoristas(self):
        return self.db.Motoristas.find()

    def read_motorista(self, motorista_id):
        motorista_id = ObjectId(motorista_id)
        return self.db.Motoristas.find_one({"_id": motorista_id})

    def update_motorista(self, motorista_id, motorista):
        motorista_id = ObjectId(motorista_id)
        return self.db.Motoristas.update_one(
            {"_id": motorista_id}, {"$set": motorista.to_dict()}
        )

    def delete_motorista(self, motorista_id):
        motorista_id = ObjectId(motorista_id)
        return self.db.Motoristas.delete_one({"_id": motorista_id})


class Motorista:
    def __init__(self, nota, corridas=[]):
        self.nota = nota
        self.corridas = corridas

    def to_dict(self):
        return {
            "nota": self.nota,
            "corridas": [corrida.to_dict() for corrida in self.corridas],
        }


class Corrida:
    def __init__(self, nota, distancia, valor, passageiro):
        self.nota = nota
        self.distancia = distancia
        self.valor = valor
        self.passageiro = passageiro

    def to_dict(self):
        return {
            "nota": self.nota,
            "distancia": self.distancia,
            "valor": self.valor,
            "passageiro": self.passageiro.to_dict(),
        }


class Passageiro:
    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento

    def to_dict(self):
        return {"nome": self.nome, "documento": self.documento}


class MotoristaCLI:
    def __init__(self, motorista_dao):
        self.motorista_dao = motorista_dao

    def create_motorista(self):
        nome = input("Nome do Passageiro: ")
        documento = input("Documento do Passageiro: ")
        passageiro = Passageiro(nome, documento)
        nota = int(input("Nota da Corrida: "))
        distancia = float(input("Distância da Corrida: "))
        valor = float(input("Valor da Corrida: "))
        corrida = Corrida(nota, distancia, valor, passageiro)
        nota_motorista = int(input("Nota do Motorista: "))
        motorista = Motorista(nota_motorista, [corrida])
        self.motorista_dao.create_motorista(motorista)
        print("Motorista criado com sucesso!")

    def read_motoristas(self):
        motoristas = self.motorista_dao.read_motoristas()
        for motorista in motoristas:
            print("-------Motorista-------")
            print(f"ID do Motorista: {motorista['_id']}")
            print(f"Nota do Motorista: {motorista['nota']}")
            for corrida in motorista["corridas"]:
                print("-------Corrida-------")
                print(f"Nota da Corrida: {corrida['nota']}")
                print(f"Distância da Corrida: {corrida['distancia']}")
                print(f"Valor da Corrida: {corrida['valor']}")
                print(f"Nome do Passageiro: {corrida['passageiro']['nome']}")
                print(f"Documento do Passageiro: {corrida['passageiro']['documento']}")
                print("----------------------")

    def update_motorista(self):
        motorista_id = input("ID do Motorista para atualizar: ")
        motorista = self.motorista_dao.read_motorista(motorista_id)
        if motorista:
            print("Deseja atualizar a nota do motorista? (sim/nao)")
            if input().lower() == "sim":
                nova_nota = int(input("Nova nota do motorista: "))
                motorista["nota"] = nova_nota

            print("Deseja atualizar uma corrida? (sim/nao)")
            if input().lower() == "sim":
                indice = int(input("Índice da corrida para atualizar: "))
                if indice < len(motorista["corridas"]):
                    print("Nova nota da corrida: ")
                    motorista["corridas"][indice]["nota"] = int(input())
                    print("Nova distância da corrida: ")
                    motorista["corridas"][indice]["distancia"] = float(input())
                    print("Novo valor da corrida: ")
                    motorista["corridas"][indice]["valor"] = float(input())

            self.motorista_dao.update_motorista(
                motorista_id, Motorista(motorista["nota"], motorista["corridas"])
            )
            print("Motorista atualizado com sucesso!")
        else:
            print("Motorista não encontrado.")

    def delete_motorista(self):
        motorista_id = input("ID do Motorista para deletar: ")
        motorista = self.motorista_dao.read_motorista(motorista_id)
        if motorista:
            self.motorista_dao.delete_motorista(motorista_id)
            print("Motorista deletado com sucesso!")
        else:
            print("Motorista não encontrado.")

    def menu(self):
        while True:
            print("0. Exit")
            print("1. Create Motorista")
            print("2. Read Motoristas")
            print("3. Update Motorista")
            print("4. Delete Motorista")
            choice = input("Enter choice: ")
            if choice == "1":
                self.create_motorista()
            elif choice == "0":
                sys.exit()
            elif choice == "2":
                self.read_motoristas()
            elif choice == "3":
                self.update_motorista()
            elif choice == "4":
                self.delete_motorista()
            else:
                print("Invalid choice")


if __name__ == "__main__":
    db = Database("mongodb+srv://root:root@cluster0.r8yvx5d.mongodb.net/")
    motorista_dao = MotoristaDAO(db.db)
    cli = MotoristaCLI(motorista_dao)
    cli.menu()
