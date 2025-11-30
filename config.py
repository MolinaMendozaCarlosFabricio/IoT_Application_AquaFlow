import os
from dotenv import load_dotenv

# Carga las variables de entrno
class Config:
    def __init__(self):
        load_dotenv()
        self.__amqp_url = os.getenv("RABBITMQ_URL", "localhost")
        self.__amqp_ip = os.getenv("RABBITMQ_IP", "127.1.1.1")
        self.__amqp_port = os.getenv("RABBITMQ_PORT", "5672")
        self.__amqp_usr = os.getenv("RABBITMQ_USER", "guest")
        self.__amqp_pwd = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.__exchange_name = os.getenv("EXCHANGE_NAME", "my-exchange")
    
    def getAMQPURL(self):
        return self.__amqp_url
    
    def getAMQPIP(self):
        return self.__amqp_ip
    
    def getAMQPPort(self):
        return self.__amqp_port
    
    def getAMQPUsr(self):
        return self.__amqp_usr
    
    def getAMQPPwd(self):
        return self.__amqp_pwd
    
    def getExchange(self):
        return self.__exchange_name