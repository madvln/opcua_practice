import time
from boiler_model import BoilerModel
from opc_server import OPCBoilerServer

if __name__ == "__main__":
    model = BoilerModel()
    server = OPCBoilerServer(model)

    try:
        server.start()
        print("✅ OPC UA сервер запущен")

        while True:
            server.update_from_nodes()
            model.step()
            server.update_outputs()
            time.sleep(1)

    except KeyboardInterrupt:
        print("🛑 Остановка сервера...")
    finally:
        server.stop()
        print("🔌 Сервер остановлен")
