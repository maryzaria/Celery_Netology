# Домашнее задание к лекции «Celery»

Специалист по машинному обучению создал модель для 
[апскейлинга](https://ru.wiktionary.org/wiki/%D0%B0%D0%BF%D1%81%D0%BA%D0%B5%D0%B9%D0%BB%D0%B8%D0%BD%D0%B3) 
изображений и функцию, которая позволяет ее использовать.  
Файлы проекта находится [здесь](upscale).  
`EDSR_2.pb` - модель.  
В модуле `upscale.py` находится функция `upscale`, которая имплементирует модель и функция `example` с примером использования.  
В файле `requirements.txt` перечислены зависимости

Перед Вами стоит задача написать сервис для апскейлинга изображений на базе Flask, Celery и ИИ модели.
Должно быть реализовано 3 роута
- POST `/upscale`. Принимает файл с изображением и возвращает id задачи
- GET `/tasks/<task_id>` возвращает статус задачи и ссылку на обработанный файл, если задача выполнена
- GET `/processed/{file}` возвращает обработанный файл

Дополнительные задачи:
- перепишите функцию `upscale` так, чтобы файл `EDSR_x2.pb` считывался только один раз, а не при каждом вызове функции
- попробуйте написать сервис и функцию `upscale` таким образом, чтобы не сохранять файлы изображений на диск
- докеризируйте приложение
- напишите тесты

# Запуск приложения

### 1. Запускаем redis 

```shell
docker-compose up redis
```
Должна быть строка:

```redis-1  | 1:M 08 Feb 2024 14:24:36.869 * Ready to accept connections```
### 2. Запускаем celery

В другой вкладке терминала запускаем celery 

```shell
docker-compose --env-file .env.test up celery
```
Должен получится вывод без ошибок

### 3. Запускаем приложение
В другой вкладке терминала запускаем приложение

```shell
docker-compose --env-file .env.test up app
```
