import time

def GetSensorsData (analogicSensors, digitalSensors, dbManager, publisher):
    deviceInfo = dbManager.getDeviceInfo()
    tempSensorInfo = dbManager.getSensor('ds18b20')
    tdsSensorInfo = dbManager.getSensor('tdsSensor')
    pHSensorInfo = dbManager.getSensor('phSensor')
    turbiditySensorInfor = dbManager.getSensor('turbiditySensor')

    valueTempSensor = digitalSensors.read_temp()
    valueTdsSensor, valuepHSensor, valueTurbiditySensor, e = analogicSensors.getAnalogicSensorReadings()

    if not e != None:
        tempReading = {
            "id": 0,
            "value": valueTempSensor,
            "timestamp": "",
            "id_sensor": tempSensorInfo["id_sensor"]
        }
        tdsReading = {
            "id": 0,
            "value": valueTdsSensor,
            "timestamp": "",
            "id_sensor": tdsSensorInfo["id_sensor"]
        }
        pHReading = {
            "id": 0,
            "value": valuepHSensor,
            "timestamp": "",
            "id_sensor": pHSensorInfo["id_sensor"]
        }
        turbidityReading = {
            "id": 0,
            "value": valueTurbiditySensor,
            "timestamp": "",
            "id_sensor": turbiditySensorInfor["id_sensor"]
        }

        sensorReadingsList = [pHReading, tdsReading, tempReading, turbidityReading]
        messageSensorReadings = {
            "idUser": deviceInfo["id_user"],
            "idFiltrer": deviceInfo["id_device"],
            "sensorReadings": sensorReadingsList
        }

        try:
            publisher.publishMessage("websocket_topic.many_readings", messageSensorReadings)
            publisher.publishMessage("db_topic", sensorReadingsList)
        except Exception as e:
            print("")