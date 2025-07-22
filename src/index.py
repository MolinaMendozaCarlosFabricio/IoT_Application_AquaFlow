from src.services.ReadAllData import GetSensorsData
import time

def Loop(analogicSensors, digitalSensors, dbManager, publisher, mainView):
    valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor = GetSensorsData(
        analogicSensors, digitalSensors, dbManager, publisher
    )
    mainView.showMeasurements(valueTurbiditySensor, valueTdsSensor, valuepHSensor, valueTempSensor)
    
    # Lo último que se debe de ejecutar
    time.sleep(10)