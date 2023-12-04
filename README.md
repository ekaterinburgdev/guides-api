# guides-api

📗 Python back-end app for Guides

- HTTP API for [Ekaterinburg guides website](https://github.com/ekaterinburgdev/guides)
- Notion data cacher. Static files downloader and optimizer
- Database viewer in Admin panel
- Telegram bot updater 

**[guides-api.ekaterinburg.city](https://guides-api.ekaterinburg.city)**


## API

### Pages list

Get urls list and metadata of all guides

```
https://guides-api.ekaterinburg.city/api/tree
```

### Guide

Get guide data `/<manual-name>`
```
https://guides-api.ekaterinburg.city/api/content/street-name-plates
```

### Guide page

Get guide page data `/<manual-name>/<page-name>`
```
https://guides-api.ekaterinburg.city/api/content/street-name-plates/general-provisions
```


### Search

Get search results on pages by query

- `скамья` — search query
```
https://guides-api.ekaterinburg.city/api/search?pattern=скамья
```


## Debug API

Methods for raw Notion data debugging

### Raw metadata

Get guide page metadata in Notion format

- `5604e0725f794708b9094b7ce49a46f7` — Notion page id
```
https://guides-api.ekaterinburg.city/api/test/retrieve?id=5604e0725f794708b9094b7ce49a46f7
```

### Raw content

Get guide page content in Notion format

- `5604e0725f794708b9094b7ce49a46f7` — Notion page id
```
https://guides-api.ekaterinburg.city/api/test/children?id=5604e0725f794708b9094b7ce49a46f7
```

## Telegram bot

The site is managed via a Telegram bot

`/update` — update content

`/update -f` — force update (rebuild tree, reload images etc.)


## Development

1. Install [Docker](https://docs.docker.com/get-docker/)


2. Create `manuals/.env` file from [`manuals/.env.example`](https://github.com/ekaterinburgdev/guides-api/blob/main/manuals/.env.example) with secrets
    - Notion token
    - Django settings
    - PostgreSQL settings
    - Telegram (bot token from [@BotFather](https://telegram.me/BotFather) and master chat id from [@userinfobot](https://t.me/userinfobot)).

3. Create static volume folder
    ```sh
    mkdir /usr/local/docker/manuals-static-volume/
    ```
    > TODO: create folder automatically in project folder (the folder path must be contained in `.gitignore`)

4. Run database migrations
    ```sh
    docker compose exec manuals python manage.py migrate
    ```

5. Configure admin panel `https://<site-url>/admin`

    5.1. Build Django static for admin panel
    ```sh
    docker compose exec manuals python manage.py collectstatic
    ```
    
    5.2. _(optional)_ Create Django user to view DB 
    ```sh
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
