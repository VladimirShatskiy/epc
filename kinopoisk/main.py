import json
from pprint import pprint

import requests

KEY = '8YC57R3-82Y49DQ-HAG53NJ-8KT967Y'

headers = {"X-API-KEY": KEY}


def out_info(data, file_name: str) -> None:
    pprint(data, indent=4)
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=True)


def movie_random() -> None:

    response = requests.get(
        'https://api.kinopoisk.dev/v1/movie/random',
        headers=headers
    )

    out_info(data=response.json(), file_name='случайный фильм.txt')


def info_about() -> None:
    try:
        film_id = int(input("\nВведите ID фильма для поиска "))
    except ValueError:
        print("Номер ID должен быть числовым")
        return

    response = requests.get(
        f'https://api.kinopoisk.dev/v1/movie/{film_id}',
        headers=headers
    )

    data = response.json()

    if 'message' in data:
        print('\nПо заданному ID фильма не обнаружено \n')
        return

    out_info(data=data, file_name=f'о фильме {film_id}.txt')


def all_season() -> None:

    try:
        film_id = int(input("\nВведите ID фильма для поиска сезонов "))
    except ValueError:
        print("Номер ID должен быть числовым")
        return

    response = requests.get(
        'https://api.kinopoisk.dev/v1/season',
        params={
            "movieId": film_id,
        },
        headers=headers
    )
    data = response.json()
    if not data['docs']:
        print(f'По указанному {film_id} сериалов нет')
        return

    out_info(data=data, file_name=f'сезоны фильма {film_id}.txt')


def reviews() -> None:

    try:
        film_id = int(input("\nВведите ID фильма для поиска отзывов "))
    except ValueError:
        print("Номер ID должен быть числовым")
        return

    response = requests.get(
        'https://api.kinopoisk.dev/v1/review',
        params={
            "movieId": film_id,
        },
        headers=headers
    )
    print(response)
    data = response.json()

    if not data['docs']:
        print(f'По указанному {film_id} отзывов нет')
        return

    out_info(data=data, file_name=f'Отзывы о  {film_id}.txt')


def main_menu():

    while True:
        print('\n'
              '1: Выбрать из базы рандомный фильм\n'
              '2: Получить всю информацию о фильме\n'
              '3: Получить все сезоны и эпизоды:\n'
              '4: Отзывы пользователей:\n'
              '0: Выход')
        try:
            n_menu = int(input('Выбери пункт меню '))
        except ValueError:
            print("\nОшибка: Необходимо указать число")
            continue

        if n_menu == 0:
            break
        elif n_menu == 1:
            movie_random()
        elif n_menu == 2:
            info_about()
        elif n_menu == 3:
            all_season()
        elif n_menu == 4:
            reviews()
        else:
            print("Пока нет такого выбора, повторите попытку")


if __name__ == "__main__":
    main_menu()
