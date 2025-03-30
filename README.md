<h1>Инструкции по запуску</h1>

**Перед запуском убедитесь в том, что у вас установлены:**
  - **[Docker](https://docs.docker.com/engine/install/)**
  - **[Docker Compose](https://docs.docker.com/compose/install/)**
  - **[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)**

Для первого запуска просто скопируйте в терминал следующее:
```shell
git clone https://github.com/rexxless/buywithease_api.git
cd buywithease_api/deploy
docker compose up --build
```
Для всех последующих запусков достаточно скопировать в терминал следующее:
```shell
cd buywithease_api/deploy
docker compose up
```
