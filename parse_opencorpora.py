#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import json
import sys
import re
from collections import defaultdict

def extract_morphological_features(lemma_element):
    """Извлекает морфологические признаки из элемента леммы"""
    features = {
        'lemma': lemma_element.get('t', ''),
        'pos': None,
        'gender': None,
        'number': None,
        'case': None,
        'declension': None,
        'conjugation': None,
        'aspect': None,
        'transitivity': None,
        'mood': None,
        'tense': None,
        'person': None,
        'animacy': None,
        'degree': None
    }
    
    # Получаем грамматические признаки
    grammemes = []
    for g in lemma_element.findall('g'):
        grammemes.append(g.get('v', ''))
    
    # Обрабатываем грамматические признаки
    for grammeme in grammemes:
        if grammeme == 'NOUN':
            features['pos'] = 'NOUN'
        elif grammeme == 'VERB':
            features['pos'] = 'VERB'
        elif grammeme == 'INFN':
            features['pos'] = 'VERB'
            features['mood'] = 'INFINITIVE'
        elif grammeme == 'ADJF':
            features['pos'] = 'ADJECTIVE'
        elif grammeme == 'ADJS':
            features['pos'] = 'ADJECTIVE'
            features['degree'] = 'SHORT'
        elif grammeme == 'COMP':
            features['pos'] = 'ADJECTIVE'
            features['degree'] = 'COMPARATIVE'
        elif grammeme == 'ADVB':
            features['pos'] = 'ADVERB'
        elif grammeme == 'CONJ':
            features['pos'] = 'CONJUNCTION'
        elif grammeme == 'PRCL':
            features['pos'] = 'PARTICLE'
        elif grammeme == 'PREP':
            features['pos'] = 'PREPOSITION'
        elif grammeme == 'NPRO':
            features['pos'] = 'PRONOUN'
        elif grammeme == 'NUMR':
            features['pos'] = 'NUMERAL'
        elif grammeme == 'INTJ':
            features['pos'] = 'INTERJECTION'
        elif grammeme == 'masc':
            features['gender'] = 'MASCULINE'
        elif grammeme == 'femn':
            features['gender'] = 'FEMININE'
        elif grammeme == 'neut':
            features['gender'] = 'NEUTER'
        elif grammeme == 'sing':
            features['number'] = 'SINGULAR'
        elif grammeme == 'plur':
            features['number'] = 'PLURAL'
        elif grammeme == 'nomn':
            features['case'] = 'NOMINATIVE'
        elif grammeme == 'gent':
            features['case'] = 'GENITIVE'
        elif grammeme == 'datv':
            features['case'] = 'DATIVE'
        elif grammeme == 'accs':
            features['case'] = 'ACCUSATIVE'
        elif grammeme == 'ablt':
            features['case'] = 'INSTRUMENTAL'
        elif grammeme in ['loct', 'loc1', 'loc2']:
            features['case'] = 'PREPOSITIONAL'
        elif grammeme == 'anim':
            features['animacy'] = 'ANIMATE'
        elif grammeme == 'inan':
            features['animacy'] = 'INANIMATE'
        elif grammeme == 'perf':
            features['aspect'] = 'PERFECTIVE'
        elif grammeme == 'impf':
            features['aspect'] = 'IMPERFECTIVE'
        elif grammeme == 'tran':
            features['transitivity'] = 'TRANSITIVE'
        elif grammeme == 'intr':
            features['transitivity'] = 'INTRANSITIVE'
        elif grammeme == 'indc':
            features['mood'] = 'INDICATIVE'
        elif grammeme == 'impr':
            features['mood'] = 'IMPERATIVE'
        elif grammeme == 'pres':
            features['tense'] = 'PRESENT'
        elif grammeme == 'past':
            features['tense'] = 'PAST'
        elif grammeme == 'futr':
            features['tense'] = 'FUTURE'
        elif grammeme == '1per':
            features['person'] = '1'
        elif grammeme == '2per':
            features['person'] = '2'
        elif grammeme == '3per':
            features['person'] = '3'
    
    # Определяем склонение для существительных
    if features['pos'] == 'NOUN' and features['case'] == 'NOMINATIVE' and features['number'] == 'SINGULAR':
        features['declension'] = determine_declension(features['lemma'], features['gender'])
    
    # Определяем спряжение для глаголов
    if features['pos'] == 'VERB' and features['mood'] == 'INFINITIVE':
        features['conjugation'] = determine_conjugation(features['lemma'])
    
    return features

