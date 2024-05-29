import pika
import json
import requests
import config


# Create a callback function
def callback(ch, method, properties, body):
    """Функция отправляет POST-запрос на сервер при создании нового сообщения в очереди"""
    new_message = json.loads(body)
    new_message.update({'message': 'message done'})
    requests.post(url=config.url_site, json=new_message)


def start_consumer():
    """Прослушивает очередь в брокере сообщений"""
    # Create connection
    connection = pika.BlockingConnection(
        pika.URLParameters(f"amqp://{config.MQ_USER}:{config.MQ_PASSWORD}@{config.MQ_HOST}:5672/"))
    channel = connection.channel()
    # Listen to the queue and call the callback function on receiving a message
    channel.basic_consume(queue='organ_docs', on_message_callback=callback, auto_ack=True)
    # Start consuming
    print('Началось прослушивание очереди...')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
