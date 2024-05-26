from database import Database

# Usando banco local no docker
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password"

db = Database(URI, USER, PASSWORD)


def get_teacher_by_name(name):
    query = """
    MATCH (t:Teacher {name: $name})
    RETURN t.ano_nasc AS ano_nasc, t.cpf AS cpf
    """
    parameters = {"name": name}
    result = db.execute_query(query, parameters)
    return result


def get_teachers_by_name_starting_with(letter):
    query = """
    MATCH (t:Teacher)
    WHERE t.name STARTS WITH $letter
    RETURN t.name AS name, t.cpf AS cpf
    """
    parameters = {"letter": letter}
    result = db.execute_query(query, parameters)
    return result


def get_all_cities():
    query = """
    MATCH (c:City)
    RETURN c.name AS name
    """
    result = db.execute_query(query)
    return result


def get_schools_by_number_range(min_number, max_number):
    query = """
    MATCH (s:School)
    WHERE s.number >= $min_number AND s.number <= $max_number
    RETURN s.name AS name, s.address AS address, s.number AS number
    """
    parameters = {"min_number": min_number, "max_number": max_number}
    result = db.execute_query(query, parameters)
    return result


def get_oldest_and_youngest_teacher_birth_year():
    query = """
    MATCH (t:Teacher)
    RETURN min(t.ano_nasc) AS youngest, max(t.ano_nasc) AS oldest
    """
    result = db.execute_query(query)
    return result


def get_average_population():
    query = """
    MATCH (c:City)
    RETURN avg(c.population) AS average_population
    """
    result = db.execute_query(query)
    return result


def get_city_by_cep(cep):
    query = """
    MATCH (c:City {cep: $cep})
    RETURN replace(c.name, 'a', 'A') AS name
    """
    parameters = {"cep": cep}
    result = db.execute_query(query, parameters)
    return result


def get_char_from_third_letter_of_teacher_names():
    query = """
    MATCH (t:Teacher)
    RETURN substring(t.name, 2, 1) AS char
    """
    result = db.execute_query(query)
    return result


renzo = get_teacher_by_name("Renzo")
print("Professor Renzo:", renzo)

teachers_m = get_teachers_by_name_starting_with("M")
print("Professores com nome começando com 'M':", teachers_m)

cities = get_all_cities()
print("Cidades:", cities)

schools = get_schools_by_number_range(150, 550)
print("Escolas com número entre 150 e 550:", schools)

birth_years = get_oldest_and_youngest_teacher_birth_year()
print("Ano de nascimento do professor mais jovem e mais velho:", birth_years)

average_population = get_average_population()
print("Média aritmética da população das cidades", average_population)

city_cep = get_city_by_cep("37540-000")
print("Cidade com CEP '37540-000' com 'a' substituído por A:", city_cep)

third_letter_chars = get_char_from_third_letter_of_teacher_names()
print("Caractere a partir da 3 letra dos nomes dos professores:", third_letter_chars)

db.close()
