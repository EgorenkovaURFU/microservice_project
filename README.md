# Microservice Project

<b>Сервис №1.</b>

Загружает [данные о диабете](https://scikit-learn.org/1.5/modules/generated/sklearn.datasets.load_diabetes.html)

Каждые 10 секунд рандомный ряд из признаков отправляется в очередь на предсказание. Также отправляется таргетное значение в очередь для оценки результата. у каждого сообщения есть id.

<b>Сервис №2.</b>

Сервис далает предсказание для ряда признаков полученного от сервиса №1. Предсказание отправляет в оцередь для оценки результата.
В папке logs/ создается и далее пополняется данными файл metric_log.csv.
В данный файл сохраняются метрики message_id, y_true, y_pred, absolute_error
При этом значения y_true, y_pred одной итерации идентифицируются и связываются с помощью message_id

<b>Сервис №3.</b>

Сервис рассчитвывает абсолютное отклолонение прогноза от реального значения.
В папке logs/ создается и далее пополняется данными файл metric_log.csv.
В данный файл сохраняются метрики message_id, y_true, y_pred, absolute_error

<b>Сервис №4.</b>

Сервис plot считывает данные из metric_log.csv и создает график error_distribution.png

<b>Оркестрация</b>

Сервисы аркестрируются с помощью Docker compose.
Файл docker-compose.yaml который указывает порядок запуска микросервисов внутри docker контейнера
Далее в терминале собран docker образ с помощью команды: docker-compose build
Далее запущен контейнер из данного образа: docker-compose up -d
Контроль работы сервисов можно осуществлять с помощью команд:
- docker ps
- docker-compose logs -f features
- docker-compose logs -f model
- docker-compose logs -f metric
- docker-compose logs -f plot