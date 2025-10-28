#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

def remove_inappropriate_words(input_json_path, output_json_path):
    """
    Удаляет неподходящие для детей слова из корпуса
    """
    print(f"Загружаем корпус из {input_json_path}...")
    with open(input_json_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    words_data = corpus['metadata']['words']
    total_words_before = len(words_data)
    print(f"Всего слов в корпусе: {total_words_before}")

    # Список неподходящих слов для детей
    inappropriate_words = [
        # Порнография и секс
        'порнограф', 'порнография', 'секс', 'сексуальный', 'проститутка', 'проституция',
        
        # Наркотики
        'наркотик', 'наркотики', 'кокаин', 'героин', 'марихуана', 'гашиш', 'наркота',
        
        # Алкоголь
        'алкоголь', 'водка', 'пиво', 'вино', 'пьяный', 'пьянство',
        
        # Насилие и смерть
        'убийство', 'убийца', 'самоубийство', 'самоубийца', 'смерть', 'труп',
        'насилие', 'изнасилование', 'изнасиловать', 'насиловать',
        
        # Терроризм и оружие
        'терроризм', 'террорист', 'бомба', 'взрыв', 'убивать',
        
        # Преступления
        'вор', 'кража', 'украсть', 'грабеж', 'грабитель',
        'преступление', 'преступник', 'тюрьма', 'арест', 'арестовать',
        
        # Курение
        'курение', 'сигарета', 'табак', 'курить',
        
        # Азартные игры
        'азарт', 'казино', 'ставка', 'ставки',
        
        # Коррупция
        'коррупция', 'взятка', 'взятки', 'коррумпированный',
        
        # Психические расстройства
        'суицид', 'суицидальный', 'депрессия', 'психиатрия'
    ]

    # Удаляем неподходящие слова
    removed_words = []
    for word in inappropriate_words:
        if word in words_data:
            del words_data[word]
            removed_words.append(word)
            print(f"  Удалено: {word}")

    # Дополнительная проверка на подозрительные слова
    suspicious_patterns = ['порн', 'секс', 'нарк', 'алког', 'убий', 'насил', 'терр', 'взрыв', 'бомб', 'суицид']
    
    words_to_remove = []
    for word in list(words_data.keys()):
        for pattern in suspicious_patterns:
            if pattern in word.lower():
                words_to_remove.append(word)
                break
    
    for word in words_to_remove:
        if word not in removed_words:  # не удаляем повторно
            del words_data[word]
            removed_words.append(word)
            print(f"  Удалено (подозрительное): {word}")

    total_words_after = len(words_data)
    removed_count = total_words_before - total_words_after

    print(f"\nУдаление завершено!")
    print(f"Удалено слов: {removed_count}")
    print(f"Осталось слов: {total_words_after}")

    # Сохраняем очищенный корпус
    output_data = {
        "metadata": {
            "source": "OpenCorpora (Очищенный от неподходящих слов)",
            "version": corpus['metadata']['version'],
            "revision": "child_safe",
            "total_words": total_words_after,
            "words": words_data
        }
    }

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Очищенный корпус сохранен в {output_json_path}")

    # Проверяем результат
    print(f"\nПроверяем результат в {output_json_path}...")
    with open(output_json_path, 'r', encoding='utf-8') as f:
        clean_corpus = json.load(f)
    
    # Проверяем, что неподходящие слова удалены
    still_present = []
    for word in inappropriate_words:
        if word in clean_corpus['metadata']['words']:
            still_present.append(word)
    
    if still_present:
        print(f"❌ Остались неподходящие слова: {still_present}")
    else:
        print("✅ Все неподходящие слова успешно удалены!")
    
    print(f"\n✅ Корпус очищен! Удалено {removed_count} неподходящих слов.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python remove_inappropriate_words.py <input_json_file> <output_json_file>")
        sys.exit(1)
    
    input_json = sys.argv[1]
    output_json = sys.argv[2]
    remove_inappropriate_words(input_json, output_json)
