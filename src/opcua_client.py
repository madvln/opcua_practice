from opcua import Client
import time

client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()
print("🔍 Клиент подключен")

boiler = client.get_root_node().get_child(["0:Objects", "2:Boiler"])
t_hot = boiler.get_child("2:InputTempHot")
t_cold = boiler.get_child("2:InputTempCold")
t_out = boiler.get_child("2:OutputTemp")
level = boiler.get_child("2:WaterLevel")

while True:
    print(f"🌡️ ВходГ: {t_hot.get_value()}°C | ВходХ: {t_cold.get_value()}°C | Выход: {t_out.get_value()}°C | Уровень: {level.get_value()} %")
    time.sleep(2)
