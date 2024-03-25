from database import Database
from bookModel import BookModel

db = Database(database="relatorio_5", collection="livros")
bookModel = BookModel(database=db)

# Comandos utilizados para testar o CRUD
# 1- Create
# bookModel.create_book("Clean Code", "Robert C. Martin", 2008, 31.0)

# 2- Read
# bookModel.read_book_by_id("6601b651f5cd9d1c7fd818fa")

# 3- Update
# bookModel.update_book("6601b651f5cd9d1c7fd818fa", "Clean Code", "Robert C. Martin", 2008, 31.0)

# 4- Delete
# bookModel.delete_book("6601b651f5cd9d1c7fd818fa")

while True:
    print("1: Create")
    print("2: Read")
    print("3: Update")
    print("4: Delete")
    print("5: Sair")

    opcao = int(input("Escolha uma opção: "))
    if opcao == 1:
        titulo = input("Digite o titulo: ")
        autor = input("Digite o autor: ")
        ano = int(input("Digite o ano: "))
        preco = float(input("Digite o preco: "))
        bookModel.create_book(titulo, autor, ano, preco)
    elif opcao == 2:
        id = input("Digite o id: ")
        bookModel.read_book_by_id(id)
    elif opcao == 3:
        id = input("Digite o id: ")
        titulo = input("Digite o titulo: ")
        autor = input("Digite o autor: ")
        ano = int(input("Digite o ano: "))
        preco = float(input("Digite o preco: "))
        bookModel.update_book(id, titulo, autor, ano, preco)
    elif opcao == 4:
        id = input("Digite o id: ")
        bookModel.delete_book(id)
    elif opcao == 5:
        break
    else:
        print("Opção inválida")
    print("\n\n")
