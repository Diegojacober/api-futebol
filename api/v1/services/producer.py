import pika, json, os

from dotenv import load_dotenv

load_dotenv()

params = pika.URLParameters(os.getenv("RABBIT_MQ_URL"))

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='sendemail', body=json.dumps(body), properties=properties)