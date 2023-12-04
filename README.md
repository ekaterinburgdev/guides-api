# guides-api

📗 Back-end for [Ekaterinburg guides website](https://github.com/ekaterinburgdev/guides) using Python Django & PostgreSQL.

The application caches content from Notion via Notion API into PostgreSQL database.

**[guides-api.ekaterinburg.city](https://guides-api.ekaterinburg.city)**

## API

### Pages tree
Returns tree of all page urls

```
https://guides-api.ekaterinburg.city/api/tree
```

### Get section/page
Returns page section or page content

```sh
https://guides-api.ekaterinburg.city/api/content/street-name-plates
https://guides-api.ekaterinburg.city/api/content/street-name-plates/general-provisions
```

- `street-name-plates` — section name
- `general-provisions` — page name


### Search
Search pages by query

```
https://guides-api.ekaterinburg.city/api/search?pattern=скамья
```
- `скамья` — search query


## Debug API
Methods for raw Notion data debugging

### Get raw metadata
Returns page metadata in Notion format

```
https://guides-api.ekaterinburg.city/api/test/retrieve?id=5604e0725f794708b9094b7ce49a46f7
```
- `5604e0725f794708b9094b7ce49a46f7` — Notion page id

### Get raw content
Returns page content in Notion format

```
https://guides-api.ekaterinburg.city/api/test/children?id=5604e0725f794708b9094b7ce49a46f7
```
- `5604e0725f794708b9094b7ce49a46f7` — Notion page id

> TODO: describe `dbretrieve` & `dbchildren` methods

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


3. Create static volume folder
> TODO: create folder automatically in project folder (the folder path must be contained in `.gitignore`)
```sh
mkdir /usr/local/docker/manuals-static-volume/
```


4. Run database migrations
```sh
docker compose exec manuals python manage.py migrate
```

5. Configure admin panel

    5.1 To collect Django static for pretty admin
    ```
    docker compose exec manuals python manage.py collectstatic
    ```

    5.2 _(optional)_ Create Django user to view Database in `https://<site-url>/admin`
    ```
    docker compose exec manuals python manage.py createsuperuser
    ```

6. Run Django & Telegram bot
```sh
docker compose up -d --build
```

7. Send message to Telegram bot to force update
```
/update -f
```
