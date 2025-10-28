#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для точной проверки и исправления классификации склонений в корпусе
"""

import json
import re

def determine_correct_declension(word, gender, pos):
    """
    Точное определение склонения на основе правил русского языка
    """
    if pos != 'NOUN':
        return None
    
    word_lower = word.lower()
    
    # 1-е склонение: муж.р. и жен.р. на -а/-я
    if word_lower.endswith(('а', 'я')):
        return '1st'
    
    # 3-е склонение: жен.р. на мягкий знак
    if word_lower.endswith('ь') and gender == 'FEMININE':
        return '3rd'
    
    # Разносклоняемые существительные
    heteroclitic_words = {
        'путь', 'время', 'имя', 'племя', 'знамя', 'пламя', 
        'стремя', 'темя', 'семя', 'бремя', 'вымя'
    }
    if word_lower in heteroclitic_words:
        return 'heteroclitic'
    
    # Несклоняемые существительные
    indeclinable_patterns = [
        # Иностранные слова на -о, -е, -и, -у, -ю
        r'[а-я]+[оеиую]$',
        # Слова на -и (многие иностранные)
        r'[а-я]+и$',
        # Слова на -у (некоторые иностранные)
        r'[а-я]+у$',
        # Слова на -ю (некоторые иностранные)
        r'[а-я]+ю$'
    ]
    
    indeclinable_words = {
        'кофе', 'пальто', 'кино', 'метро', 'такси', 'меню', 'кафе',
        'ателье', 'пенсне', 'кашне', 'пари', 'реле', 'шоссе', 'алоэ',
        'какао', 'пианино', 'радио', 'видео', 'аудио', 'фото', 'авто',
        'мото', 'домино', 'казино', 'лото', 'бюро', 'депо', 'фойе',
        'манто', 'боа', 'кенгуру', 'шимпанзе', 'какаду', 'фламинго',
        'самоа', 'манчестер', 'джозеф', 'кортни', 'ник', 'пабло',
        'ариэль', 'ольга', 'елена', 'александрия', 'минниханов'
    }
    
    if word_lower in indeclinable_words:
        return 'indeclinable'
    
    # Проверяем паттерны несклоняемых
    for pattern in indeclinable_patterns:
        if re.match(pattern, word_lower):
            return 'indeclinable'
    
    # 2-е склонение: муж.р. с нулевым окончанием и ср.р. на -о/-е
    if gender == 'MASCULINE' and not word_lower.endswith(('а', 'я', 'ь')):
        return '2nd'
    elif gender == 'NEUTER' and word_lower.endswith(('о', 'е')):
        return '2nd'
    
    # По умолчанию для неопределенных случаев
    return '2nd'

def verify_and_fix_corpus(input_file, output_file):
    """
    Проверяет и исправляет корпус
    """
    print(f"Загружаем корпус из {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    
    words = corpus['metadata']['words']
    total_words = len(words)
    
    print(f"Всего слов в корпусе: {total_words}")
    
    corrections = {
        '1st': 0,
        '2nd': 0,
        '3rd': 0,
        'heteroclitic': 0,
        'indeclinable': 0,
        'total': 0
    }
    
    print("Начинаем проверку и исправления...")
    
    for word, features in words.items():
        if features.get('pos') != 'NOUN':
            continue
            
        original_declension = features.get('declension')
        gender = features.get('gender')
        
        # Определяем правильное склонение
        correct_declension = determine_correct_declension(word, gender, features.get('pos'))
        
        if correct_declension and correct_declension != original_declension:
            features['declension'] = correct_declension
            corrections[correct_declension] += 1
            corrections['total'] += 1
            print(f"  {word}: {original_declension} -> {correct_declension}")
    
    print(f"\nИсправления завершены!")
    print(f"Статистика исправлений:")
    for decl, count in corrections.items():
        if decl != 'total':
            print(f"  {decl}: {count} слов")
    print(f"  ВСЕГО исправлений: {corrections['total']}")
    
    # Сохраняем исправленный корпус
    print(f"\nСохраняем исправленный корпус в {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"Готово! Исправленный корпус сохранен в {output_file}")
    
    return corrections

def check_specific_words(corpus_file, words_to_check):
    """
    Проверяет конкретные слова
    """
    print(f"\nПроверяем конкретные слова в {corpus_file}...")
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    
    words = corpus['metadata']['words']
    
    for word in words_to_check:
        if word in words:
            features = words[word]
            correct_declension = determine_correct_declension(
                word, 
                features.get('gender'), 
                features.get('pos')
            )
            print(f"{word}: {features.get('gender')} {features.get('declension')} -> должно быть {correct_declension}")
        else:
            print(f"{word}: не найдено в корпусе")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Использование: python verify_corpus.py <input_file> <output_file>")
        print("Пример: python verify_corpus.py opencorpora.json opencorpora_verified.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        corrections = verify_and_fix_corpus(input_file, output_file)
        
        # Проверяем конкретные проблемные слова
        problem_words = ['кортни', 'джозеф', 'ник', 'пабло', 'ариэль', 'ольга', 'елена']
        check_specific_words(output_file, problem_words)
        
        print(f"\n✅ Успешно исправлено {corrections['total']} слов!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)
