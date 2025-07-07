# opcua_client.py
from opcua import Client

class OPCBoilerClient:
    def __init__(self, endpoint="opc.tcp://localhost:4840/freeopcua/server/"):
        self.client = Client(endpoint)
        self.nodes = {}

    def connect(self):
        self.client.connect()
        root = self.client.get_objects_node()
        boiler = root.get_child(["2:Boiler"])  # ❌ не находит

        # ✅ Правильно:
        boiler = self.client.get_root_node().get_child(["0:Objects", "2:Boiler"])

        for variable in boiler.get_variables():
            name = variable.get_display_name().Text
            self.nodes[name] = variable

    def disconnect(self):
        self.client.disconnect()

    def get_value(self, tag_name):
        return self.nodes[tag_name].get_value()

    def set_value(self, tag_name, value):
        self.nodes[tag_name].set_value(value)