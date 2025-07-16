import serial

class AnalogicSensors:
    def __init__(self):
        self.ser = serial.Serial('/dev/rfcomm0', baudrate=115200, timeout=2)
    
    def getAnalogicSensorReadings(self):
        data = self.ser.readline().decode().strip()
        if data:
            print(f"Datos recibidos: {data}")
            chunks = dict(item.split('=') for item in data.split(','))
            try:
                ph = float(chunks["PH"])
                tds = float(chunks["TDS"])
                ntu = float(chunks["NTU"])

                return ph, tds, ntu, None
            except Exception as e:
                print("Error al parsear salida serial:", e)
                return 0, 0, 0, e
