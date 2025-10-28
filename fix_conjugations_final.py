#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def fix_conjugations_final(input_json_path, output_json_path):
    """
    Исправляет спряжения глаголов согласно ТОЧНОМУ алгоритму русского языка
    """
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words = len(words_data)
    print(f"Всего слов в корпусе: {total_words}")

    fixed_count = 0
    
    # ТОЧНЫЙ алгоритм определения спряжения согласно правилам русского языка
    
    # 1-е спряжение: инфинитивы на -ать, -ять, -ыть, -уть, -оть, -ти, -чь
    # + исключения из -ить: брить, стелить (стлать), зиждиться
    first_conjugation_endings = ['ать', 'ять', 'ыть', 'уть', 'оть', 'ти', 'чь']
    first_conjugation_ite_exceptions = ['брить', 'стелить', 'стлать', 'зиждиться']
    
    # 2-е спряжение: инфинитивы на -ить (кроме исключений из 1-го)
    # + исключения из -ать, -еть: слышать, дышать, держать, гнать, терпеть, вертеть, 
    # обидеть, зависеть, ненавидеть, видеть, смотреть
    second_conjugation_exceptions = [
        'слышать', 'дышать', 'держать', 'гнать', 'терпеть', 'вертеть',
        'обидеть', 'зависеть', 'ненавидеть', 'видеть', 'смотреть'
    ]
    
    # Разноспрягаемые глаголы
    heteroclitic_verbs = ['есть', 'дать', 'хотеть', 'бежать', 'брезжить']

    print("Начинаем исправления спряжений по ТОЧНОМУ алгоритму...")
    
    for word, features in words_data.items():
        if features.get('pos') != 'VERB':
            continue
            
        original_conjugation = features.get('conjugation')
        mood = features.get('mood')
        
        # Определяем спряжение по алгоритму
        conjugation = None
        
        # Шаг 6: Разноспрягаемые глаголы (приоритет)
        if word in heteroclitic_verbs:
            conjugation = 'heteroclitic'
        
        # Шаг 1-2: Проверяем ударные окончания в 3 лице
        elif mood == 'INDICATIVE' and word.endswith(('ет', 'ёт', 'ит', 'ат', 'ят', 'ут', 'ют')):
            # Ударные окончания: Е(Ё), У, Ю – 1 спр., И, А, Я – 2 спр.
            if word.endswith(('ет', 'ёт', 'ут', 'ют')):
                conjugation = '1st'
            elif word.endswith(('ит', 'ат', 'ят')):
                conjugation = '2nd'
        
        # Шаг 3-4: Если окончание безударное, проверяем инфинитив
        elif mood == 'INFINITIVE':
            # 4А: 1-е спряжение
            if (any(word.endswith(ending) for ending in first_conjugation_endings) or 
                word in first_conjugation_ite_exceptions):
                conjugation = '1st'
            # 4Б: 2-е спряжение
            elif (word.endswith('ить') and word not in first_conjugation_ite_exceptions) or word in second_conjugation_exceptions:
                conjugation = '2nd'
        
        # Шаг 5: Учитываем приставку вы-
        elif word.startswith('вы') and len(word) > 3:
            # Отбрасываем приставку вы- и проверяем корень
            root = word[2:]  # убираем "вы"
            if root.endswith(('ет', 'ёт', 'ут', 'ют')):
                conjugation = '1st'
            elif root.endswith(('ит', 'ат', 'ят')):
                conjugation = '2nd'
        
        # Дополнительная проверка по формам
        else:
            # Проверяем по окончаниям форм
            if word.endswith(('ет', 'ёт', 'ут', 'ют', 'ешь', 'ёшь', 'ете', 'ёте', 'ем', 'ём')):
                conjugation = '1st'
            elif word.endswith(('ит', 'ат', 'ят', 'ишь', 'ите', 'им')):
                conjugation = '2nd'
        
        # Применяем исправление
        if conjugation and original_conjugation != conjugation:
            features['conjugation'] = conjugation
            print(f"  {word}: {original_conjugation} -> {conjugation} ({mood})")
            fixed_count += 1
        elif conjugation is None and original_conjugation is None:
            # Для глаголов, которые не удалось классифицировать
            if word.endswith(('ать', 'ять', 'ыть', 'уть', 'оть', 'ти', 'чь')):
                features['conjugation'] = '1st'
                print(f"  {word}: None -> 1st (по умолчанию)")
                fixed_count += 1
            elif word.endswith('ить'):
                features['conjugation'] = '2nd'
                print(f"  {word}: None -> 2nd (по умолчанию)")
                fixed_count += 1

    print(f"\nИсправления завершены!")
    print(f"Исправлено спряжений: {fixed_count}")

    # Сохраняем исправленный корпус
    output_data = {
        "metadata": {
            "source": "OpenCorpora (Исправленный - финальный алгоритм спряжений)",
            "version": corpus['metadata']['version'],
            "revision": "corrected_conjugations_final",
            "total_words": total_words,
            "words": words_data
        }
    }

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Исправленный корпус сохранен в {output_json_path}")

    # Проверяем результаты
    print(f"\nПроверяем результаты в {output_json_path}...")
    with open(output_json_path, 'r', encoding='utf-8') as f:
        fixed_corpus = json.load(f)
    
    conjugation_counts = {}
    for word, features in fixed_corpus['metadata']['words'].items():
        if features.get('pos') == 'VERB':
            conjugation = features.get('conjugation')
            conjugation_counts[conjugation] = conjugation_counts.get(conjugation, 0) + 1
    
    print("Распределение по спряжениям:")
    for conjugation, count in sorted(conjugation_counts.items(), key=lambda x: (x[0] is None, x[0])):
        print(f"  {conjugation}: {count} глаголов")
    
    # Проверяем конкретные примеры
    test_verbs = {
        '1-е спряжение (правильно)': ['выпить', 'уничтожить', 'работать', 'писать', 'жить'],
        '2-е спряжение (правильно)': ['дышать', 'слышать', 'держать', 'гнать', 'терпеть', 'вертеть', 'обидеть', 'зависеть', 'ненавидеть', 'видеть', 'смотреть'],
        'Разноспрягаемые': ['есть', 'дать', 'хотеть', 'бежать', 'брезжить']
    }
    
    print("\nПроверка конкретных примеров:")
    for conjugation_type, verbs in test_verbs.items():
        print(f"\n{conjugation_type}:")
        for verb in verbs:
            if verb in fixed_corpus['metadata']['words']:
                features = fixed_corpus['metadata']['words'][verb]
                conjugation = features.get('conjugation')
                mood = features.get('mood')
                print(f"  {verb}: {conjugation} ({mood})")
            else:
                print(f"  {verb}: не найдено в корпусе")
    
    print(f"\n✅ Успешно исправлено {fixed_count} спряжений!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python fix_conjugations_final.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    fix_conjugations_final(input_json, output_json)
