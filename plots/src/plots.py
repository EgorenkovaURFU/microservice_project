import pandas as pd
import pika
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='plot_run')
    print('Новое сообщение')

    def callback(ch, method, properties, body):
        print(f'Из очереди {method.routing_key} получено сообщение {json.loads(body)}')
        file_path = './logs/metric_log.csv'
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
            except Exception:
                print(f'Ошибка при чтении файла {file_path}')
                return
        else:
            print(f'Файл {file_path} не существует')
            return
        plot = sns.histplot(df['absolute_error'], kde=True)
        fig = plot.get_figure()
        fig.savefig('./logs/error_distribution.png')
        print('Файл с распределением абсолютной ошибки успешно сохранен')
        
    channel.basic_consume(
            queue='plot_run',
            on_message_callback=callback,
            auto_ack=True
        )

    print('...Ожидание сообщений для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception:
    print('Не удалось подключиться к очереди')

            
            
            



    
