# -*- coding: utf-8 -*-

def distribute_funds(fund: int, places: int, distribution_ratio: float = 0.8):
    # Подсчёт суммы геометрической прогрессии
    progression_sum = (1 - distribution_ratio ** places) / (1 - distribution_ratio)

    # Подсчёт первого члена прогрессии
    first_prize = fund / progression_sum

    # Генерация результатов
    for i in range(places):
        yield first_prize * (distribution_ratio ** i)


names: dict[int, str] = {
    1: 'Дмитрий',
    2: 'Farel',
    3: 'Игорь',
    4: 'ambienthugg',
    5: 'Женьчик',
    6: 'Работает Артур',
    7: 'Vladimir',
    8: 'CHVS',
    9: 'Honex',
    10: 'Kirill Usenko',
    11: 'Jesus',
    12: 'Споки | 1k ROI',
    13: 'Tony',
    14: 'Влад',
    15: 'Сергей',
    16: 'Kartright',
    17: 'Jesus',
    18: 'Yankee',
    19: 'Igor',
    20: 'Un/tilt/ed'
}


# Print the prizes
print('--- Fund distribution TEST ---')
for place, prize in enumerate(distribute_funds(20_000, 20), start=1):
    print(f"{place}. {names[place]} — %i баллов — {prize:.2f}₽")
