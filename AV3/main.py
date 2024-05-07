from neo4j import GraphDatabase


class GameDatabase:
    def __init__(self, uri, user, password):

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):

        self.driver.close()

    def create_player(self, name):

        query = "CREATE (p:Player {name: $name}) RETURN id(p)"
        with self.driver.session() as session:
            result = session.run(query, name=name)
            return result.single()[0]

    def update_player(self, player_id, name):

        query = "MATCH (p:Player) WHERE id(p) = $player_id SET p.name = $name RETURN p"
        with self.driver.session() as session:
            session.run(query, player_id=player_id, name=name)

    def get_player(self, player_id):

        query = "MATCH (p:Player) WHERE id(p) = $player_id RETURN p"
        with self.driver.session() as session:
            result = session.run(query, player_id=player_id)
            return result.single()[0]

    def list_players(self):

        query = "MATCH (p:Player) RETURN id(p) as id, p.name as name"
        with self.driver.session() as session:
            results = session.run(query)
            return [{"id": record["id"], "name": record["name"]} for record in results]

    def delete_player(self, player_id):

        query = "MATCH (p:Player) WHERE id(p) = $player_id DETACH DELETE p"
        with self.driver.session() as session:
            session.run(query, player_id=player_id)

    def create_match(self, player1_id, player2_id, result):

        query = """
        MATCH (p1:Player), (p2:Player)
        WHERE id(p1) = $player1_id AND id(p2) = $player2_id
        CREATE (m:Match {result: $result})
        CREATE (p1)-[:PARTICIPATED_IN]->(m)
        CREATE (p2)-[:PARTICIPATED_IN]->(m)
        RETURN id(m)
        """
        with self.driver.session() as session:
            result = session.run(
                query, player1_id=player1_id, player2_id=player2_id, result=result
            )
            return result.single()[0]

    def get_match(self, match_id):

        query = """
        MATCH (m:Match) WHERE id(m) = $match_id
        OPTIONAL MATCH (p:Player)-[:PARTICIPATED_IN]->(m)
        RETURN m, collect(p)
        """
        with self.driver.session() as session:
            result = session.run(query, match_id=match_id)
            record = result.single()
            return {"match": record[0], "players": record[1]}

    def update_match_result(self, match_id, result):

        query = (
            "MATCH (m:Match) WHERE id(m) = $match_id SET m.result = $result RETURN m"
        )
        with self.driver.session() as session:
            session.run(query, match_id=match_id, result=result)

    def delete_match(self, match_id):

        query = "MATCH (m:Match) WHERE id(m) = $match_id DETACH DELETE m"
        with self.driver.session() as session:
            session.run(query, match_id=match_id)

    def get_player_match_history(self, player_id):

        query = """
        MATCH (p:Player)-[:PARTICIPATED_IN]->(m:Match)
        WHERE id(p) = $player_id
        RETURN m
        """
        with self.driver.session() as session:
            results = session.run(query, player_id=player_id)
            return [record["m"] for record in results]


db = GameDatabase("bolt://localhost:7687", "neo4j", "senha")
player1_id = db.create_player("Jogador 1")
player2_id = db.create_player("Jogador 2")
match_id = db.create_match(player1_id, player2_id, "3-1")
db.update_match_result(match_id, "3-2")
print("Lista de jogadores:", db.list_players())
print("Histórico de partidas do Jogador 1:", db.get_player_match_history(player1_id))
print("Detalhes da partida:", db.get_match(match_id))
db.delete_match(match_id)
db.delete_player(player1_id)
db.delete_player(player2_id)
db.close()
