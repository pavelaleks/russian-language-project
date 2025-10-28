#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def fix_conjugations(input_json_path, output_json_path):
    """
    Исправляет спряжения глаголов согласно правилам русского языка
    """
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words = len(words_data)
    print(f"Всего слов в корпусе: {total_words}")

    fixed_count = 0
    
    # Правила определения спряжения глаголов
    # 1-е спряжение: глаголы на -ать, -ять, -еть (кроме исключений), -уть, -оть
    # 2-е спряжение: глаголы на -ить (кроме исключений), -еть (исключения), -ать (исключения)
    
    # Исключения для 2-го спряжения (глаголы на -ать, -еть, которые спрягаются как 2-е)
    second_conjugation_exceptions = {
        'дышать', 'слышать', 'держать', 'гнать', 'терпеть', 'обидеть', 'зависеть', 
        'ненавидеть', 'видеть', 'вертеть', 'обидеться', 'строить', 'любить', 
        'ненавидеть', 'терпеть', 'обидеть', 'зависеть', 'ненавидеть', 'смотреть',
        'говорить', 'слышать', 'дышать', 'держать', 'гнать', 'терпеть', 'обидеть',
        'зависеть', 'ненавидеть', 'видеть', 'вертеть', 'обидеться', 'строить'
    }
    
    # Исключения для 1-го спряжения (глаголы на -ить, которые спрягаются как 1-е)
    first_conjugation_exceptions = {
        'брить', 'стелить', 'зиждиться'
    }

    print("Начинаем исправления спряжений...")
    
    for word, features in words_data.items():
        if features.get('pos') != 'VERB':
            continue
            
        original_conjugation = features.get('conjugation')
        current_conjugation = original_conjugation
        
        # Определяем спряжение по окончанию инфинитива
        if word.endswith('ить'):
            if word in first_conjugation_exceptions:
                new_conjugation = '1st'
            else:
                new_conjugation = '2nd'
        elif word.endswith(('ать', 'ять', 'еть', 'уть', 'оть')):
            if word in second_conjugation_exceptions:
                new_conjugation = '2nd'
            else:
                new_conjugation = '1st'
        elif word.endswith('чь'):  # глаголы на -чь обычно 1-е спряжение
            new_conjugation = '1st'
        elif word.endswith('чься'):  # возвратные глаголы на -чься
            new_conjugation = '1st'
        else:
            # Для остальных случаев оставляем как есть или определяем по контексту
            continue
        
        # Применяем исправление только если оно отличается от текущего
        if current_conjugation != new_conjugation:
            features['conjugation'] = new_conjugation
            print(f"  {word}: {original_conjugation} -> {new_conjugation}")
            fixed_count += 1
            current_conjugation = new_conjugation
        
        # Если спряжение не было определено (None), устанавливаем его
        elif current_conjugation is None:
            features['conjugation'] = new_conjugation
            print(f"  {word}: None -> {new_conjugation}")
            fixed_count += 1

    print(f"\nИсправления завершены!")
    print(f"Исправлено спряжений: {fixed_count}")

    # Сохраняем исправленный корпус
    output_data = {
        "metadata": {
            "source": "OpenCorpora (Исправленный - склонения и спряжения)",
            "version": corpus['metadata']['version'],
            "revision": "corrected_conjugations",
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
    
    print(f"\n✅ Успешно исправлено {fixed_count} спряжений!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python fix_conjugations.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    fix_conjugations(input_json, output_json)
