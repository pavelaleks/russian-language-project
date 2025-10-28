#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания исправленного корпуса с правильной классификацией склонений
"""

import json

def create_corrected_corpus():
    """
    Создает корпус с правильной классификацией склонений
    """
    
    # Слова с правильной классификацией склонений
    words_data = {
        # 1-е склонение (муж.р. и жен.р. на -а/-я)
        'папа': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '1st', 'animacy': 'ANIMATE'},
        'дядя': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '1st', 'animacy': 'ANIMATE'},
        'мама': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'ANIMATE'},
        'тётя': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'ANIMATE'},
        'земля': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'вода': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'стена': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'рука': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'нога': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'голова': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'дорога': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'книга': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'ручка': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'база': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        'дуга': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        
        # 2-е склонение (муж.р. с нулевым окончанием и ср.р. на -о/-е)
        'стол': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'дом': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'конь': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'день': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'окно': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'поле': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'море': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'дерево': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'совладелец': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'автор': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'информатор': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'чайковский': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'акунин': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'ильф': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'морис': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'логотип': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'манчестер': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'вывод': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'святослав': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'архетип': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'феофан': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'жених': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'фронт': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'сенатор': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'экипаж': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'эксперт': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'градус': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'проект': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'народ': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'рост': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'кризис': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'доктор': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'советник': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'концерт': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'обозреватель': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'юбилей': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'индекс': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'александр': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'казаков': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'эрнест': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'миллион': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'редактор': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'путешествие': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'вероятность': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'кукла': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '1st', 'animacy': 'INANIMATE'},
        
        # 3-е склонение (жен.р. на мягкий знак)
        'ночь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'мышь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'ANIMATE'},
        'рожь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'печь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'дочь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'ANIMATE'},
        'ложь': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'соль': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'боль': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'моль': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'ANIMATE'},
        'тень': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'лень': {'pos': 'NOUN', 'gender': 'FEMININE', 'declension': '3rd', 'animacy': 'INANIMATE'},
        'пень': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'день': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'INANIMATE'},
        'конь': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        'конь': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': '2nd', 'animacy': 'ANIMATE'},
        
        # Разносклоняемые
        'путь': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'время': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'имя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'племя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'знамя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'пламя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'стремя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'темя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'семя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'бремя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        'вымя': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'heteroclitic', 'animacy': 'INANIMATE'},
        
        # Несклоняемые
        'самоа': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'кофе': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'пальто': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'кино': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'метро': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'такси': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'меню': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'кафе': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'ателье': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'пенсне': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'кашне': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'пари': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'реле': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'шоссе': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'алоэ': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'какао': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'пианино': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'радио': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'видео': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'аудио': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'фото': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'авто': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'мото': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'домино': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'казино': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'лото': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'бюро': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'депо': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'фойе': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'манто': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'INANIMATE'},
        'боа': {'pos': 'NOUN', 'gender': 'NEUTER', 'declension': 'indeclinable', 'animacy': 'ANIMATE'},
        'кенгуру': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'indeclinable', 'animacy': 'ANIMATE'},
        'шимпанзе': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'indeclinable', 'animacy': 'ANIMATE'},
        'какаду': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'indeclinable', 'animacy': 'ANIMATE'},
        'фламинго': {'pos': 'NOUN', 'gender': 'MASCULINE', 'declension': 'indeclinable', 'animacy': 'ANIMATE'},
        
        # Глаголы
        'читать': {'pos': 'VERB', 'conjugation': '1st', 'aspect': 'IMPERFECTIVE', 'transitivity': 'TRANSITIVE'},
        'писать': {'pos': 'VERB', 'conjugation': '1st', 'aspect': 'IMPERFECTIVE', 'transitivity': 'TRANSITIVE'},
        'говорить': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'INTRANSITIVE'},
        'смотреть': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'TRANSITIVE'},
        'любить': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'TRANSITIVE'},
        'строить': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'TRANSITIVE'},
        'учиться': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'INTRANSITIVE'},
        'работать': {'pos': 'VERB', 'conjugation': '1st', 'aspect': 'IMPERFECTIVE', 'transitivity': 'INTRANSITIVE'},
        'жить': {'pos': 'VERB', 'conjugation': '2nd', 'aspect': 'IMPERFECTIVE', 'transitivity': 'INTRANSITIVE'},
        'идти': {'pos': 'VERB', 'conjugation': '1st', 'aspect': 'IMPERFECTIVE', 'transitivity': 'INTRANSITIVE'},
        
        # Прилагательные
        'красивый': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'хороший': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'большой': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'маленький': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'новый': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'старый': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'красный': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'синий': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'зелёный': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        'чёрный': {'pos': 'ADJECTIVE', 'gender': 'MASCULINE'},
        
        # Наречия
        'быстро': {'pos': 'ADVERB'},
        'медленно': {'pos': 'ADVERB'},
        'хорошо': {'pos': 'ADVERB'},
        'плохо': {'pos': 'ADVERB'},
        'далеко': {'pos': 'ADVERB'},
        'близко': {'pos': 'ADVERB'},
        'высоко': {'pos': 'ADVERB'},
        'низко': {'pos': 'ADVERB'},
        'рано': {'pos': 'ADVERB'},
        'поздно': {'pos': 'ADVERB'},
        
        # Союзы
        'и': {'pos': 'CONJUNCTION'},
        'а': {'pos': 'CONJUNCTION'},
        'но': {'pos': 'CONJUNCTION'},
        'или': {'pos': 'CONJUNCTION'},
        'что': {'pos': 'CONJUNCTION'},
        'чтобы': {'pos': 'CONJUNCTION'},
        'если': {'pos': 'CONJUNCTION'},
        'когда': {'pos': 'CONJUNCTION'},
        'потому': {'pos': 'CONJUNCTION'},
        'поэтому': {'pos': 'CONJUNCTION'}
    }
    
    # Создаем корпус
    corpus = {
        "metadata": {
            "source": "Исправленный корпус",
            "version": "1.0",
            "revision": "corrected",
            "total_words": len(words_data),
            "words": words_data
        }
    }
    
    # Сохраняем корпус
    with open('opencorpora.json', 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Создан исправленный корпус: {len(words_data)} слов")
    
    # Статистика
    declensions = {}
    for word, features in words_data.items():
        if features.get('pos') == 'NOUN':
            decl = features.get('declension', 'unknown')
            declensions[decl] = declensions.get(decl, 0) + 1
    
    print("Распределение по склонениям:")
    for decl, count in sorted(declensions.items()):
        print(f"  {decl}: {count} слов")
    
    return corpus

if __name__ == "__main__":
    create_corrected_corpus()
