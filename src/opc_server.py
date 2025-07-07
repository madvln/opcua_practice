from opcua import Server
from opc_tags import TAGS

class OPCBoilerServer:
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4840/freeopcua/server/"):
        self.server = Server()
        self.server.set_endpoint(endpoint)
        uri = "http://example.org/boiler/"
        self.idx = self.server.register_namespace(uri)
        self.nodes = {}
        self._setup_nodes()

    def _setup_nodes(self):
        boiler = self.server.nodes.objects.add_object(self.idx, "Boiler")

        for tag_name, props in TAGS.items():
            node = boiler.add_variable(self.idx, tag_name, props["initial"])
            if props.get("writable", False):
                node.set_writable()
            self.nodes[tag_name] = node

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def get_value(self, name):
        return self.nodes[name].get_value()

    def set_value(self, name, value):
        self.nodes[name].set_value(value)