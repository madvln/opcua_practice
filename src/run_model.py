import time
from boiler_model import BoilerModel
from opcua_client import OPCBoilerClient

if __name__ == "__main__":
    model = BoilerModel()
    client = OPCBoilerClient()

    try:
        client.connect()
        print("🎛️ OPC UA клиент подключен")

        # ⏱️ Устанавливаем запуск моделирования
        client.set_value("StartSimulation", True)
        print("🚀 Моделирование запущено (StartSimulation = True)")

        # Инициализируем задвижки и записываем их в OPC UA
        model.valve_hot = 0.5
        model.valve_cold = 0.5
        model.valve_out = 1

        client.set_value("ValveHotIn", model.valve_hot)
        client.set_value("ValveColdIn", model.valve_cold)
        client.set_value("ValveOut", model.valve_out)

        while True:
            if not client.get_value("StartSimulation"):
                print("⏸ Ожидание запуска моделирования (StartSimulation = False)")
                time.sleep(1)
                continue
            
            # Считываем текущие значения задвижек с OPC UA
            model.valve_hot = client.get_value("ValveHotIn")
            model.valve_cold = client.get_value("ValveColdIn")
            model.valve_out = client.get_value("ValveOut")

            model.temp_hot = 80.0
            model.temp_cold = 20.0
    
            model.step()

            client.set_value("InputTempHot", model.temp_hot)
            client.set_value("InputTempCold", model.temp_cold)
            client.set_value("OutputTemp", model.get_temperature())
            client.set_value("WaterLevel", model.get_level_percent())

            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Остановка модели...")
    finally:
        client.set_value("StartSimulation", False)  # 👈 Остановить по завершению
        client.disconnect()
        print("🔌 Клиент отключён")