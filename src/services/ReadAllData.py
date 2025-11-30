from datetime import datetime

def GetSensorsData (analogicSensors, digitalSensors, dbManager, publisher, userConfig):
    # Obtiene lecturas de sensores
    try:
        valueTempSensor = digitalSensors.read_temp()
        valuepHSensor, valueTdsSensor, valueTurbiditySensor, e = analogicSensors.getAnalogicSensorReadings()
    except Exception as e:
        print("Error al obtener lecturas:", e)
        return 0, 0, 0, 0, False

    if e != None or userConfig.userId:
        # Obtiene timestamp (Fecha y hora)
        now = datetime.now()
        iso_string = now.isoformat() + 'Z'
        # Hace un diccionario de las lecturas
        tempReading = {
            "id": 0,
            "value": valueTempSensor,
            "date": iso_string,
            "sensor_id": userConfig.sensorsInfo[0]["sensor_id"]
        }
        tdsReading = {
            "id": 0,
            "value": valueTdsSensor,
            "date": iso_string,
            "sensor_id": userConfig.sensorsInfo[1]["sensor_id"]
        }
        pHReading = {
            "id": 0,
            "value": valuepHSensor,
            "date": iso_string,
            "sensor_id": userConfig.sensorsInfo[2]["sensor_id"]
        }
        turbidityReading = {
            "id": 0,
            "value": valueTurbiditySensor,
            "date": iso_string,
            "sensor_id": userConfig.sensorsInfo[3]["sensor_id"]
        }

        sensorReadingsList = [pHReading, tdsReading, tempReading, turbidityReading]
        messageSensorReadings = {
            "idUser": userConfig.userId,
            "idFiltrer": userConfig.deviceId,
            "sensorReadings": sensorReadingsList
        }

        # Intenta publicar las lecturas en los tópicos
        backed = False
        try:
            publisher.publishMessage("websocket_topic.many_readings", messageSensorReadings)
            print("Datos enviados al websocket")
            publisher.publishMessage(".measurements", sensorReadingsList)
            print("Datos enviados a la Base de datos")
            backed = True
        # Si no puede, almacena las lecturas locales como no respaldadas
        except Exception as e:
            print("Error al mandar datos por amqp:", e)
            backed = False
        
        try:
            # Almacena en la bd local
            dbManager.createSensorReading(tempReading["value"], tempReading["sensor_id"], backed)
            dbManager.createSensorReading(tdsReading["value"], tdsReading["sensor_id"], backed)
            dbManager.createSensorReading(pHReading["value"], pHReading["sensor_id"], backed)
            dbManager.createSensorReading(turbidityReading["value"], turbidityReading["sensor_id"], backed)
            print("Lecturas guardadas de manera local")
        except Exception as e:
            print("Error al guardar lecturas de manera local")
        # Retorna los valores leídos
        return valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor, True
    else:
        print("Error en la toma de lecturas")
        return False