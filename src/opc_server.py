from opcua import Server

class OPCBoilerServer:
    def __init__(self, model, endpoint="opc.tcp://0.0.0.0:4840/freeopcua/server/"):
        self.model = model
        self.server = Server()
        self.server.set_endpoint(endpoint)

        uri = "http://example.org/boiler/"
        self.idx = self.server.register_namespace(uri)

        self._setup_nodes()

    def _setup_nodes(self):
        boiler = self.server.nodes.objects.add_object(self.idx, "Boiler")

        # Управляющие клапаны
        self.valve_hot_node = boiler.add_variable(self.idx, "ValveHotIn", self.model.valve_hot)
        self.valve_cold_node = boiler.add_variable(self.idx, "ValveColdIn", self.model.valve_cold)
        self.valve_out_node = boiler.add_variable(self.idx, "ValveOut", self.model.valve_out)

        for n in [self.valve_hot_node, self.valve_cold_node, self.valve_out_node]:
            n.set_writable()

        # Входные температуры (не изменяются)
        self.input_temp_hot = boiler.add_variable(self.idx, "InputTempHot", self.model.temp_hot)
        self.input_temp_cold = boiler.add_variable(self.idx, "InputTempCold", self.model.temp_cold)

        # Выходные переменные
        self.output_temp = boiler.add_variable(self.idx, "OutputTemp", self.model.get_temperature())
        self.level = boiler.add_variable(self.idx, "WaterLevel", self.model.get_level_percent())

    def update_from_nodes(self):
        self.model.valve_hot = self.valve_hot_node.get_value()
        self.model.valve_cold = self.valve_cold_node.get_value()
        self.model.valve_out = self.valve_out_node.get_value()

    def update_outputs(self):
        self.output_temp.set_value(round(self.model.get_temperature(), 2))
        self.level.set_value(round(self.model.get_level_percent(), 2))

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()
