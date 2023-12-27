import mysql.connector
import random
import time
from ping3 import ping, verbose_ping

class MySQLProxy:
    def __init__(self, master_host, slave_hosts):
        self.master_host = master_host
        self.slave_hosts = slave_hosts
        self.proxy_instance = None

    def connect(self):
        self.proxy_instance = mysql.connector.connect(
            host=self.master_host,
            user='your_username',
            password='your_password',
            database='your_database'
        )

    def direct_hit(self, query):
        cursor = self.proxy_instance.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def random_forward(self, query):
        slave_host = random.choice(self.slave_hosts)
        slave_instance = mysql.connector.connect(
            host=slave_host,
            user='your_username',
            password='your_password',
            database='your_database'
        )
        cursor = slave_instance.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        slave_instance.close()
        return result

    def customized_forward(self, query):
        ping_times = {}

        for host in self.slave_hosts:
            response_time = ping(host)
            if response_time is not None:
                ping_times[host] = response_time

        # Sort servers based on response time
        sorted_servers = sorted(ping_times.items(), key=lambda x: x[1])

        # Forward request to the server with the least response time
        best_server = sorted_servers[0][0]

        best_instance = mysql.connector.connect(
            host=best_server,
            user='root',
            password='',
            database='NDB'
        )

        cursor = best_instance.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        best_instance.close()
        return result

    def close(self):
        if self.proxy_instance:
            self.proxy_instance.close()

if __name__ == "__main__":
    # Replace the following values with your MySQL configuration
    master_host = "your_master_host"
    slave_hosts = ["slave_host1", "slave_host2", "slave_host3"]

    proxy = MySQLProxy(master_host, slave_hosts)

    # Choose the proxy type: "direct_hit", "random_forward", or "customized_forward"
    proxy_type = "customized_forward"

    # Connect to the proxy instance
    proxy.connect()

    # Example query
    query = "SELECT * FROM your_table;"

    if proxy_type == "direct_hit":
        result = proxy.direct_hit(query)
    elif proxy_type == "random_forward":
        result = proxy.random_forward(query)
    elif proxy_type == "customized_forward":
        result = proxy.customized_forward(query)
    else:
        raise ValueError("Invalid proxy type")

    print("Result:", result)

    # Close the proxy connection
    proxy.close()
