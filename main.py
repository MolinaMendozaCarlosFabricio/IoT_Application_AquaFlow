from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from src.ui.MainView import MainView
from config import Config
from src.index import Loop
import threading

try:
    configManager = Config()
    dbManager = LocalDB()
    amqpManager = PublisherAMQP(configManager)
    digitalSensorManager = DigitalSensors()
    analogicSensorManager = AnalogicSensors()
    mainView = MainView()
except Exception as e:
    print("Error al iniciar dependencias:", e)

runing = True
deviceInfo = dbManager.getDeviceInfo()
hilo_ui = threading.Thread(target=mainView.mainloop)
hilo_ui.daemon = True
hilo_ui.start()

while runing:
    Loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView)
    runing = mainView.verifyRunning()
# Cerrar las conexiones con dependencias al finalizar
dbManager.closeDB()
amqpManager.closeConnection()