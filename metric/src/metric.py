import pika
import json
import os
import pandas as pd


def write_metric(id, y, y_type):
    file_path = './logs/metric_log.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except Exception:
            print(f'Ошибка при чтении файла {file_path}')
            return
    else:
        df = pd.DataFrame(columns=['id', 'y_true', 'y_pred', 'absolute_error'])
    
    index = df['id'] == id

    if any(index):
        if y_type == 'y_true':
            df.loc[index, 'y_true'] = y
            df.loc[index, 'absolute_error'] = abs(y - df.loc[index, 'y_pred'])
        else:
            df.loc[index, 'y_pred'] = y
            df.loc[index, 'absolute_error'] = abs(df.loc[index, 'y_true'] - y)
    else:
        df.loc[len(df)] = [
            id, 
            y if y_type == 'y_true' else None,
            y if y_type == 'y_pred' else None,
            None
            ]
    df.to_csv('./logs/metric_log.csv', index=False)
    print('Файл с метриками обновлен.')


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')
    channel.queue_declare(queue='plot_run')

    def callback(ch, method, properties, body):
        data  = json.loads(body)
        y = data.get('body')
        id = data.get('id')
        if method.routing_key == 'y_true':
            write_metric(id, y, 'y_true')
        elif method.routing_key == 'y_pred':
            write_metric(id, y, 'y_pred')
        channel.basic_publish(exchange='',
            routing_key = 'plot_run',
            body=json.dumps('Поступили новые данные'))

    channel.basic_consume(
            queue='y_true',
            on_message_callback=callback,
            auto_ack=True
        )

    channel.basic_consume(
            queue='y_pred',
            on_message_callback=callback,
            auto_ack=True
        )


    print('...Ожидание сообщений для выхода нажмите CTRL+C')
    channel.start_consuming()
except:
    print('Не удалось подключиться к очереди')