def determine_declension(lemma, gender):
    """Определяет склонение существительного"""
    if gender == 'FEMININE' and lemma.endswith('ь'):
        return '3rd'
    elif lemma.endswith('а') or lemma.endswith('я'):
        return '1st'
    elif lemma.endswith('о') or lemma.endswith('е') or gender == 'NEUTER':
        return '2nd'
    elif lemma.endswith('мя'):
        return 'heteroclitic'
    elif lemma.endswith('о') and not lemma.endswith('мя'):
        # Проверяем несклоняемые
        indeclinable_endings = ['кофе', 'какао', 'радио', 'метро', 'кино', 'кабаре', 'бюро', 'депо', 'фойе', 'ателье', 'кафе', 'пенсне', 'колье']
        if lemma in indeclinable_endings:
            return 'indeclinable'
        return '2nd'
    else:
        return '1st'

def determine_conjugation(lemma):
    """Определяет спряжение глагола"""
    second_conjugation_endings = ['ить', 'ать', 'ять', 'еть', 'уть', 'оть']
    second_conjugation_exceptions = ['брить', 'стелить', 'зиждиться']
    
    if lemma in second_conjugation_exceptions:
        return '2nd'
    
    for ending in second_conjugation_endings:
        if lemma.endswith(ending):
            return '2nd'
    
    return '1st'

def parse_opencorpora_xml(xml_file_path):
    """Парсит XML файл OpenCorpora и извлекает морфологические данные"""
    print(f"Парсинг файла: {xml_file_path}")
    
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        morphology_data = {
            'metadata': {
                'source': 'OpenCorpora',
                'version': root.get('version', ''),
                'revision': root.get('revision', ''),
                'total_words': 0,
                'words': {}
            }
        }
        
        word_count = 0
        unique_words = set()
        
        # Обрабатываем тексты
        for text in root.findall('text'):
            paragraphs = text.find('paragraphs')
            if paragraphs is None:
                continue
                
            for paragraph in paragraphs.findall('paragraph'):
                for sentence in paragraph.findall('sentence'):
                    tokens = sentence.find('tokens')
                    if tokens is None:
                        continue
                    
                    for token in tokens.findall('token'):
                        tfr = token.find('tfr')
                        if tfr is None:
                            continue
                        
                        v = tfr.find('v')
                        if v is None:
                            continue
                        
                        l = v.find('l')
                        if l is None:
                            continue
                        
                        word = token.get('text', '').lower()
                        
                        # Пропускаем знаки препинания и служебные слова
                        grammemes = [g.get('v', '') for g in l.findall('g')]
                        if any(g in ['PNCT', 'PREP', 'PRCL'] for g in grammemes):
                            continue
                        
                        # Извлекаем морфологические признаки
                        features = extract_morphological_features(l)
                        
                        if features and word not in unique_words and features['pos']:
                            unique_words.add(word)
                            morphology_data['metadata']['words'][word] = features
                            word_count += 1
                            
                            if word_count % 1000 == 0:
                                print(f"Обработано {word_count} слов...")
        
        morphology_data['metadata']['total_words'] = word_count
        
        print(f"Извлечено {word_count} уникальных слов")
        return morphology_data
        
    except Exception as e:
        print(f"Ошибка парсинга XML: {e}")
        return None

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'annot.opcorpora.no_ambig.xml'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'opencorpora_morphology.json'
    
    print(f"Парсинг {input_file}...")
    
    morphology_data = parse_opencorpora_xml(input_file)
    
    if morphology_data:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(morphology_data, f, ensure_ascii=False, indent=2)
        print(f"Результат сохранен в {output_file}")
        print(f"Всего слов: {morphology_data['metadata']['total_words']}")
    else:
        print("Ошибка парсинга")

if __name__ == "__main__":
    main()
