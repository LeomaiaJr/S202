from database import Database


class TeacherCRUD:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name, ano_nasc, cpf):
        query = """
        CREATE (:Teacher {name: $name, ano_nasc: $ano_nasc, cpf: $cpf})
        """
        parameters = {"name": name, "ano_nasc": ano_nasc, "cpf": cpf}
        self.db.execute_query(query, parameters)
        print(f"Teacher '{name}' foi criado.")

    def read(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        RETURN t.name AS name, t.ano_nasc AS ano_nasc, t.cpf AS cpf
        """
        parameters = {"name": name}
        result = self.db.execute_query(query, parameters)
        if result:
            return result[0]
        else:
            print(f"Teacher '{name}' nao encontrado")
            return None

    def delete(self, name):
        query = """
        MATCH (t:Teacher {name: $name})
        DELETE t
        """
        parameters = {"name": name}
        self.db.execute_query(query, parameters)
        print(f"Teacher '{name}' deletado.")

    def update(self, name, newCpf):
        query = """
        MATCH (t:Teacher {name: $name})
        SET t.cpf = $newCpf
        """
        parameters = {"name": name, "newCpf": newCpf}
        self.db.execute_query(query, parameters)
        print(f"Teacher '{name}' atualizado com novo CPF '{newCpf}'.")


class CLI:
    def __init__(self):
        URI = "bolt://localhost:7687"
        USER = "neo4j"
        PASSWORD = "password"
        self.db = Database(URI, USER, PASSWORD)
        self.teacher_crud = TeacherCRUD(self.db)

    def run(self):
        while True:
            print("\n1. Criar Teacher")
            print("2. Ler Teacher")
            print("3. Atualizar Teacher")
            print("4. Deletar Teacher")
            print("5. Sair")
            choice = input("Digite a opcao: ")

            if choice == "1":
                name = input("Digite o nome: ")
                ano_nasc = int(input("Digite o ano do nascimento: "))
                cpf = input("Digite o CPF: ")
                self.teacher_crud.create(name, ano_nasc, cpf)
            elif choice == "2":
                name = input("Digite o nome: ")
                teacher = self.teacher_crud.read(name)
                if teacher:
                    print(teacher)
            elif choice == "3":
                name = input("Digite o nome: ")
                newCpf = input("Digite o novo CPF: ")
                self.teacher_crud.update(name, newCpf)
            elif choice == "4":
                name = input("Digite o nome: ")
                self.teacher_crud.delete(name)
            elif choice == "5":
                self.db.close()
                print("Saindo...")
                break
            else:
                print("Opcao invalida")
