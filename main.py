import json
import datetime
import mysql.connector

class Container:
    def __init__(self, name, cpu, memory_usage, created_at, status, ip_addresses):
        self.name = name
        self.cpu = cpu
        self.memory_usage = memory_usage
        self.created_at = created_at
        self.status = status
        self.ip_addresses = ip_addresses

    @classmethod
    def from_json(cls, json):
        name = json["name"]
        status = json["status"]
        created_at = Container.convert_to_utc_timestamp(json["created_at"])
        cpu, memory_usage, addresses = Container.extract_state(json["state"])
        return cls(name, cpu, memory_usage, created_at, status, addresses)

    @staticmethod
    def convert_to_utc_timestamp (time):
        time_object = datetime.datetime.fromisoformat(time)
        utc_timestamp = time_object.timestamp()
        return utc_timestamp

    @staticmethod
    def get_addresses (network):
        addresses = []
        for key, value in network.items():
            for el2 in value["addresses"]:
                addresses.append(el2["address"])
        return addresses

    @staticmethod
    def extract_state(state):
        if state is None:
            return None, None, None
        if state["cpu"] is not None:
            cpu = state["cpu"]["usage"]
        else:
            cpu = None
        if state["memory"] is not None:
            memory_usage = state["memory"]["usage"]
        else:
            memory_usage = None
        if state["network"] is not None:
            addresses = Container.get_addresses(state["network"])
        else:
            addresses = None
        return cpu, memory_usage, addresses


if __name__ == "__main__":
    with open('sample-data.json') as f:
        data = json.load(f)
    containers = list(map(Container.from_json, data))

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qwerty",
        database="containers_db"
    )
    mycursor = mydb.cursor()

    for container in containers:
        sql = f"INSERT INTO containers_info (name, created_at, status, cpu, memory_usage) VALUES ("\
              f"'{container.name}',"\
              f"{container.created_at}," \
              f"'{container.status}',"\
              f"{'NULL' if container.cpu is None else container.cpu},"\
              f"{'NULL' if container.memory_usage is None else container.memory_usage})"
        mycursor.execute(sql)
        id = mycursor.lastrowid
        if container.ip_addresses is not None:
            for address in container.ip_addresses:
                sql = f"INSERT INTO containers_addresses (container_id, address) VALUES ({id}, '{address}')"
                mycursor.execute(sql)
    mydb.commit()

