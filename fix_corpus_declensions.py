#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления ошибок классификации склонений в корпусе OpenCorpora
"""

import json
import sys

def fix_declensions(input_file, output_file):
    """
    Исправляет ошибки классификации склонений в корпусе
    """
    print(f"Загружаем корпус из {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    
    words = corpus['metadata']['words']
    total_words = len(words)
    
    print(f"Всего слов в корпусе: {total_words}")
    
    # Статистика исправлений
    corrections = {
        'masculine_to_2nd': 0,  # Мужские слова с нулевым окончанием -> 2-е склонение
        'heteroclitic': 0,      # Разносклоняемые
        'indeclinable': 0,      # Несклоняемые
        'feminine_3rd': 0,      # Женские на -ь -> 3-е склонение
        'total': 0
    }
    
    # Разносклоняемые существительные
    heteroclitic_words = {
        'путь', 'время', 'имя', 'племя', 'знамя', 'пламя', 
        'стремя', 'темя', 'семя', 'бремя', 'вымя'
    }
    
    # Несклоняемые существительные (иностранные слова, имена собственные)
    indeclinable_words = {
        'самоа', 'манчестер', 'кофе', 'пальто', 'кино', 'метро', 
        'такси', 'меню', 'кафе', 'ателье', 'пенсне', 'кашне',
        'пари', 'реле', 'шоссе', 'алоэ', 'какао', 'пианино',
        'радио', 'видео', 'аудио', 'фото', 'авто', 'мото',
        'домино', 'казино', 'лото', 'бюро', 'депо', 'фойе',
        'пальто', 'манто', 'боа', 'кенгуру', 'шимпанзе', 'какаду',
        'фламинго', 'какао', 'кофе', 'какао', 'шоссе', 'метро'
    }
    
    print("Начинаем исправления...")
    
    for word, features in words.items():
        if features.get('pos') != 'NOUN':
            continue
            
        original_declension = features.get('declension')
        gender = features.get('gender')
        
        # 1. Разносклоняемые существительные
        if word in heteroclitic_words:
            if original_declension != 'heteroclitic':
                features['declension'] = 'heteroclitic'
                corrections['heteroclitic'] += 1
                corrections['total'] += 1
                print(f"  {word}: {original_declension} -> heteroclitic")
        
        # 2. Несклоняемые существительные
        elif word in indeclinable_words:
            if original_declension != 'indeclinable':
                features['declension'] = 'indeclinable'
                corrections['indeclinable'] += 1
                corrections['total'] += 1
                print(f"  {word}: {original_declension} -> indeclinable")
        
        # 3. Мужские существительные с нулевым окончанием = 2-е склонение
        elif (gender == 'MASCULINE' and 
              not word.endswith('а') and not word.endswith('я') and 
              original_declension == '1st'):
            features['declension'] = '2nd'
            corrections['masculine_to_2nd'] += 1
            corrections['total'] += 1
            if corrections['masculine_to_2nd'] <= 10:  # Показываем только первые 10
                print(f"  {word}: 1st -> 2nd (муж.р. без -а/-я)")
        
        # 4. Женские существительные на мягкий знак = 3-е склонение
        elif (gender == 'FEMININE' and 
              word.endswith('ь') and 
              original_declension != '3rd'):
            features['declension'] = '3rd'
            corrections['feminine_3rd'] += 1
            corrections['total'] += 1
            if corrections['feminine_3rd'] <= 10:  # Показываем только первые 10
                print(f"  {word}: {original_declension} -> 3rd (жен.р. на -ь)")
    
    print(f"\nИсправления завершены!")
    print(f"Статистика исправлений:")
    print(f"  Мужские слова с нулевым окончанием -> 2-е склонение: {corrections['masculine_to_2nd']}")
    print(f"  Разносклоняемые: {corrections['heteroclitic']}")
    print(f"  Несклоняемые: {corrections['indeclinable']}")
    print(f"  Женские на -ь -> 3-е склонение: {corrections['feminine_3rd']}")
    print(f"  ВСЕГО исправлений: {corrections['total']}")
    
    # Сохраняем исправленный корпус
    print(f"\nСохраняем исправленный корпус в {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"Готово! Исправленный корпус сохранен в {output_file}")
    
    return corrections

def verify_corrections(corpus_file):
    """
    Проверяет результаты исправлений
    """
    print(f"\nПроверяем результаты в {corpus_file}...")
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    
    words = corpus['metadata']['words']
    
    # Подсчитываем распределение по склонениям
    declension_counts = {}
    gender_declension_counts = {}
    
    for word, features in words.items():
        if features.get('pos') != 'NOUN':
            continue
            
        declension = features.get('declension', 'unknown')
        gender = features.get('gender', 'unknown')
        
        declension_counts[declension] = declension_counts.get(declension, 0) + 1
        
        key = f"{gender}_{declension}"
        gender_declension_counts[key] = gender_declension_counts.get(key, 0) + 1
    
    print("Распределение по склонениям:")
    for declension, count in sorted(declension_counts.items(), key=lambda x: (x[0] is None, x[0])):
        print(f"  {declension}: {count} слов")
    
    print("\nРаспределение по полу и склонению:")
    for key, count in sorted(gender_declension_counts.items(), key=lambda x: (x[0] is None, x[0])):
        print(f"  {key}: {count} слов")
    
    # Проверяем несколько примеров
    print("\nПримеры исправленных слов:")
    examples = ['совладелец', 'автор', 'путь', 'время', 'самоа', 'кофе', 'ночь']
    for word in examples:
        if word in words:
            features = words[word]
            print(f"  {word}: {features.get('gender')} {features.get('declension')}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python fix_corpus_declensions.py <input_file> <output_file>")
        print("Пример: python fix_corpus_declensions.py opencorpora_no_ambig.json opencorpora_fixed.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        corrections = fix_declensions(input_file, output_file)
        verify_corrections(output_file)
        
        print(f"\n✅ Успешно исправлено {corrections['total']} слов!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
