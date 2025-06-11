# О программе
Это простое Flask-приложение, предоставляющее RESTful API для управления списком задач и тегов. Оно использует SQLite в качестве базы данных по умолчанию, имеет валидацию входящих данных, обработку ошибок и подробные сообщения в ответах.

### Функционал:

Для задач (/tasks):
- POST /tasks: Создать новую задачу
- GET /tasks: Получить список всех задач (можно фильтровать по тегу)
- GET /tasks/{id}: Получить задачу по ID
- PUT /tasks/{id}: Обновить задачу
- DELETE /tasks/{id}: Удалить задачу
  
Для тегов (/tags):
- POST /tags: Создать новый тег
- GET /tags: Получить список всех тегов
- GET /tags/{id}: Получить тег по ID
- PUT /tags/{id}: Обновить имя тега
- DELETE /tags/{id}: Удалить тег

### Требования:
- Python 3.8 или выше
- pip (установлен вместе с Python)

### Как запустить:

 Склонируйте репозиторий: [Ссылка]([https://github.com/vmangos/wiki](https://github.com/KinLab666/Test_Programm.git))

### Создайте виртуальное окружение

Linux/macOS:
```
 python -m venv venv
 source venv/bin/activate
```
Windows:
```
 python -m venv venv
 venv\Scripts\activate
```
### Установите зависимости:

- pip install -r requirements.txt

### Запустите приложение:

- python app.py

- API будет доступен по адресу: http://localhost:5000

### База данных

- По умолчанию используется SQLite . При первом запуске создаётся файл instance/tasks.db.
- Если файла нет, он создаётся автоматически вместе с таблицами task, tag.

### Примеры запросов через Postman или curl

Создать задачу
```
 POST http://localhost:5000/tasks
 Content-Type: application/json
 {
   "title": "Купить продукты",
   "description": "Закупиться на выходные",
   "deadline": "2025-04-10T18:00:00",
   "completed": false,
   "tags": ["дом", "покупки"]
 }
```
Получить все задачи
```
 GET http://localhost:5000/tasks
```
Получить задачи по тегу
```
 GET http://localhost:5000/tasks?tag=дом
```
Получить одну задачу
```
 GET http://localhost:5000/tasks/1
```
Обновить задачу
```
 PUT http://localhost:5000/tasks/1
 Content-Type: application/json
 {
   "title": "Обновлённая задача",
   "completed": true,
   "tags": ["личное"]
 }
```
Удалить задачу
```
 DELETE http://localhost:5000/tasks/1
```
Создать тег
```
 POST http://localhost:5000/tags
 Content-Type: application/json
 {
   "name": "важное"
 }
```
Получить все теги
```
 GET http://localhost:5000/tags
```
Получить один тег
```
 GET http://localhost:5000/tags/1
```
Обновить тег
```
 PUT http://localhost:5000/tags/1
 Content-Type: application/json
 {
   "name": "срочное"
 }
```
 Удалить тег
 ```
 DELETE http://localhost:5000/tags/1
```
### Тестирование
- Проект содержит unit-тесты, написанные с использованием pytest. Они находятся в папке tests/.

Как запустить тесты:
```
 pip install pytest
 pytest tests/test_api.py -v
```
### Валидации
 Все запросы проверяют данные на корректность:
- Поле title обязательно для задач.
- Имя тега должно быть уникальным.
- Некорректный формат даты вызывает ошибку 400.
- Если объект не найден — возвращается 404.

Пример ответа с ошибкой:
```
{
   "ошибка": "Ошибка валидации"
}
```
