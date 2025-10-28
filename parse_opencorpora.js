#!/usr/bin/env node

const fs = require('fs');
const xml2js = require('xml2js');

// Функция для парсинга XML файла OpenCorpora
async function parseOpenCorporaXML(xmlFilePath) {
    try {
        console.log(`Парсинг файла: ${xmlFilePath}`);
        
        const xmlData = fs.readFileSync(xmlFilePath, 'utf8');
        const parser = new xml2js.Parser({
            explicitArray: false,
            mergeAttrs: true
        });
        
        const result = await parser.parseStringPromise(xmlData);
        
        const morphologyData = {
            metadata: {
                source: "OpenCorpora",
                version: result.annotation.$.version,
                revision: result.annotation.$.revision,
                total_words: 0,
                words: {}
            }
        };
        
        let wordCount = 0;
        const uniqueWords = new Set();
        
        // Обрабатываем тексты
        const texts = Array.isArray(result.annotation.text) ? result.annotation.text : [result.annotation.text];
        
        for (const text of texts) {
            if (!text.paragraphs) continue;
            
            const paragraphs = Array.isArray(text.paragraphs.paragraph) ? text.paragraphs.paragraph : [text.paragraphs.paragraph];
            
            for (const paragraph of paragraphs) {
                if (!paragraph.sentence) continue;
                
                const sentences = Array.isArray(paragraph.sentence) ? paragraph.sentence : [paragraph.sentence];
                
                for (const sentence of sentences) {
                    if (!sentence.tokens) continue;
                    
                    const tokens = Array.isArray(sentence.tokens.token) ? sentence.tokens.token : [sentence.tokens.token];
                    
                    for (const token of tokens) {
                        if (!token.tfr || !token.tfr.v || !token.tfr.v.l) continue;
                        
                        const lemma = token.tfr.v.l;
                        const word = token.text.toLowerCase();
                        
                        // Пропускаем знаки препинания и служебные слова
                        if (lemma.g && (lemma.g === 'PNCT' || lemma.g === 'PREP' || lemma.g === 'PRCL')) {
                            continue;
                        }
                        
                        // Извлекаем морфологические признаки
                        const features = extractMorphologicalFeatures(lemma);
                        
                        if (features && !uniqueWords.has(word)) {
                            uniqueWords.add(word);
                            morphologyData.metadata.words[word] = features;
                            wordCount++;
                        }
                    }
                }
            }
        }
        
        morphologyData.metadata.total_words = wordCount;
        
        console.log(`Извлечено ${wordCount} уникальных слов`);
        return morphologyData;
        
    } catch (error) {
        console.error('Ошибка парсинга XML:', error);
        return null;
    }
}

