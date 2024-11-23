from py2neo import Graph


class Neo4j:
    def __init__(self):
        # self.url = 'http://localhost:7474/'
        self.url = 'http://82.156.31.125:7474/'
        self.username = 'neo4j'
        self.password = '12345678'
        self.db = None

    def get_db(self, database):
        print(database)
        self.db = Graph(self.url, username=self.username, password=self.password, name=database)
        print(self.db.database.name)
        return self.db

    def close_db(self):
        if self.db is not None:
            self.db.close()
