# Stock Market API

## Description
A little bit stock market API (simple). The intention of this project is provide
a simple way for accesing to stock market information. The stock market information

## Denpendencies
- Docker version: 24.0.2 or upper
- Environment ubuntu 22.04

## How to run the server

From project home folder, invoke the script ./scripts/start.sh. The api will be 
available on localhost:8000.
For accesing to API swagger and perform some validations you can try: http://localhost:8000/docs

NOTE: environment uses a docker compose version where compose is integrated to docker itself. 
So if you are using older versions, change "docker compose" by "docker-compose" on 
start.sh and stop.sh scripts

## How to stop the server
For stopping the server and databases execute: ./scripts/stop.sh from project home folder.

## Settings
In order to modify settings you can edit .env file at project home.
The following settings are available:

- POSTGRES_SERVER: database server name, string
- POSTGRES_USER: database user, string
- POSTGRES_PASSWORD: database password, string
- POSTGRES_DB: database url, string
- LOGLEVEL: Loglevel, ENUM (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- HOST: server host, string
- PORT: server port, int
- API_KEY_LENGTH: api key length in bytes, int
- STOCK_API_KEY: external stock api key, string
- DEBUG_MODE: server debug mode, bool
- LIMITER_RULE: Rule for throttling, string, format N/unit example: 5/minute
- ROOT_PATH: API root path, string

NOTE: settings are prepared to be executed in localhost:8000, if try something else
you have to change docker-compose.yml file for exporting the desidered port.