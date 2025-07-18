import time
from opc_server import OPCBoilerServer

if __name__ == "__main__":
    server = OPCBoilerServer()  # Универсальный OPC сервер без модели
    try:
        server.start()
        print("✅ OPC UA сервер запущен")
        while True:
            time.sleep(1)  # Держим процесс живым
    except KeyboardInterrupt:
        print("🛑 Остановка сервера...")
    finally:
        server.stop()
        print("🔌 Сервер остановлен")