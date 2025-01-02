import pika
import numpy as np
from sklearn.datasets import load_diabetes
import json
import time
from datetime import datetime


while True:
    try:
        X, y = load_diabetes(return_X_y=True)
        random_row = np.random.randint(0, X.shape[0]-1)

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='y_true')

        message_id = datetime.timestamp(datetime.now())
        message_y_true = {
            'id': message_id,
            'body': y[random_row]}
        
        message_features = {
            'id': message_id,
            'body': list(X[random_row])
        }

        channel.basic_publish(exchange='',
                            routing_key='y_true',
                            body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь.')

        channel.queue_declare(queue='features')
        channel.basic_publish(exchange='',
                            routing_key='features',
                            body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь.')

        time.sleep(10)

        connection.close()
    except Exception:
        print('Не удалось подключиться к очереди.')

