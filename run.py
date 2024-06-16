import pika
import json
import requests

try:
    from config import MQ_HOST, MQ_PASSWORD, MQ_URL_SITE, MQ_USER
except ImportError:
    import os

    MQ_URL_SITE = os.getenv('MQ_URL_SITE')
    MQ_HOST = os.getenv('MQ_HOST')
    MQ_USER = os.getenv('MQ_USER')
    MQ_PASSWORD = os.getenv('MQ_PASSWORD')


# Create a callback function
def callback(ch, method, properties, body):
    """Функция отправляет POST-запрос на сервер при создании нового сообщения в очереди"""
    new_message = json.loads(body)
    new_message.update({'message': 'message done'})
    print(new_message)
    requests.post(url=MQ_URL_SITE, json=new_message)


def start_consumer():
    """Прослушивает очередь в брокере сообщений"""
    # Create connection
    connection = pika.BlockingConnection(
        pika.URLParameters(f"amqp://{MQ_USER}:{MQ_PASSWORD}@{MQ_HOST}:5672/"))
    channel = connection.channel()
    # Listen to the queue and call the callback function on receiving a message
    channel.basic_consume(queue='organ_docs', on_message_callback=callback, auto_ack=True)
    # Start consuming
    print('Началось новое прослушивание очереди...')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
