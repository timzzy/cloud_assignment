import mysql.connector

class GatekeeperApp:
    def __init__(self, manager_host, manager_user, manager_password, manager_database):
        self.manager_host = manager_host
        self.manager_user = manager_user
        self.manager_password = manager_password
        self.manager_database = manager_database
        self.connection = None

    def connect_to_manager(self):
        self.connection = mysql.connector.connect(
            host=self.manager_host,
            user=self.manager_user,
            password=self.manager_password,
            database=self.manager_database
        )

    def send_request(self, query):
        if not self.connection.is_connected():
            self.connect_to_manager()

        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()


if __name__ == "__main__":
    manager_host = "172.31.83.148"
    manager_user = "testuser"
    manager_password = ""
    manager_database = "ndb"

    gatekeeper_app = GatekeeperApp(manager_host, manager_user, manager_password, manager_database)

    query = "SELECT * FROM sbtest1;"

    try:
        gatekeeper_app.connect_to_manager()
        result = gatekeeper_app.send_request(query)
        print("Result:", result)
    finally:
        gatekeeper_app.close_connection()
