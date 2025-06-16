### Примеры запросов через curl на Windows

[Вернутся назад](README.md)

Создать задачу
```
curl -X POST http://localhost:5000/tasks
-H "Content-Type: application/json"
-d "{
 \"title\": \"Купить продукты\",
 \"description\": \"Закупиться на выходные\",
 \"deadline\": \"2025-04-10T18:00:00\",
 \"completed\": false,
 \"tags\": [\"дом\", \"покупки\"]
}"
```
Получить все задачи
```
curl http://localhost:5000/tasks
```
Получить задачи по тегу
```
curl http://localhost:5000/tasks?tag=дом
```
Получить одну задачу
```
curl http://localhost:5000/tasks/1
```
Обновить задачу
```
curl -X PUT http://localhost:5000/tasks/1
-H "Content-Type: application/json"
-d "{
 \"title\": \"Купить машину\",
 \"completed\": true,
 \"tags\": [\"покупки\", \"Транспорт\"]
}"
```
Удалить задачу
```
curl -X DELETE http://localhost:5000/tasks/1
```
Создать тег
```
curl -X POST http://localhost:5000/tags
-H "Content-Type: application/json"
-d "{
\"name\": \"тест\"
}"
```
Получить все теги
```
curl http://localhost:5000/tags
```
Получить один тег
```
curl http://localhost:5000/tags/1
```
Обновить тег
```
curl -X PUT http://localhost:5000/tags/1
-H "Content-Type: application/json"
-d "{
\"name\": \"Редактированая\"
}"
```
 Удалить тег
 ```
curl -X DELETE http://localhost:5000/tags/1
```
