# Система рекомендаций на основе графов

Проект демонстрирует работу рекомендательной системы использующей алгоритмы графов для поиска рекомендаций на основе 
поведения пользователя в прошлом. За основу взят небольшой фрагмент датасета: 
https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm, 
выбраны 5 самых популярных треков из 5 самых популярных жанров. Связи я старался подобрать таким образом,
чтобы пользователи не имели повторяющися предпочтений в жанрах, но есть довольно выраженный кластер.
Проблема холодного старта решается демонстрацией рекомендаций на основе pagerank - таким образом мы предполагаем 
что самые прослушиваемые треки имеют больше всего связей. Затем, когда пользователь указывает предпочтения либо выбирает 
трек из рекомендованных вычисляется метрика схожести пользователей из базы данных по отношению к текущему, отбираются 
3 самых близких и рекомендации делаются на основе тех треков что прослушивали эти 3 самых похожих по предпочтениям 
пользователя - k-nearest neighbors. Если же пользователь укажет предпочтения (жанр), то в первую очередь будут 
выводиться треки предпочитаемых жанров. На любом этапе набор рекомендованных треков отсортирован по pagerank.


## Tech Stack

- django
- postgresql
- networkx
- html
- Bootstrap


## Запуск

- перед запуском указать параметры подключения к бд в файле .env

клонировать репозиторий

```sh
git@github.com:UltimaKIND/Graph-based-recomendation-system.git
```

перейти в папку с проектом

```sh
  cd Graph-based-recomendation-system
```

установить зависимости

```sh
  poetry install
```

активировать виртуальное окружение

```sh
  poetry shell
```

накатить миграции на базу данных

```sh
  python3 manage.py migrate
```

наполнить бд данными

```sh
  python3 manage.py fill
```

Start the server

```sh
  python3 manage.py runserver
```