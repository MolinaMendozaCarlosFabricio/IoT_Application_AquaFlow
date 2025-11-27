import pika
import json

class PublisherAMQP:
    def __init__(self, config):
        # Inicia la conexión con el broker AMQP y el exchange
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.getAMQPURL()))
        self.__channel = self.__connection.channel()
        self.__exchange = config.getExchange()
        self.__channel.exchange_declare(exchange=self.__exchange, exchange_type='topic', durable=True)
    
    # Método para enviar un mensaje por el broker AMQP
    def publishMessage(self, routing_key, message):
        print(f"Publicando mensaje en el tópico {routing_key}: {message}")
        self.__channel.basic_publish(
            exchange=self.__exchange, 
            routing_key=routing_key, 
            body=json.dumps(message)
        )
        print("Mensaje publicado!")
    
    # Método para cerrar conexión con el broker AMQP
    def closeConnection(self):
        self.__connection.close()