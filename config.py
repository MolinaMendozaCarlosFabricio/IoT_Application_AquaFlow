import os
from dotenv import load_dotenv

# Carga las variables de entrno
class Config:
    def __init__(self):
        load_dotenv()
        self.__amqp_url = os.getenv("RABBITMQ_URL", "localhost")
        self.__exchange_name = os.getenv("EXCHANGE_NAME", "my-exchange")
    
    def getAMQPURL(self):
        return self.__amqp_url
    
    def getExchange(self):
        return self.__exchange_name