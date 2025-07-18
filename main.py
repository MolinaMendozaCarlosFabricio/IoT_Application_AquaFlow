from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from config import Config

try:
    configManager = Config()
    dbManager = LocalDB()
    amqpManager = PublisherAMQP(configManager)
    digitalSensorManager = DigitalSensors()
    analogicSensorManager = AnalogicSensors()
except Exception as e:
    print("Error al iniciar dependencias:", e)

deviceInfo = dbManager.getDeviceInfo()