// Функция для извлечения морфологических признаков
function extractMorphologicalFeatures(lemma) {
    if (!lemma.g) return null;
    
    const features = {
        lemma: lemma.t,
        pos: null,
        gender: null,
        number: null,
        case: null,
        declension: null,
        conjugation: null,
        aspect: null,
        transitivity: null,
        mood: null,
        tense: null,
        person: null,
        animacy: null,
        degree: null
    };
    
    // Обрабатываем грамматические признаки
    const grammemes = Array.isArray(lemma.g) ? lemma.g : [lemma.g];
    
    for (const grammeme of grammemes) {
        switch (grammeme.v) {
            // Части речи
            case 'NOUN':
                features.pos = 'NOUN';
                break;
            case 'VERB':
                features.pos = 'VERB';
                break;
            case 'INFN':
                features.pos = 'VERB';
                features.mood = 'INFINITIVE';
                break;
            case 'ADJF':
                features.pos = 'ADJECTIVE';
                break;
            case 'ADJS':
                features.pos = 'ADJECTIVE';
                features.degree = 'SHORT';
                break;
            case 'COMP':
                features.pos = 'ADJECTIVE';
                features.degree = 'COMPARATIVE';
                break;
            case 'ADVB':
                features.pos = 'ADVERB';
                break;
            case 'CONJ':
                features.pos = 'CONJUNCTION';
                break;
            case 'PRCL':
                features.pos = 'PARTICLE';
                break;
            case 'PREP':
                features.pos = 'PREPOSITION';
                break;
            case 'NPRO':
                features.pos = 'PRONOUN';
                break;
            case 'NUMR':
                features.pos = 'NUMERAL';
                break;
            case 'INTJ':
                features.pos = 'INTERJECTION';
                break;
                
            // Род
            case 'masc':
                features.gender = 'MASCULINE';
                break;
            case 'femn':
                features.gender = 'FEMININE';
                break;
            case 'neut':
                features.gender = 'NEUTER';
                break;
                
            // Число
            case 'sing':
                features.number = 'SINGULAR';
                break;
            case 'plur':
                features.number = 'PLURAL';
                break;
                
            // Падеж
            case 'nomn':
                features.case = 'NOMINATIVE';
                break;
            case 'gent':
                features.case = 'GENITIVE';
                break;
            case 'datv':
                features.case = 'DATIVE';
                break;
            case 'accs':
                features.case = 'ACCUSATIVE';
                break;
            case 'ablt':
                features.case = 'INSTRUMENTAL';
                break;
            case 'loct':
            case 'loc1':
            case 'loc2':
                features.case = 'PREPOSITIONAL';
                break;
                
            // Одушевленность
            case 'anim':
                features.animacy = 'ANIMATE';
                break;
            case 'inan':
                features.animacy = 'INANIMATE';
                break;
                
            // Вид глагола
            case 'perf':
                features.aspect = 'PERFECTIVE';
                break;
            case 'impf':
                features.aspect = 'IMPERFECTIVE';
                break;
                
            // Переходность
            case 'tran':
                features.transitivity = 'TRANSITIVE';
                break;
            case 'intr':
                features.transitivity = 'INTRANSITIVE';
                break;
                
            // Наклонение
            case 'indc':
                features.mood = 'INDICATIVE';
                break;
            case 'impr':
                features.mood = 'IMPERATIVE';
                break;
                
            // Время
            case 'pres':
                features.tense = 'PRESENT';
                break;
            case 'past':
                features.tense = 'PAST';
                break;
            case 'futr':
                features.tense = 'FUTURE';
                break;
                
            // Лицо
            case '1per':
                features.person = '1';
                break;
            case '2per':
                features.person = '2';
                break;
            case '3per':
                features.person = '3';
                break;
        }
    }
    
    // Определяем склонение для существительных
    if (features.pos === 'NOUN' && features.case === 'NOMINATIVE' && features.number === 'SINGULAR') {
        features.declension = determineDeclension(features.lemma, features.gender);
    }
    
    // Определяем спряжение для глаголов
    if (features.pos === 'VERB' && features.mood === 'INFINITIVE') {
        features.conjugation = determineConjugation(features.lemma);
    }
    
    return features;
}

// Функция определения склонения
function determineDeclension(lemma, gender) {
    if (gender === 'FEMININE' && lemma.endsWith('ь')) {
        return '3rd';
    } else if (lemma.endsWith('а') || lemma.endsWith('я')) {
        return '1st';
    } else if (lemma.endsWith('о') || lemma.endsWith('е') || gender === 'NEUTER') {
        return '2nd';
    } else if (lemma.endsWith('мя')) {
        return 'heteroclitic';
    } else if (lemma.endsWith('о') && !lemma.endsWith('мя')) {
        // Проверяем несклоняемые
        const indeclinableEndings = ['кофе', 'какао', 'радио', 'метро', 'кино', 'кабаре', 'бюро', 'депо', 'фойе', 'ателье', 'кафе', 'пенсне', 'колье'];
        if (indeclinableEndings.includes(lemma)) {
            return 'indeclinable';
        }
        return '2nd';
    } else {
        return '1st';
    }
}

// Функция определения спряжения
function determineConjugation(lemma) {
    const secondConjugationEndings = ['ить', 'ать', 'ять', 'еть', 'уть', 'оть'];
    const secondConjugationExceptions = ['брить', 'стелить', 'зиждиться'];
    
    if (secondConjugationExceptions.includes(lemma)) {
        return '2nd';
    }
    
    for (let ending of secondConjugationEndings) {
        if (lemma.endsWith(ending)) {
            return '2nd';
        }
    }
    
    return '1st';
}

// Основная функция
async function main() {
    const inputFile = process.argv[2] || 'annot.opcorpora.no_ambig.xml';
    const outputFile = process.argv[3] || 'opencorpora_morphology.json';
    
    console.log(`Парсинг ${inputFile}...`);
    
    const morphologyData = await parseOpenCorporaXML(inputFile);
    
    if (morphologyData) {
        fs.writeFileSync(outputFile, JSON.stringify(morphologyData, null, 2), 'utf8');
        console.log(`Результат сохранен в ${outputFile}`);
        console.log(`Всего слов: ${morphologyData.metadata.total_words}`);
    } else {
        console.error('Ошибка парсинга');
    }
}

if (require.main === module) {
    main();
}

module.exports = { parseOpenCorporaXML, extractMorphologicalFeatures };
