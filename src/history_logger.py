from opcua import Client
import sqlite3
import time
import datetime

DB_FILE = "data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            input_temp_hot REAL NOT NULL,
            input_temp_cold REAL NOT NULL,
            valve_hot REAL NOT NULL,
            valve_cold REAL NOT NULL,
            valve_out REAL NOT NULL,
            output_temp REAL NOT NULL,
            water_level REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_to_db(in_hot, in_cold, v_hot, v_cold, v_out, out_temp, level):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history 
        (timestamp, input_temp_hot, input_temp_cold, valve_hot, valve_cold, valve_out, output_temp, water_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        in_hot, in_cold,
        v_hot, v_cold, v_out,
        out_temp, level
    ))
    conn.commit()
    conn.close()

def main():
    init_db()
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    try:
        client.connect()
        print("✅ Исторический логгер подключён к OPC UA")

        boiler = client.get_root_node().get_child(["0:Objects", "2:Boiler"])

        input_temp_hot = boiler.get_child("2:InputTempHot")
        input_temp_cold = boiler.get_child("2:InputTempCold")

        valve_hot = boiler.get_child("2:ValveHotIn")
        valve_cold = boiler.get_child("2:ValveColdIn")
        valve_out = boiler.get_child("2:ValveOut")

        output_temp = boiler.get_child("2:OutputTemp")
        water_level = boiler.get_child("2:WaterLevel")

        while True:
            vals = {
                "in_hot": input_temp_hot.get_value(),
                "in_cold": input_temp_cold.get_value(),
                "v_hot": valve_hot.get_value(),
                "v_cold": valve_cold.get_value(),
                "v_out": valve_out.get_value(),
                "out_temp": output_temp.get_value(),
                "level": water_level.get_value()
            }

            log_to_db(**vals)

            print(f"💾 Запись: T_in_hot={vals['in_hot']:.1f}°C, T_in_cold={vals['in_cold']:.1f}°C, "
                  f"V_hot={vals['v_hot']:.2f}, V_cold={vals['v_cold']:.2f}, V_out={vals['v_out']:.2f}, "
                  f"T_out={vals['out_temp']:.1f}°C, Level={vals['level']:.1f}%")

            time.sleep(5)

    except Exception as e:
        print("Ошибка логгера:", e)
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
