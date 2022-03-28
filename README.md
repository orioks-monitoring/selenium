# ОРИОКС Мониторинг Selenium

*Существует [Бот](https://github.com/orioks-monitoring/bot) - усовершенствованная и самая полная версия настоящего скрипта, подходящая для широкого круга пользователей*


## Описание
Скрипт для мониторинга информации с сайта [orioks.miet.ru](https://orioks.miet.ru/). Автоматическая отправка уведомления при изменениях через [API VK](https://dev.vk.com/) или [API Telegram](https://core.telegram.org/bots/api). Подразумевается, что скрипт работает на бесплатном сервисе от [GitHub Actions](https://github.com/features/actions), поэтому для хранения данных пользователя используется [API Yandex Disk](https://yandex.ru/dev/disk/rest/).

Скрипт запускается каждые 15 минут[^1] и сравнивает данные, хранящиеся на [Яндекс Диске](https://disk.yandex.ru/), с информацией от драйвера браузера [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/).

_P.S. Существует [скрипт](https://github.com/llirrikk/orioks-monitoring-api/), работающий на основе [ORIOKS STUDENT **API**](https://orioks.gitlab.io/student-api/), но его использование не рекомендуется[^2]._


## Использование

1. Получение [API токена от Yandex Disk](https://yandex.ru/dev/oauth/)
    1. Переходим по [ссылке](https://oauth.yandex.ru/client/new).
        - *Название приложения*:	`ЛЮБОЕ`.
        - *Платформы*: `"Веб-сервисы"` -> `"Подставить URL для разработки"` -> Кнопка `"Добавить"`.
        - *Доступы*: Выбираем `"Яндекс.Диск REST API"` -> `"Доступ к папке приложения на Диске"`.
        - Нажимаем кнопку `"Создать приложение"`.
    2. Переходим по ссылке, заменяя последнюю часть: 
        https://oauth.yandex.ru/authorize?response_type=token&client_id=ИДЕНТИФИКАТОР_ПРИЛОЖЕНИЯ
    3. Нажимаем кнопку `"Войти как ..."`.
    4. Запоминаем `YANDEX_DISK_API_TOKEN` токен Яндекс Диска.


2. [^3]Получение [API токена от паблика VK](https://dev.vk.com/)
    1. Создание группы ВК
        - Выбираем `"Группа по интересам"`.
        - *Название*: `ЛЮБОЕ`.
        - *Тип группы*: `Частная`.
        - *Тематика*: `Образование`.
        - Нажимаем кнопку `"Создать сообщество"`.
    2. Нажимаем кнопку `"Управление"`.
        - *Сообщения* -> *Сообщения сообщества*: `Включены`.
        - *Сообщения* -> *Настройки для бота* -> *Возможности ботов*: `Включены`.
        - *Настройки* -> *Работа с API* -> *Ключи доступа* -> *Создать ключ* -> `Разрешить приложению доступ к сообщениям сообщества`.
        - Запоминаем `VK_API_TOKEN` токен ВК группы.
        - Пишем любое сообщение этой группе с аккаунта ВК, на который хотите получать уведомления.
    3. Узнаём свой *VK ID*:
        1. Например, используя [этот](https://regvk.com/id/) сайт.
        2. Запоминаем `VK_PEER_ID` свой *VK ID*.


3. [^3]Получение [API токена для Telegram бота](https://core.telegram.org/bots/api)
    1. Пишем `/newbot` сюда: [@BotFather](https://t.me/botfather).
    2. Запоминаем `TG_API_TOKEN` токен Telegram бота.
    3. Узнаём свой *Telegram ID*, например, так:
        1. Пишем `/start` сюда: [@userinfobot](https://t.me/userinfobot).
        2. Запоминаем `TG_CHAT_ID` свой *Telegram ID*.


4. Настройка выполнения скрипта на [GitHub Actions](https://github.com/features/actions).
    1. Сделать **Fork** [репозитория](https://github.com/llirrikk/orioks-monitoring-selenium).
    2. Включить **Actions** в репозитории своего профиля, нажав на кнопку: *I understand my workflows, go ahead and enable them*, затем на кнопку *Enable workflow*.
    3. Перейти в *Settings* -> *Secrets* -> *Actions* -> *New repository secret* и добавить значения: 
        - `ORIOKS_LOGPASS_LOGIN` (логин ОРИОКС), `ORIOKS_LOGPASS_PASSWORD` (пароль ОРИОКС),
        - `YANDEX_DISK_API_TOKEN`,
        - `VK_API_TOKEN`, `VK_PEER_ID` и/или[^3] `TG_API_TOKEN`, `TG_CHAT_ID`,
        - `VK_USE` (*True*, если использовать сервис ВК, *False* -- в противном случае),
        - `TG_USE` (*True*, если использовать сервис Telegram, *False* -- в противном случае).



[^1]: > Выполнение может быть отложено в периоды высокой загрузки рабочих процессов GitHub Actions... Самый короткий интервал, с которым вы можете запускать запланированные рабочие процессы, — [каждые 15 минут](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule).

[^2]: [ORIOKS STUDENT API](https://orioks.gitlab.io/student-api/) имеет ряд ограничений (не позволяет получить всю необходимую информацию), поэтому рекомендуется использовать скрипт из настоящего репозитория, вместо [скрипта, использующего API](https://github.com/llirrikk/orioks-monitoring).

[^3]: Необходимо выбрать хотя бы один сервис: [ВКонтакте](https://vk.com/) или [Telegram](https://telegram.org/) (то есть выбрать 2 или 3 пункт, либо и 2, и 3).
