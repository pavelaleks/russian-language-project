#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для расширения корпуса слов и тщательной проверки склонений и спряжений
"""

import json
import random
import re
from collections import defaultdict

def load_corpus(filename):
    """Загружает корпус из JSON файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки {filename}: {e}")
        return None

def save_corpus(corpus, filename):
    """Сохраняет корпус в JSON файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(corpus, f, ensure_ascii=False, indent=2)
        print(f"✅ Корпус сохранен в {filename}")
        return True
    except Exception as e:
        print(f"❌ Ошибка сохранения {filename}: {e}")
        return False

def determine_declension_correct(word, features):
    """Определяет правильное склонение для существительного"""
    word_lower = word.lower()
    
    # Разносклоняемые существительные (на -мя)
    heteroclitic_words = [
        'время', 'имя', 'племя', 'знамя', 'пламя', 'стремя', 'темя', 
        'семя', 'бремя', 'вымя', 'племя', 'время', 'имя', 'знамя'
    ]
    if word_lower in heteroclitic_words:
        return 'heteroclitic'
    
    # Несклоняемые существительные
    indeclinable_words = [
        'кофе', 'пальто', 'кино', 'такси', 'метро', 'кафе', 'меню', 
        'алоэ', 'какао', 'радио', 'шоу', 'казино', 'кабаре', 'бюро', 
        'депо', 'фойе', 'ателье', 'пенсне', 'колье', 'какаду', 'кенгуру',
        'шимпанзе', 'какао', 'радио', 'метро', 'кино', 'такси'
    ]
    if word_lower in indeclinable_words:
        return 'indeclinable'
    
    # Определение по окончаниям
    if word_lower.endswith('а') or word_lower.endswith('я'):
        return '1st'
    elif word_lower.endswith('о') or word_lower.endswith('е'):
        return '2nd'
    elif word_lower.endswith('ь'):
        return '3rd'
    else:
        # Мужской род без окончания - обычно 2-е склонение
        if features.get('gender') == 'MASCULINE':
            return '2nd'
        # По умолчанию 1-е склонение
        return '1st'

def determine_conjugation_correct(word, features):
    """Определяет правильное спряжение для глагола"""
    word_lower = word.lower()
    
    # Исключения для 1-го спряжения
    first_conjugation_exceptions = ['брить', 'стелить', 'зиждиться']
    if word_lower in first_conjugation_exceptions:
        return '1st'
    
    # 2-е спряжение по окончаниям
    second_conjugation_endings = ['ить', 'ать', 'ять', 'еть', 'уть', 'оть']
    for ending in second_conjugation_endings:
        if word_lower.endswith(ending):
            return '2nd'
    
    # По умолчанию 1-е спряжение
    return '1st'

def fix_word_features(word, features):
    """Исправляет морфологические признаки слова"""
    fixed_features = features.copy()
    
    if features.get('pos') == 'NOUN':
        # Исправляем склонение
        correct_declension = determine_declension_correct(word, features)
        fixed_features['declension'] = correct_declension
        
        # Исправляем род для несклоняемых слов
        if correct_declension == 'indeclinable':
            if word.lower() in ['кофе', 'какао', 'радио', 'метро', 'кино', 'такси']:
                fixed_features['gender'] = 'MASCULINE'
            elif word.lower() in ['пальто', 'кафе', 'меню', 'алоэ', 'колье']:
                fixed_features['gender'] = 'NEUTER'
    
    elif features.get('pos') == 'VERB':
        # Исправляем спряжение
        correct_conjugation = determine_conjugation_correct(word, features)
        fixed_features['conjugation'] = correct_conjugation
    
    return fixed_features

def expand_corpus_with_verification():
    """Расширяет корпус и проводит тщательную проверку"""
    print("🔄 Начинаем расширение корпуса...")
    
    # Загружаем текущий корпус
    current_corpus = load_corpus('opencorpora.json')
    if not current_corpus:
        print("❌ Не удалось загрузить текущий корпус")
        return False
    
    # Загружаем большой корпус для расширения
    large_corpus = load_corpus('opencorpora_fixed.json')
    if not large_corpus:
        print("❌ Не удалось загрузить большой корпус")
        return False
    
    print(f"📊 Текущий корпус: {current_corpus['metadata']['total_words']} слов")
    print(f"📊 Большой корпус: {large_corpus['metadata']['total_words']} слов")
    
    # Получаем существующие слова
    existing_words = set(current_corpus['metadata']['words'].keys())
    
    # Фильтруем новые слова из большого корпуса
    new_words = {}
    words_by_type = defaultdict(list)
    
    for word, features in large_corpus['metadata']['words'].items():
        if word not in existing_words:
            # Проверяем, что это подходящее слово для упражнений
            if (features.get('pos') in ['NOUN', 'VERB', 'ADJECTIVE', 'ADVERB', 'CONJUNCTION'] and
                features.get('case') == 'NOMINATIVE' and 
                features.get('number') == 'SINGULAR'):
                
                # Исправляем морфологические признаки
                fixed_features = fix_word_features(word, features)
                new_words[word] = fixed_features
                
                # Группируем по частям речи
                words_by_type[fixed_features.get('pos')].append(word)
    
    print(f"📝 Найдено {len(new_words)} новых подходящих слов")
    print(f"   - Существительные: {len(words_by_type['NOUN'])}")
    print(f"   - Глаголы: {len(words_by_type['VERB'])}")
    print(f"   - Прилагательные: {len(words_by_type['ADJECTIVE'])}")
    print(f"   - Наречия: {len(words_by_type['ADVERB'])}")
    print(f"   - Союзы: {len(words_by_type['CONJUNCTION'])}")
    
    # Выбираем 4000 лучших слов
    target_count = 4000
    selected_words = {}
    
    # Приоритет: существительные и глаголы для упражнений
    priority_order = ['NOUN', 'VERB', 'ADJECTIVE', 'ADVERB', 'CONJUNCTION']
    
    for pos in priority_order:
        if len(selected_words) >= target_count:
            break
        
        words_of_type = words_by_type[pos]
        random.shuffle(words_of_type)  # Случайный порядок
        
        for word in words_of_type:
            if len(selected_words) >= target_count:
                break
            selected_words[word] = new_words[word]
    
    print(f"✅ Выбрано {len(selected_words)} слов для добавления")
    
    # Добавляем новые слова в корпус
    current_corpus['metadata']['words'].update(selected_words)
    current_corpus['metadata']['total_words'] = len(current_corpus['metadata']['words'])
    current_corpus['metadata']['source'] = 'OpenCorpora + Extended'
    current_corpus['metadata']['revision'] = f"extended_{current_corpus['metadata']['total_words']}"
    
    # Проводим финальную проверку всех слов
    print("🔍 Проводим тщательную проверку всех слов...")
    
    verification_errors = []
    declension_stats = defaultdict(int)
    conjugation_stats = defaultdict(int)
    
    for word, features in current_corpus['metadata']['words'].items():
        # Проверяем склонения существительных
        if features.get('pos') == 'NOUN':
            correct_declension = determine_declension_correct(word, features)
            if features.get('declension') != correct_declension:
                verification_errors.append(f"Склонение '{word}': {features.get('declension')} → {correct_declension}")
                features['declension'] = correct_declension
            declension_stats[correct_declension] += 1
        
        # Проверяем спряжения глаголов
        elif features.get('pos') == 'VERB':
            correct_conjugation = determine_conjugation_correct(word, features)
            if features.get('conjugation') != correct_conjugation:
                verification_errors.append(f"Спряжение '{word}': {features.get('conjugation')} → {correct_conjugation}")
                features['conjugation'] = correct_conjugation
            conjugation_stats[correct_conjugation] += 1
    
    print(f"📊 Статистика склонений:")
    for decl, count in declension_stats.items():
        print(f"   - {decl}: {count} слов")
    
    print(f"📊 Статистика спряжений:")
    for conj, count in conjugation_stats.items():
        print(f"   - {conj}: {count} слов")
    
    if verification_errors:
        print(f"⚠️ Исправлено {len(verification_errors)} ошибок:")
        for error in verification_errors[:10]:  # Показываем первые 10
            print(f"   {error}")
        if len(verification_errors) > 10:
            print(f"   ... и еще {len(verification_errors) - 10} ошибок")
    else:
        print("✅ Все склонения и спряжения корректны!")
    
    # Сохраняем расширенный корпус
    if save_corpus(current_corpus, 'opencorpora_extended.json'):
        print(f"🎉 Корпус успешно расширен до {current_corpus['metadata']['total_words']} слов!")
        return True
    
    return False

if __name__ == "__main__":
    success = expand_corpus_with_verification()
    if success:
        print("\n✅ Расширение корпуса завершено успешно!")
    else:
        print("\n❌ Ошибка при расширении корпуса")
