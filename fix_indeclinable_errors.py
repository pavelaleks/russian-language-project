#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def fix_indeclinable_errors(input_json_path, output_json_path):
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words = len(words_data)
    print(f"Всего слов в корпусе: {total_words}")

    # Слова, которые ошибочно помечены как несклоняемые, но должны быть 2-го склонения
    words_to_fix = {
        'правительство': '2nd',  # средний род на -ство
        'государство': '2nd',    # средний род на -ство
        'доверие': '2nd',        # средний род на -ие
        'пространство': '2nd',   # средний род на -ство
        'понятие': '2nd',        # средний род на -ие
        'отождествление': '2nd', # средний род на -ие
        'варьирование': '2nd',   # средний род на -ие
        'влияние': '2nd',        # средний род на -ие
        'признание': '2nd',      # средний род на -ие
        'расширение': '2nd',     # средний род на -ие
        'разоблачение': '2nd',   # средний род на -ие
        'следствие': '2nd',      # средний род на -ие
        'введение': '2nd',       # уже исправлено, но для полноты
    }

    # Действительно несклоняемые слова (заимствованные, аббревиатуры и т.д.)
    truly_indeclinable = {
        'биеннале', 'кино', 'кафе', 'метро', 'такси', 'меню', 'пальто', 'кофе',
        'какао', 'кашне', 'пенсне', 'монпансье', 'конферансье', 'атташе',
        'портмоне', 'резюме', 'алоэ', 'какаду', 'кенгуру', 'шимпанзе'
    }

    fixed_count = 0
    kept_indeclinable = 0

    for word, features in words_data.items():
        if features.get('declension') == 'indeclinable':
            if word in words_to_fix:
                # Исправляем ошибочно помеченные слова
                features['declension'] = words_to_fix[word]
                print(f"✅ Исправлено: {word} -> {words_to_fix[word]} склонение")
                fixed_count += 1
            elif word in truly_indeclinable:
                # Оставляем действительно несклоняемые
                print(f"✅ Оставлено несклоняемым: {word}")
                kept_indeclinable += 1
            else:
                # Проверяем по окончаниям
                if word.endswith(('ие', 'ье', 'ство', 'ение', 'ание', 'ение')):
                    # Скорее всего 2-е склонение
                    features['declension'] = '2nd'
                    print(f"✅ Автоисправление по окончанию: {word} -> 2-е склонение")
                    fixed_count += 1
                else:
                    print(f"❓ Неопределено: {word} (оставляем несклоняемым)")

    print(f"\nИсправления завершены!")
    print(f"Исправлено слов: {fixed_count}")
    print(f"Оставлено несклоняемыми: {kept_indeclinable}")

    # Сохраняем исправленный корпус
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"Исправленный корпус сохранен в {output_json_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python fix_indeclinable_errors.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    fix_indeclinable_errors(input_json, output_json)
