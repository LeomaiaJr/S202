import random
import threading
import time
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["bancoiot"]
sensores = db["sensores"]

sens = ["Temperature1", "Temperature2", "Temperature3"]
threads = []


def initializeDatabase():
    if sensores.count_documents({}) == 0:
        for sensor in sens:
            sensores.insert_one(
                {
                    "nomeSensor": sensor,
                    "valorSensor": 0,
                    "sensorAlarmado": False,
                }
            )
    else:
        sensores.update_many({}, {"$set": {"valorSensor": 0, "sensorAlarmado": False}})


def generateTemp(sensor):
    while True:
        temperatura = random.randint(30, 40)
        print(f"Sensor {sensor}: {temperatura} °C")

        sensores.update_one(
            {"nomeSensor": sensor}, {"$set": {"valorSensor": temperatura}}
        )

        if temperatura > 38:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {sensor}!")
            sensores.update_one(
                {"nomeSensor": sensor}, {"$set": {"sensorAlarmado": True}}
            )
            break

        time.sleep(1)


initializeDatabase()

for sensor in sens:
    thread = threading.Thread(target=generateTemp, args=(sensor,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
