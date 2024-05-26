from teacher_crud import CLI

cli = CLI()

cli.teacher_crud.create("Chris Lima", 1956, "189.052.396-66")
print(cli.teacher_crud.read("Chris Lima"))
cli.teacher_crud.update("Chris Lima", "162.052.777-77")
print(cli.teacher_crud.read("Chris Lima"))
cli.teacher_crud.delete("Chris Lima")


cli.run()
