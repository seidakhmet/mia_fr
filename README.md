# Настройки через .env 

### Обязательные переменные
``` toml
SECRET_KEY=**SECRET_KEY**  # Секретный ключ
DB_USER=**DB_USER**  # Пользователь базы данных
DB_PASSWORD=**DB_PASSWORD**  # Пароль пользователя базы данных
DB_NAME=**DB_NAME**  # Наименование базы данных
CSRF_TRUSTED_ORIGINS=https://127.0.0.1:20000, http://127.0.0.1:20000, https://localhost:20000, http://localhost:20000  # Доверенные адреса для CSRF проверки
```

**CSRF_TRUSTED_ORIGINS** - сюда прописываете все адреса по которым будут обращаться на текущее приложение из внешних источников. Например, если в какой-то сети адрес сервера 192.168.1.1, то в `.env` файле это поле должно выглядеть так: 
``` toml
CSRF_TRUSTED_ORIGINS=https://127.0.0.1:20000, http://127.0.0.1:20000, https://localhost:20000, http://localhost:20000, https://192.168.1.1:20000, http://192.168.1.1:20000
```
Адреса разделяются через ```, ``` (*запятая + пробел*). В конце строки не должно быть никаких добавочных символов в виде слэша, пробела и т.п.

### Необязательные переменные
``` toml
APP_NAME=mia_fr_back  # Название приложения
DB_HOST=db  # IP адрес базы данных
DB_PORT=5432  # Порт базы данных
REDIS_HOST=redis  # IP адрес Redis
REDIS_PORT=6379  # Порт Redis
RABBIT_HOST=rabbitmq  # IP адрес RabbitMQ
RABBIT_PORT=5672  # Порт RAbbitMQ
DS_HOST=111.111.0.1  # IP адрес аналитической системы (здесь внутри идёт своя сеть с настройкой ipam subnet 111.111.0.0/24)
DS_PORT=9999  # Порт аналитической системы
DJANGO_SETTINGS_MODULE=config.settings.production  # Режим запуска приложения (по умолчанию production, для дебага development)
```
 