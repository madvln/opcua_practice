from flask import Flask, render_template, request, jsonify
from opcua import Client

app = Flask(__name__)

# Подключение к OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

boiler = client.get_root_node().get_child(["0:Objects", "2:Boiler"])

nodes = {
    "InputTempHot": boiler.get_child("2:InputTempHot"),
    "InputTempCold": boiler.get_child("2:InputTempCold"),
    "OutputTemp": boiler.get_child("2:OutputTemp"),
    "WaterLevel": boiler.get_child("2:WaterLevel"),
    "ValveHotIn": boiler.get_child("2:ValveHotIn"),
    "ValveColdIn": boiler.get_child("2:ValveColdIn"),
    "ValveOut": boiler.get_child("2:ValveOut"),
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    try:
        return jsonify({
            "input_temp_hot": round(nodes["InputTempHot"].get_value(), 1),
            "input_temp_cold": round(nodes["InputTempCold"].get_value(), 1),
            "output_temp": round(nodes["OutputTemp"].get_value(), 1),
            "water_level": round(nodes["WaterLevel"].get_value(), 1),
            "valve_hot": round(nodes["ValveHotIn"].get_value() * 100),
            "valve_cold": round(nodes["ValveColdIn"].get_value() * 100),
            "valve_out": round(nodes["ValveOut"].get_value() * 100),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set_valve", methods=["POST"])
def set_valve():
    try:
        name = request.json.get("name")
        value = float(request.json.get("value")) / 100  # ожидается 0–1
        if name in ["ValveHotIn", "ValveColdIn", "ValveOut"]:
            nodes[name].set_value(value)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"error": "Invalid valve name"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)