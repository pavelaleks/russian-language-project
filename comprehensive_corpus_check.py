#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def comprehensive_corpus_check(input_json_path, output_json_path):
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words = len(words_data)
    print(f"Всего слов в корпусе: {total_words}")

    # Правила для существительных
    def determine_correct_declension(word, pos, gender):
        if pos != 'NOUN':
            return None
            
        # 1-е склонение: мужской и женский род на -а/-я
        if word.endswith(('а', 'я')):
            if gender in ['MASCULINE', 'FEMININE']:
                return '1st'
        
        # 2-е склонение: мужской род с нулевым окончанием, средний род на -о/-е
        elif word.endswith(('о', 'е')):
            if gender == 'NEUTER':
                return '2nd'
        elif not word.endswith(('а', 'я', 'ь')):
            if gender == 'MASCULINE':
                return '2nd'
        
        # 3-е склонение: женский род на -ь
        elif word.endswith('ь'):
            if gender == 'FEMININE':
                return '3rd'
        
        # Разносклоняемые (особые случаи)
        heteroclitic_words = {
            'путь', 'время', 'имя', 'племя', 'знамя', 'пламя', 'бремя', 'стремя', 'темя', 'семя'
        }
        if word in heteroclitic_words:
            return 'heteroclitic'
        
        # Несклоняемые (заимствованные, аббревиатуры, особые случаи)
        indeclinable_words = {
            'кино', 'кафе', 'метро', 'такси', 'меню', 'пальто', 'кофе', 'какао', 'кашне', 
            'пенсне', 'монпансье', 'конферансье', 'атташе', 'портмоне', 'резюме', 'алоэ',
            'какаду', 'кенгуру', 'шимпанзе', 'биеннале', 'радио', 'видео', 'аудио', 'фото',
            'авто', 'депо', 'трио', 'фэнтези', 'регби', 'танго', 'маэстро', 'цунами',
            'слово', 'дело', 'кольцо', 'пятно', 'тело', 'чудо', 'второе', 'яблочко',
            'манчестер', 'бобби', 'томми', 'джонни', 'джозеф', 'прозвище', 'шереметьево',
            'ооо', 'зимбабве', 'гиорги', 'мэтью', 'люси', 'нло', 'регги', 'внуково',
            'лукашенко', 'авченко', 'барри', 'бадри', 'коби', 'уго', 'кадафи', 'канделаки',
            'пабло', 'самоа', 'тэо', 'андре', 'пегги', 'терещенко', 'палермо', 'гаучо',
            'сильвио', 'иржи', 'тимоти', 'грегори', 'хельсинки', 'саакашвили', 'минниханов',
            'алехандро', 'бурджанадзе', 'зощенко', 'довженко', 'папандреу', 'эльдорадо'
        }
        
        # Проверяем по подстрокам для заимствованных слов
        indeclinable_patterns = ['ооо', 'ао', 'нло', 'вконтакте']
        for pattern in indeclinable_patterns:
            if pattern in word.lower():
                return 'indeclinable'
        
        if word in indeclinable_words:
            return 'indeclinable'
        
        # Имена собственные (часто несклоняемые)
        if word.istitle() and len(word) > 2:
            # Проверяем, не является ли это именем собственным
            foreign_names = {
                'джозеф', 'кортни', 'хиллари', 'джо', 'гарри', 'барри', 'пегги', 'сьюзи',
                'томми', 'джонни', 'бобби', 'люси', 'маэстро', 'пабло', 'андре', 'педро',
                'фернандо', 'алонсо', 'сильвио', 'иржи', 'гиви', 'бадри', 'коби', 'уго',
                'тимоти', 'грегори', 'алехандро', 'миньиханов', 'саакашвили', 'гиорги',
                'мэтью', 'бурджанадзе', 'терещенко', 'зощенко', 'довженко', 'лукашенко',
                'авченко', 'папандреу', 'кадафи', 'канделаки', 'тэо', 'альдо', 'самоа',
                'онтарио', 'малави', 'монако', 'чили', 'марокко', 'марти', 'зимбабве',
                'хельсинки', 'шереметьево', 'внуково', 'эльдорадо', 'палермо', 'гаучо'
            }
            if word.lower() in foreign_names:
                return 'indeclinable'
        
        return None

    # Правила для глаголов
    def determine_correct_conjugation(word, pos):
        if pos != 'VERB':
            return None
            
        # Алгоритм определения спряжения глаголов
        # 1. Проверяем окончание инфинитива
        
        # 1-е спряжение: -ать, -ять, -ыть, -уть, -оть, -ти, -чь
        if word.endswith(('ать', 'ять', 'ыть', 'уть', 'оть', 'ти', 'чь')):
            return '1st'
        
        # 2-е спряжение: -ить
        elif word.endswith('ить'):
            return '2nd'
        
        # Исключения для 1-го спряжения
        first_conjugation_exceptions = {
            'брить', 'стелить', 'зиждиться', 'выпить', 'уничтожить', 'жить'
        }
        if word in first_conjugation_exceptions:
            return '1st'
        
        # Исключения для 2-го спряжения
        second_conjugation_exceptions = {
            'слышать', 'дышать', 'держать', 'гнать', 'терпеть', 'вертеть', 
            'обидеть', 'зависеть', 'ненавидеть', 'видеть', 'смотреть', 'лежать'
        }
        if word in second_conjugation_exceptions:
            return '2nd'
        
        return None

    # Статистика исправлений
    declension_fixes = 0
    conjugation_fixes = 0
    total_checked = 0
    errors_found = []

    # Список действительно несклоняемых слов для проверки
    truly_indeclinable = {
        'кино', 'кафе', 'метро', 'такси', 'меню', 'пальто', 'кофе', 'какао', 'кашне', 
        'пенсне', 'монпансье', 'конферансье', 'атташе', 'портмоне', 'резюме', 'алоэ',
        'какаду', 'кенгуру', 'шимпанзе', 'биеннале', 'радио', 'видео', 'аудио', 'фото',
        'авто', 'депо', 'трио', 'фэнтези', 'регби', 'танго', 'маэстро', 'цунами',
        'слово', 'дело', 'кольцо', 'пятно', 'тело', 'чудо', 'второе', 'яблочко',
        'манчестер', 'бобби', 'томми', 'джонни', 'джозеф', 'прозвище', 'шереметьево',
        'ооо', 'зимбабве', 'гиорги', 'мэтью', 'люси', 'нло', 'регги', 'внуково',
        'лукашенко', 'авченко', 'барри', 'бадри', 'коби', 'уго', 'кадафи', 'канделаки',
        'пабло', 'самоа', 'тэо', 'андре', 'пегги', 'терещенко', 'палермо', 'гаучо',
        'сильвио', 'иржи', 'тимоти', 'грегори', 'хельсинки', 'саакашвили', 'минниханов',
        'алехандро', 'бурджанадзе', 'зощенко', 'довженко', 'папандреу', 'эльдорадо'
    }

    print("\n🔍 Проверяем каждое слово...")
    
    for word, features in words_data.items():
        total_checked += 1
        if total_checked % 500 == 0:
            print(f"Проверено {total_checked}/{total_words} слов...")
        
        pos = features.get('pos')
        gender = features.get('gender')
        current_declension = features.get('declension')
        current_conjugation = features.get('conjugation')
        
        # Проверяем склонение для существительных
        if pos == 'NOUN':
            correct_declension = determine_correct_declension(word, pos, gender)
            if correct_declension and correct_declension != current_declension:
                # Дополнительная проверка: не исправляем слова, которые уже правильно помечены как несклоняемые
                if current_declension == 'indeclinable' and word in truly_indeclinable:
                    continue  # Пропускаем правильно помеченные несклоняемые слова
                features['declension'] = correct_declension
                declension_fixes += 1
                errors_found.append(f"Склонение: {word} ({current_declension} → {correct_declension})")
        
        # Проверяем спряжение для глаголов
        elif pos == 'VERB':
            correct_conjugation = determine_correct_conjugation(word, pos)
            if correct_conjugation and correct_conjugation != current_conjugation:
                features['conjugation'] = correct_conjugation
                conjugation_fixes += 1
                errors_found.append(f"Спряжение: {word} ({current_conjugation} → {correct_conjugation})")

    print(f"\n✅ Проверка завершена!")
    print(f"Всего проверено слов: {total_checked}")
    print(f"Исправлено склонений: {declension_fixes}")
    print(f"Исправлено спряжений: {conjugation_fixes}")
    print(f"Всего исправлений: {declension_fixes + conjugation_fixes}")

    if errors_found:
        print(f"\n📋 Найденные ошибки:")
        for error in errors_found[:20]:  # Показываем первые 20 ошибок
            print(f"  {error}")
        if len(errors_found) > 20:
            print(f"  ... и еще {len(errors_found) - 20} ошибок")

    # Сохраняем исправленный корпус
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Исправленный корпус сохранен в {output_json_path}")
    
    return declension_fixes + conjugation_fixes

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python comprehensive_corpus_check.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    total_fixes = comprehensive_corpus_check(input_json, output_json)
    
    if total_fixes > 0:
        print(f"\n🎯 Найдено и исправлено {total_fixes} ошибок в корпусе!")
    else:
        print(f"\n✨ Корпус проверен - ошибок не найдено!")
