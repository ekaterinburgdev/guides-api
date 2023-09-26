# guides-api

📗 Back-end for [Ekaterinburg guides website](https://github.com/ekaterinburgdev/guides) using Python Django & PostgreSQL.

The application caches content from Notion via Notion API into PostgreSQL database.

**[guides-api.ekaterinburg.city](https://guides-api.ekaterinburg.city)**

## API

### Pages tree
Returns tree of all page urls

```sh
https://guides-api.ekaterinburg.city/api/tree
```

### Get page
Returns page content

```sh
# Section
https://guides-api.ekaterinburg.city/api/content/street-name-plates

# Section + Page
https://guides-api.ekaterinburg.city/api/content/street-name-plates/general-provisions
```

- `street-name-plates` — section name
- `general-provisions` — page name


### Search
Search pages by query

```sh
https://guides-api.ekaterinburg.city/api/search?pattern=скамья
```
- `скамья` — search query


## Debug API

> TODO: describe `dbretrieve` & `dbchildren` methods

Methods for raw Notion data debugging

### Get page Notion raw metadata


```sh
https://guides-api.ekaterinburg.city/api/test/retrieve?id=5604e0725f794708b9094b7ce49a46f7
```
- `5604e0725f794708b9094b7ce49a46f7` — Notion page id

### Get page Notion raw content
```sh
https://guides-api.ekaterinburg.city/api/test/children?id=5604e0725f794708b9094b7ce49a46f7
```
- `5604e0725f794708b9094b7ce49a46f7` — Notion page id

## Telegram bot commands
The site is managed via a telegram bot

`/update` — update content

`/update -f` — force update (rebuild tree, reload images, etc.)

## Development

1. Install [Docker](https://docs.docker.com/get-docker/)


2. Create `manuals/.env` file from [`manuals/.env.example`](https://github.com/ekaterinburgdev/guides-api/blob/main/manuals/.env.example) with secrets
- Notion token
- Django settings
- PostgreSQL settings
- Telegram (bot token from [@BotFather](https://telegram.me/BotFather) + master chat id from [@userinfobot](https://t.me/userinfobot)).


3. _(only first time)_ Create static volume folder
> TODO: create folder automatically in project folder (the folder path must be contained in `.gitignore`)
```sh
mkdir /usr/local/docker/manuals-static-volume/
```


4. _(only first time)_ Run database migrations
```sh
docker compose exec manuals python manage.py migrate
```

5. Run Django & Telegram bot
```sh
docker compose up -d --build
```

6. _(only first time)_ Send message to Telegram bot to force update
```
`/update -f`
```

<br />

## Updates 15.04.2022

> TODO: Translate to English, remove deprecated descriptions

Инструкция по запуску старая. Возможны ошибки, если кто-то создавал volume. Чтобы всё точно перебилдилось рекомендую хотя бы в первый раз запустить билд с флагами:


### Новые возможности:

- Теперь помимо первого раздела есть типовая страница
- Все страницы получаются по пути baseurl/api/content?id={page_id}
- Можно получить список всех страниц по пути baseurl/api/options
- Можно получать от сервера не только самые большие по вложенности страницы, но и любого дочернего элемента по тому же пути, используя id элемента. В них так же будут вложены все их дети
- Изменился формат ответа по baseurl/api/content. Теперь он выглядит так: { "{element_id}" : { "type" : "{element_tupe}", content : "{контент самого элемента*}", children : [{рекурсивно вложенный потомок того же формата}, ...]** } }
- По просьбе Льва есть ручки для получения элементов напрямую с ноушена, но они у меня из докера отказались работать. Позже разберусь. Может у вас будет работать:
    - для получения самого элемента baseurl/api/test/retrieve?id={page_id}
    - для получения потомков элемента baseurl/api/test/children?id={page_id}

Оказалось, что типов элементов ноушена (по крайней мере тех, которые есть в типовой странице) очень много (порядка 26), и разобрать контент каждой я не успел. Поэтому, если в каком-то элементе летит много мусора, а полезной информации совсем немного - сообщите, буду разбирать содержимое такого типа и хранить только то, что полезно. А пока что в content лежит почти весь контент элемента.

Обратите внимание, что в контенте элемента типа image лежит json с контентом из ноушена по ключу "image_data" (оставил, потому что именно там лежат подписи к картинкам, если они есть), а по ключу "image_name" лежит название картинки для получения её сохраненной на сервере копии по пути baseurl/static/{image_name}

Если хочется посмотреть на сохраненные элементы с фильтрацией по типам, рекомендую использовать админку. Инструкция уже была выше.

*Элементы, содержащие детей тоже могут иметь свой контент. Пример - сворачивающийся список (тип "toggle"), который имеет надпись, которая попадет в контент, при этом имеет детей - элементы сворачивающегося списка.

**Если потомков нет, то список будет пустой - []

## Deprecated

Перед билдом необходимо создать .env файл в той же директории, где лежит .env.example. В экзампле можно посмотреть, что нужно заполнить. За ключом от джанги нужно обратиться ко мне (Евгений).

Билд образа: 
``` bash
docker-compose build
```

Запуск контейнера:
``` bash
docker-compose up -d
```

Чтобы всё работало хорошо сейчас нужно запустить миграции и заполнить БД (пока что. Позже сделаю, чтобы всё само работало). Обязательно выполните:
``` bash
docker-compose exec manuals python manage.py migrate
docker-compose exec manuals python manage.py init_db_check
```

По умолчанию стоит внешний порт 48655

~~Получение контента страницы: baseurl/api/content~~

Получение картинки по id: baseurl/static/{pageid}

pageid находится в контенте, как правило выглядит как строковый id.png

Если нужно посмотреть содержание БД, можно использовать админку. Для этого нужно зарегистрировать суперюзера, для этого выполнить
``` bash
docker-compose exec manuals python manage.py createsuperuser 
```
После выполнения указать логин, мейл и пароль. Можно любые
Использовать админку: baseurl/admin/
(слэш в конце обязателен)
Откроется страничка аутентификации. Вводите свои логин и пароль, указанные на этапе создания суперюзера

Остановить контейнер: 
``` bash
docker-compose down
```
