#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def optimize_corpus(input_file, output_file):
    """Создает оптимизированную версию корпуса для веб-хостинга"""
    
    print(f"Загрузка корпуса из {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        full_corpus = json.load(f)
    
    # Создаем оптимизированную версию
    optimized_corpus = {
        'metadata': {
            'source': 'OpenCorpora (Optimized)',
            'version': full_corpus['metadata']['version'],
            'revision': full_corpus['metadata']['revision'],
            'total_words': 0,
            'words': {}
        }
    }
    
    # Отбираем наиболее частотные и полезные слова
    word_priority = {
        'NOUN': 0.4,      # 40% существительных
        'VERB': 0.25,     # 25% глаголов
        'ADJECTIVE': 0.2, # 20% прилагательных
        'ADVERB': 0.1,    # 10% наречий
        'CONJUNCTION': 0.05 # 5% союзов
    }
    
    word_counts = {pos: 0 for pos in word_priority}
    max_words_per_pos = {
        'NOUN': 2000,
        'VERB': 1000,
        'ADJECTIVE': 800,
        'ADVERB': 400,
        'CONJUNCTION': 200
    }
    
    # Сортируем слова по приоритету
    for word, features in full_corpus['metadata']['words'].items():
        pos = features.get('pos')
        if pos in word_priority and word_counts[pos] < max_words_per_pos[pos]:
            # Приоритет: базовые формы, короткие слова, частотные
            priority_score = 0
            
            # Базовые формы получают приоритет
            if (pos == 'NOUN' and features.get('case') == 'NOMINATIVE' and features.get('number') == 'SINGULAR'):
                priority_score += 100
            elif (pos == 'VERB' and features.get('mood') == 'INFINITIVE'):
                priority_score += 100
            elif (pos == 'ADJECTIVE' and features.get('case') == 'NOMINATIVE' and features.get('number') == 'SINGULAR'):
                priority_score += 100
            elif pos in ['ADVERB', 'CONJUNCTION']:
                priority_score += 100
                
            # Короткие слова получают приоритет
            priority_score += max(0, 10 - len(word))
            
            # Добавляем слово с приоритетом
            optimized_corpus['metadata']['words'][word] = features
            word_counts[pos] += 1
            optimized_corpus['metadata']['total_words'] += 1
    
    print(f'Создан оптимизированный корпус: {optimized_corpus["metadata"]["total_words"]} слов')
    print('Распределение по частям речи:')
    for pos, count in word_counts.items():
        print(f'  {pos}: {count} слов')
    
    # Сохраняем оптимизированный корпус
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(optimized_corpus, f, ensure_ascii=False, indent=2)
    
    print(f'Оптимизированный корпус сохранен в {output_file}')
    
    # Показываем размер файлов
    import os
    original_size = os.path.getsize(input_file) / (1024 * 1024)
    optimized_size = os.path.getsize(output_file) / (1024 * 1024)
    compression_ratio = (1 - optimized_size / original_size) * 100
    
    print(f'Размер исходного файла: {original_size:.1f} MB')
    print(f'Размер оптимизированного файла: {optimized_size:.1f} MB')
    print(f'Сжатие: {compression_ratio:.1f}%')

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'opencorpora_no_ambig.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'opencorpora_optimized.json'
    
    try:
        optimize_corpus(input_file, output_file)
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
