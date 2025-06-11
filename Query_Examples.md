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
