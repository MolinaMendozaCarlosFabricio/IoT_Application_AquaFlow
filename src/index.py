from src.services.ReadAllData import GetSensorsData

def Loop(analogicSensors, digitalSensors, dbManager, publisher):
    valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor = GetSensorsData(
        analogicSensors, digitalSensors, dbManager, publisher
    )