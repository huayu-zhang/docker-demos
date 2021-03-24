import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import mysql.connector


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for record in result:
                print("Created friendship between: {p1}, {p2}".format(
                    p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for record in result:
                print("Found person: {record}".format(record=record))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [record["name"] for record in result]


def insert_friend_sql(host, name1, name2):
    mydb = mysql.connector.connect(
        host=host,
        user="root",
        password="my-secret-pw",
        database="mydatabase"
    )

    sql = "INSERT INTO friends (name1, name2) VALUES (%s, %s)"
    val = (name1, name2)

    cursor = mydb.cursor()
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()


def main():
    uri = 'neo4j://localhost:7687/'

    name1 = input("enter a name: ")
    name2 = input("enter another name: ")

    app = App(uri=uri, user='neo4j', password='password')
    app.create_friendship(person1_name=name1, person2_name=name2)
    app.close()

    mysql_host = 'localhost'
    insert_friend_sql(host=mysql_host, name1=name1, name2=name2)


if __name__ == '__main__':
    main()

