# URLer - Uniform Resource Locator shortener.

## How to prepare environment

A projects works well with python 3.11. Other version were not tested.

Create virtual environment
```bash
pip3 install virtualenv
python3 -m virtualenv venv -p python3
source venv/bin/activate
```
Install dependencies
```bash
pip install -r requirements.txt
```
Also, you may install additional dependencies (they are set for testing and refactoring purposes).
```bash
pip install -r requirements-dev.txt
```

## How to prepare a database

Install PostgreSQL from the official site with an elephant as the logo.

Install Rancher Desktop (or another similar software).

Rancher Desktop will install a required software by itself.
Projects works well with Kubernetes 1.24.17. 

Rancher Desktop --> Settings --> Container engine --> dockerd (moby)

If it's installed, just open it, and Rancher Desktop will run a virtual machine. 

Run a container for PostgreSQL by a following command (just in a standard terminal):
```bash
docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:14.5
```
Use these username and password only for a local running. For a real server choose more sophisticated password.

Create `.env` file in the root of project with `PROJECT_NAME='Your-name-for-this-project'`
```bash
touch .env
echo "PROJECT_NAME='URLer'" > .env
```


## How to run

**Run server**
```bash
uvicorn src.main:app \
--host 127.0.0.1 \
--port 8080 \
--reload \
--reload-include src
```
_Note: 0.0.0.0 may not work in Safari browser_
`--reload-exclude tests` requires watchgod installed. Otherwise, run without this line (flag).

## How to test

### In browser
Open any link in any browser

 * Swagger http://127.0.0.1:8080/docs
 * ReDoc http://127.0.0.1:8080/redoc
 * OpenAPI documentation (json) http://127.0.0.1:8080/openapi.json

### With pytest and TestClient
Run all tests by
```bash
pytest
```
or create your own tests in `tests` folder. You may use tests in `test_routes.py` as template for your tests.

### In docker container
Use the next command to connect to the terminal of runned container
```bash
docker exec -it postgres-fastapi psql -U postgres 
```
To show all databases
```bash
\dt
```
To show all records in a database `recordmodel`
```
SELECT * FROM recordmodel;
```

## A tidy up and a health check

Install additional "developer's" requirements
```bash
pip install -r requirements-dev.txt
```

A linter
```bash
ruff src
```

A linter's fixing tool
```bash
ruff src --fix
```

A formatter
```bash
ruff format src
```

A default 'health-checking' linter
```bash
flake8 src
```

A static type checker tool
```bash
mypy src
```

# Тому кто будет это читать

## Способности проекта

Проект может:
 - генерировать случайные короткие ссылки (точнее, айдишки - из четырех 16-ричных цифр) - 
```
POST `/shorten` json={'url': <ссылка>}
```
 - выдавать полную ссылку по короткой ссылке 
```
GET `/link?url_id=abcd`
```
 - подсчитывать число переходов по ссылке (`RecordModel->used`)
 - удалять (deprecate) ссылки. Операция безвозвратная
```
PATCH `/deprecate?url_id=abcd`
```
 - выдавать запись из базы данных о ссылке 
```
GET `/info?url_id=abcd`
```
 - выдавать ошибки. Например, при попытке передать неверную ссылку (например, "https://example .com")


## Результаты

В ходе работы над этим заданием автору удалось **впервые**:
 - [x] Полноценно поработать с FastApi и подобными фреймворками в принципе
 - [x] Опробовать всю магию pydantic - действительно удобный инструмент как о нём ходили слухи
 - [x] Писать Post- и Patch- запросы
 - [x] Поработать с сопутствующими технологиями как uvicorn, FastApi TestClient и др. 
 - [x] Поработать с базой данных через ORM (в частности, SqlAlchemy) - вместо написаний каноничных SQL-запросов
 - [x] Внедрить базу данных в свой проект (PostgreSQL)

Хотелось, но не удалось впервые применить (из-за нехватки времени на эти новые технологии):

 - [ ] Сделать отдельно схемы (протокол взаимодействия клиентов и сервера) и отдельно модели (взаимодействие ORM и базы данных). 
 - Вместо этого используется SQLModel, объединяющий эти сущности. Он объединяет Pydantic и SQLAlchemy под единым интерфейсом. Оптимизирован под FastApi.

Также не реализован batch upload ссылок. Но обычный, по одной ссылке, работает отлично.

# Проектное задание четвёртого спринта

Спроектируйте и реализуйте сервис для создания сокращённой формы передаваемых URL и анализа активности их использования.

Кроме этого, выберите из списка дополнительные требования и тоже реализуйте их. У каждого задания есть определённая сложность, от которой зависит количество баллов. Вам необходимо выбрать такое количество заданий, чтобы общая сумма баллов была больше 4. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

Реализовать `http`-сервис, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080` (значение по умолчанию, можно изменять).

<details>
<summary> Список возможных эндпойнтов (можно изменять) </summary>

1. Получить сокращённый вариант переданного URL.

```python
POST /
```

Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.

2. Вернуть оригинальный URL.

```python
GET /<shorten-url-id>
```

Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL.

```python
GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
```

Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает информацию о количестве переходов, совершенных по ссылке.

В ответе может содержаться как **общее количество совершенных переходов**, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
- дата и время перехода/использования ссылки;
- информация о клиенте, выполнившем запрос;

</details>


## Дополнительные требования (отметьте [Х] выбранные пункты):

- [x] (1 балл) Реализуйте метод `GET /ping`, который возвращает информацию о статусе доступности БД.
- [x] (1 балл) Реализуйте возможность «удаления» сохранённого URL. Запись должна остаться, но помечаться как удалённая. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.
- [ ] (2 балла) Реализуйте middlware, блокирующий доступ к сервису из запрещённых подсетей (black list).
- [x] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).

<details>
<summary> Описание изменений </summary>

- Метод `POST /shorten` принимает в теле запроса список URL в формате:

```python
[
    {
        "original-url": "<URL-for-shorten>"
    },
    ...
]

```
... и возвращает данные в следующем формате:

```python
[
    {
        "short-id": "<shoten-id>",
        "short-url": "http://...",
    },
    ...
]
```
</details>


- [ ] (3 балла) Реализуйте взаимодействие с сервисом авторизованного пользователя. Пользователь может создавать как приватные, так и публичные ссылки или изменять видимость ссылок. Вызов метода `GET /user/status` возвращает все созданные ранее ссылки в формате:

```
[
    {
        "short-id": "<text-id>",
        "short-url": "http://...",
        "original-url": "http://...",
        "type": "<public|private>"
    },
    ...
]
```

- [ ] **(5 баллов) Реализуйте кастомное взаимодействия с БД. Необходимо учесть возможность работы с транзакциями.


## Требования к решению

1. Используйте фреймворк FastAPI. В качестве СУБД используйте PostgreSQL (не ниже 10 версии).
2. Используйте концепции ООП.
3. Предусмотрите обработку исключительных ситуаций.
4. Приведите стиль кода в соответствие pep8, flake8, mypy.
5. Логируйте результаты действий.
6. Покройте написанный код тестами.
