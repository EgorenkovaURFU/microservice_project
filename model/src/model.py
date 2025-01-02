import pika
import pickle
import numpy as np
import json


with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')


    def callback(ch, method, properties, body):
        print(f'Получен вектор признаков {body}')
        data = json.loads(body)
        features = data.get('body')
        id = data.get('id')
        shaped_features = np.array(features).reshape(1, -1)
        prediction = regressor.predict(shaped_features)[0]
        prediction_message = {
            'id': id,
            'body': prediction}
        channel.basic_publish(exchange='',
                            routing_key='y_pred',
                            body=json.dumps(prediction_message))
        print(f'Предсказание {id} - {prediction} отправлено в очередь.')


    channel.basic_consume(
        queue='features',
        on_message_callback=callback,
        auto_ack=True
    )
    print('... Ожидание сообщенийб для выхода нажмите CTRL+C')

    channel.start_consuming()
