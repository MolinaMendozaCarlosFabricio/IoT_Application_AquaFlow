from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from src.ui.MainView import MainView
from config import Config
from src.index import Loop
import threading

def main():
    try:
        configManager = Config()
        print("Configuración Obtenida")
    except Exception as e:
        print("Error al obtener configuración:", e)
        configManager = None

    try:
        dbManager = LocalDB()
        print("Base de datos iniciada")
    except Exception as e:
        print("Error al iniciar base de datos:", e)
        dbManager = None

    try:
        amqpManager = PublisherAMQP(configManager)
        print("Conexión AMQP establecida")
    except Exception as e:
        print("Error al conectarse con servidor AMQP:", e)
        amqpManager = None

    try:
        digitalSensorManager = DigitalSensors()
        print("Sensores Digitales inicializados")
    except Exception as e:
        print("Error al conectar con los sensores digitales:", e)
        digitalSensorManager = None

    try:
        analogicSensorManager = AnalogicSensors()
        print("Sensores analógicos inicializados")
    except Exception as e:
        print("Error al conectar con los sensores analógicos:", e)
        analogicSensorManager = None

    try:
        mainView = MainView()
        print("Vista inicializada")
    except Exception as e:
        print("Error al iniciar vista:", e)
        return

    hilo_loop = threading.Thread(target=system_loop, args=(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView))
    hilo_loop.daemon = True
    hilo_loop.start()

    mainView.mainloop()

    dbManager.closeDB()
    amqpManager.closeConnection()

def system_loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView):
    while mainView.verifyRunning():
        Loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView)

if __name__ == "__main__":
    main()