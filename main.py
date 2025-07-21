from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from config import Config
from src.index import Loop

try:
    configManager = Config()
    dbManager = LocalDB()
    amqpManager = PublisherAMQP(configManager)
    digitalSensorManager = DigitalSensors()
    analogicSensorManager = AnalogicSensors()
except Exception as e:
    print("Error al iniciar dependencias:", e)

runing = True
deviceInfo = dbManager.getDeviceInfo()

while runing:
    Loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager)
# Cerrar las conexiones con dependencias al finalizar
dbManager.closeDB()
amqpManager.closeConnection()