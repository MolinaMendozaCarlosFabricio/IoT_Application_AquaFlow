import serial

class AnalogicSensors:
    def __init__(self):
        # Establece conexión por puerto serial (vía bluetooth) con el ESP32
        self.ser = serial.Serial('/dev/rfcomm0', baudrate=115200, timeout=2)
    
    # Método para obtener lecturas del esp32
    def getAnalogicSensorReadings(self):
        data = self.ser.readline().decode().strip()
        if data:
            # Decodifica la información recibida
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
