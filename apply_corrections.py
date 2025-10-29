#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для автоматического исправления базы данных на основе ошибок из админ-панели
"""

import json
import os
from datetime import datetime

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

def load_errors_from_file(filename):
    """Загружает ошибки из экспортированного файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки файла ошибок {filename}: {e}")
        return None

def apply_corrections_to_corpus(corpus, corrections):
    """Применяет исправления к корпусу"""
    corrections_applied = 0
    
    for correction in corrections:
        word = correction['word']
        corrected_declension = correction.get('correctedDeclension')
        corrected_conjugation = correction.get('correctedConjugation')
        
        if word in corpus['metadata']['words']:
            features = corpus['metadata']['words'][word]
            
            # Применяем исправления склонения
            if corrected_declension and features.get('pos') == 'NOUN':
                old_declension = features.get('declension', 'unknown')
                features['declension'] = corrected_declension
                print(f"🔧 Исправлено склонение '{word}': {old_declension} → {corrected_declension}")
                corrections_applied += 1
            
            # Применяем исправления спряжения
            if corrected_conjugation and features.get('pos') == 'VERB':
                old_conjugation = features.get('conjugation', 'unknown')
                features['conjugation'] = corrected_conjugation
                print(f"🔧 Исправлено спряжение '{word}': {old_conjugation} → {corrected_conjugation}")
                corrections_applied += 1
            
            # Добавляем метаданные об исправлении
            features['last_corrected'] = correction.get('correctedAt', datetime.now().isoformat())
            features['correction_source'] = 'admin_panel'
    
    return corrections_applied

def process_errors_file():
    """Обрабатывает файл с ошибками и применяет исправления"""
    print("🔧 Обработка ошибок из админ-панели...")
    
    # Ищем файлы с ошибками
    error_files = [f for f in os.listdir('.') if f.startswith('lexicon_errors_') and f.endswith('.json')]
    
    if not error_files:
        print("❌ Файлы с ошибками не найдены")
        print("💡 Экспортируйте ошибки из админ-панели (кнопка 'Экспорт')")
        return False
    
    # Берем самый новый файл
    latest_file = max(error_files, key=os.path.getctime)
    print(f"📁 Обрабатываем файл: {latest_file}")
    
    # Загружаем ошибки
    errors_data = load_errors_from_file(latest_file)
    if not errors_data:
        return False
    
    # Фильтруем только исправленные ошибки
    corrected_errors = [
        error for error in errors_data['errors'] 
        if error.get('status') == 'corrected'
    ]
    
    if not corrected_errors:
        print("ℹ️ Нет исправленных ошибок для применения")
        return True
    
    print(f"📊 Найдено {len(corrected_errors)} исправленных ошибок")
    
    # Загружаем корпус
    corpus = load_corpus('opencorpora.json')
    if not corpus:
        return False
    
    # Применяем исправления
    corrections_applied = apply_corrections_to_corpus(corpus, corrected_errors)
    
    if corrections_applied > 0:
        # Обновляем метаданные корпуса
        corpus['metadata']['last_correction'] = datetime.now().isoformat()
        corpus['metadata']['corrections_applied'] = corrections_applied
        corpus['metadata']['revision'] = f"corrected_{corpus['metadata']['total_words']}_{corrections_applied}"
        
        # Сохраняем исправленный корпус
        if save_corpus(corpus, 'opencorpora.json'):
            # Также обновляем офлайн версию
            save_corpus(corpus, 'russian_language_offline/opencorpora.json')
            print(f"🎉 Успешно применено {corrections_applied} исправлений!")
            return True
    
    return False

def create_backup():
    """Создает резервную копию корпуса"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"opencorpora_backup_{timestamp}.json"
    
    corpus = load_corpus('opencorpora.json')
    if corpus and save_corpus(corpus, backup_filename):
        print(f"💾 Создана резервная копия: {backup_filename}")
        return True
    return False

if __name__ == "__main__":
    print("🔧 Система исправления базы данных Лексикон")
    print("=" * 50)
    
    # Создаем резервную копию
    if not create_backup():
        print("❌ Не удалось создать резервную копию")
        exit(1)
    
    # Обрабатываем ошибки
    success = process_errors_file()
    
    if success:
        print("\n✅ Исправления успешно применены!")
        print("🔄 Обновите страницу в браузере для применения изменений")
    else:
        print("\n❌ Ошибка при применении исправлений")
