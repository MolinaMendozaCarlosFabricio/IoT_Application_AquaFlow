import time

def GetSensorsData (analogicSensors, digitalSensors, dbManager, publisher):
    deviceInfo = dbManager.getDeviceInfo()
    tempSensorInfo = dbManager.getSensor('ds18b20')
    tdsSensorInfo = dbManager.getSensor('tdsSensor')
    pHSensorInfo = dbManager.getSensor('phSensor')
    turbiditySensorInfor = dbManager.getSensor('turbiditySensor')

    valueTempSensor = digitalSensors.read_temp()
    valuepHSensor, valueTdsSensor, valueTurbiditySensor, e = analogicSensors.getAnalogicSensorReadings()

    if e != None or deviceInfo["synchronized"]:
        tempReading = {
            "id": 0,
            "value": valueTempSensor,
            "timestamp": "",
            "sensor_id": tempSensorInfo["id_sensor"]
        }
        tdsReading = {
            "id": 0,
            "value": valueTdsSensor,
            "timestamp": "",
            "sensor_id": tdsSensorInfo["id_sensor"]
        }
        pHReading = {
            "id": 0,
            "value": valuepHSensor,
            "timestamp": "",
            "sensor_id": pHSensorInfo["id_sensor"]
        }
        turbidityReading = {
            "id": 0,
            "value": valueTurbiditySensor,
            "timestamp": "",
            "sensor_id": turbiditySensorInfor["id_sensor"]
        }

        sensorReadingsList = [pHReading, tdsReading, tempReading, turbidityReading]
        messageSensorReadings = {
            "idUser": deviceInfo["id_user"],
            "idFiltrer": deviceInfo["id_device"],
            "sensorReadings": sensorReadingsList
        }

        try:
            publisher.publishMessage("websocket_topic.many_readings", messageSensorReadings)
            print("Datos enviados al websocket")
            publisher.publishMessage(".measurements", sensorReadingsList)
            print("Datos enviados a la Base de datos")
            dbManager.createSensorReading(tempReading["value"], tempReading["id_sensor"], True)
            dbManager.createSensorReading(tdsReading["value"], tdsReading["id_sensor"], True)
            dbManager.createSensorReading(pHReading["value"], pHReading["id_sensor"], True)
            dbManager.createSensorReading(turbidityReading["value"], turbidityReading["id_sensor"], True)
            print("Lecturas guardadas de manera local")
        except Exception as e:
            print("Error al mandar datos por amqp:", e)
            dbManager.createSensorReading(tempReading["value"], tempReading["id_sensor"], False)
            dbManager.createSensorReading(tdsReading["value"], tdsReading["id_sensor"], False)
            dbManager.createSensorReading(pHReading["value"], pHReading["id_sensor"], False)
            dbManager.createSensorReading(turbidityReading["value"], turbidityReading["id_sensor"], False)
            print("Datos guardados de manera local")
        
        return valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor
    else:
        print("Error en la toma de lecturas")
        return False