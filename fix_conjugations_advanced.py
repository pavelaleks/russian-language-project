#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def fix_conjugations_advanced(input_json_path, output_json_path):
    """
    Исправляет спряжения глаголов, определяя их по формам
    """
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words = len(words_data)
    print(f"Всего слов в корпусе: {total_words}")

    fixed_count = 0
    
    # Правила определения спряжения по формам глаголов
    # 1-е спряжение: окончания -у/-ю, -ешь/-ёшь, -ет/-ёт, -ем/-ём, -ете/-ёте, -ут/-ют
    # 2-е спряжение: окончания -у/-ю, -ишь, -ит, -им, -ите, -ат/-ят
    
    print("Начинаем исправления спряжений по формам...")
    
    for word, features in words_data.items():
        if features.get('pos') != 'VERB':
            continue
            
        original_conjugation = features.get('conjugation')
        mood = features.get('mood')
        
        # Определяем спряжение по окончаниям форм
        conjugation = None
        
        # Инфинитивы
        if mood == 'INFINITIVE':
            if word.endswith('ить'):
                conjugation = '2nd'
            elif word.endswith(('ать', 'ять', 'еть', 'уть', 'оть')):
                # Исключения для 2-го спряжения
                second_conj_exceptions = {
                    'дышать', 'слышать', 'держать', 'гнать', 'терпеть', 'обидеть', 
                    'зависеть', 'ненавидеть', 'видеть', 'вертеть', 'обидеться', 'строить'
                }
                if word in second_conj_exceptions:
                    conjugation = '2nd'
                else:
                    conjugation = '1st'
            elif word.endswith('чь'):
                conjugation = '1st'
        
        # Формы настоящего времени (изъявительное наклонение)
        elif mood == 'INDICATIVE':
            # 2-е спряжение: окончания -ит, -ат/-ят, -ишь, -ите, -им
            if (word.endswith(('ит', 'ат', 'ят', 'ишь', 'ите', 'им')) or 
                word.endswith(('ится', 'атся', 'ятся', 'ишься', 'итесь', 'имся'))):
                conjugation = '2nd'
            # 1-е спряжение: окончания -ет/-ёт, -ут/-ют, -ешь/-ёшь, -ете/-ёте, -ем/-ём
            elif (word.endswith(('ет', 'ёт', 'ут', 'ют', 'ешь', 'ёшь', 'ете', 'ёте', 'ем', 'ём')) or
                  word.endswith(('ется', 'ётся', 'утся', 'ются', 'ешься', 'ёшься', 'етесь', 'ётесь', 'емся', 'ёмся'))):
                conjugation = '1st'
        
        # Повелительное наклонение
        elif mood == 'IMPERATIVE':
            # 2-е спряжение: окончания -и, -ите
            if word.endswith(('и', 'ите')):
                conjugation = '2nd'
            # 1-е спряжение: окончания -й, -йте
            elif word.endswith(('й', 'йте')):
                conjugation = '1st'
        
        # Применяем исправление
        if conjugation and original_conjugation != conjugation:
            features['conjugation'] = conjugation
            print(f"  {word}: {original_conjugation} -> {conjugation} ({mood})")
            fixed_count += 1
        elif conjugation is None and original_conjugation is None:
            # Для глаголов, которые не удалось классифицировать, попробуем по общим правилам
            if word.endswith(('ать', 'ять', 'еть', 'уть', 'оть')):
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
            "source": "OpenCorpora (Исправленный - склонения и спряжения)",
            "version": corpus['metadata']['version'],
            "revision": "corrected_conjugations_advanced",
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
        print("Использование: python fix_conjugations_advanced.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    fix_conjugations_advanced(input_json, output_json)
