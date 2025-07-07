from opcua import Client
import time

client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()
print("🔍 Клиент подключен")

boiler = client.get_root_node().get_child(["0:Objects", "2:Boiler"])

def get(tag):
    return boiler.get_child(f"2:{tag}").get_value()

while True:
    print(f"🌡️ Горячая: {get('InputTempHot')} | Холодная: {get('InputTempCold')} | "
          f"Выход: {get('OutputTemp')} | Уровень: {get('WaterLevel')} | "
          f"Вент. Г: {get('ValveHotIn')} | Вент. Х: {get('ValveColdIn')} | Вент. Вых: {get('ValveOut')}")
    time.sleep(2)