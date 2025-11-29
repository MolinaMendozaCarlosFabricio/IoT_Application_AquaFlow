import json

class ConfigUser:
    def __init__(self):
        with open('src/config/userConfig.json', 'r') as file:
            data = json.load(file)
            self.deviceId = data["device_id"]
            self.userId = data["user_id"]
            self.model = data["model"]
            self.createdAt = data["created_at"]
            self.sensorsInfo = data["sensors_info"]