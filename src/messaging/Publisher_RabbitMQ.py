import pika

class PublisherAMQP:
    def __init__(self, config):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.getAMQPURL()))
        self.channel = self.connection.channel()
        self.exchange = config.getExchange()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic')
    
    def publishMessage(self, routing_key, message):
        print(f"Publicando mensaje en el tópico {routing_key}: {message}")
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=message)
        print("Mensaje publicado!")