#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления ошибок в корпусе и добавления корзинки ошибок
"""

import json
import re

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

def fix_indeclinable_words():
    """Исправляет несклоняемые слова в корпусе"""
    print("🔧 Исправляем несклоняемые слова...")
    
    corpus = load_corpus('opencorpora.json')
    if not corpus:
        return False
    
    # Расширенный список несклоняемых слов
    indeclinable_patterns = [
        # Иностранные слова на -е
        'биеннале', 'триеннале', 'квадриеннале', 'биеннале', 'триеннале',
        
        # Французские слова
        'пальто', 'кафе', 'меню', 'алоэ', 'колье', 'пенсне', 'кабаре', 
        'бюро', 'депо', 'фойе', 'ателье', 'казино', 'шоу',
        
        # Латинские слова
        'какао', 'радио', 'метро', 'кино', 'такси', 'кофе',
        
        # Животные
        'какаду', 'кенгуру', 'шимпанзе', 'фламинго', 'колибри',
        
        # Другие несклоняемые
        'эссе', 'резюме', 'интервью', 'портмоне', 'конферансье'
    ]
    
    fixes_made = 0
    
    for word in indeclinable_patterns:
        if word in corpus['metadata']['words']:
            features = corpus['metadata']['words'][word]
            if features.get('declension') != 'indeclinable':
                print(f"🔧 Исправляем {word}: {features.get('declension')} → indeclinable")
                features['declension'] = 'indeclinable'
                fixes_made += 1
    
    # Также проверяем по паттернам окончаний
    for word, features in corpus['metadata']['words'].items():
        word_lower = word.lower()
        
        # Слова на -е, которые часто несклоняемые
        if (word_lower.endswith('е') and 
            len(word_lower) > 4 and 
            features.get('pos') == 'NOUN' and
            features.get('declension') == '2nd'):
            
            # Проверяем, не является ли это несклоняемым
            if any(pattern in word_lower for pattern in ['биеннале', 'триеннале', 'эссе', 'резюме']):
                print(f"🔧 Исправляем по паттерну {word}: {features.get('declension')} → indeclinable")
                features['declension'] = 'indeclinable'
                fixes_made += 1
    
    print(f"✅ Исправлено {fixes_made} несклоняемых слов")
    
    # Сохраняем исправленный корпус
    if save_corpus(corpus, 'opencorpora.json'):
        print("✅ Корпус обновлен")
        return True
    
    return False

if __name__ == "__main__":
    success = fix_indeclinable_words()
    if success:
        print("\n✅ Исправление несклоняемых слов завершено!")
    else:
        print("\n❌ Ошибка при исправлении")
