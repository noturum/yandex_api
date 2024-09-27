Тестовое задание для https://docs.google.com/document/d/1LPFktOxgFiV1A7KU-mq44FnEt-ykeKK1-4Yv40BsXho/edit?pli=1

Веб приложение на Flask , которое взаимодействует с API Яндекс.Диска

Для запуска сервера нужно собрать контейнер.
``` bash
docker-compose  up --build
```
Реализованны следующие функции:

    1.загрузка файлов из публичных файлов
    2. мульти выбор файлов для скачивания
    3. кеширование списка файлов для запроса
