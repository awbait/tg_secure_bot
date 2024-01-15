
## Настройка подключения в Google Api Console

Переходим по ссылке:
[Google Cloud Platform](https://console.developers.google.com/)
 ![](https://i.imgur.com/IvjNFSf.png)

Введите имя проекта
![](https://i.imgur.com/RNlzUpG.png)

Если у вас уже есть проекты, выберите только что созданный.
![](https://i.imgur.com/aw1p2y2.png)

В меню слева выберите “Marketplace”
![](https://i.imgur.com/YlUX1MO.png)

В поле поиска введите “Google Drive api” и нажмите на Enter.
![](https://i.imgur.com/E8q5N3W.png)

Кликните на Google Drive API
![](https://i.imgur.com/KfbL9MP.png)

На открывшейся странице нажмите “Enable”.
![](https://i.imgur.com/yTQXqiK.png)

Повторите эти же шаги (начиная с момента, когда вы заходите в marketplace) но в поиске введите Google Sheets API, перейдите в него и нажмите Enable.

Затем зайдите в пункт меню “APIs & Services”.
![](https://i.imgur.com/wbGoN0z.png)

Слева в меню перейдите в “Credentials”. Нажмите на “Create Credentials”, в открывшемся меню выберите пункт Service account.
![](https://i.imgur.com/9Zs1C2Y.png)

Откроется страница создания аккаунта. Введите имя и нажмите “Create”
![](https://i.imgur.com/uIju8Oq.png)

В поле “Select Role” выберите “Editor”. Затем нажмите Continue.
![](https://i.imgur.com/n54FUJA.png)

Нажмите Done.
![](https://i.imgur.com/x5bFcpe.png)

Кликаем на только что созданный аккаунт.
![](https://i.imgur.com/ho0mvW6.png)

Переходим во вкладку KEYS. Жмем на ADD KEY. В появившемся меню выбираем Create new key.
![](https://i.imgur.com/5YfavX0.png)

Выбираем JSON и жмем CREATE.
![](https://i.imgur.com/wvD3IaG.png)

Скачиваем json файл на свой компьютер.
Переходим во вкладку Details, копируем Email.
![](https://i.imgur.com/gK7dDbd.png)

Переходим в таблицу, к которой у вас будет доступ. Жмем “Настройки доступа”, вводим скопированный Email и жмем “Готово”.
![](https://i.imgur.com/jWpxqWH.png)

После этого вам будет предложено выбрать роль, выберите “Редактор”.

Файл json вы должны переименовать в credentials.json и положить в папку рядом с файлом docker-compose.yaml

## Основные параметры для настройки

Настройки прописываются в файл docker-compose.yml в разделе environment

SСHEDULE_TIME - Время в которое будет проводится сканирование.

**Google**:
GSPREAD_NAME - Название таблицы
GSPREAD_CREDENTIALS_JSON_FILE - 

**Telegram**:
TG_API_ID и TG_API_HASH - можно получить тут - https://my.telegram.org/
TG_BOT_TOKEN - Токен бота получаем у BotFather
TG_ADMIN_CHANNEL_ID - ID чата Администраторов
## Запуск / Перезапуск

Для запуска, нам необходимо положить файл docker-compose.yml и рядом файл credentials.json, который мы получили выше.

Запуск
```bash
docker-compose up -d
```

Рестарт
```bash
docker-compose restart
```

Остановить
```bash
docker-compose down
```

## Команда получения ID канала

/get_id - Позволяет получить ID канала

## Пример Google таблицы сотрудников и модерируемых чатов

Пример доступен по ссылке: [TREND\_SECURITY - Google Таблицы](https://docs.google.com/spreadsheets/d/1rsoJNtIF5RIyWs08zbRhzehVzLYG6psSIEAnC07DUNQ/edit#gid=0)

В данной таблице присутствуют два листа, в первом Employees мы прописываем всех наших сотрудников. Во втором Chats прописываем ID наших чатов, которые мы будем модерировать (ID можно получить выполнив команду /get_id в чате в который вы добавили бота и **выдали права администратора**).
