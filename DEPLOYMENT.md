# 🚀 Развертывание на GitHub Pages

## Подготовка к публикации

### 1. Создание GitHub репозитория

```bash
# Инициализация Git репозитория
git init

# Добавление файлов
git add .

# Первый коммит
git commit -m "Initial commit: Russian Language Practice App"

# Создание основной ветки
git branch -M main

# Добавление удаленного репозитория (замените yourusername на ваш GitHub username)
git remote add origin https://github.com/yourusername/russian-language-project.git

# Отправка в GitHub
git push -u origin main
```

### 2. Настройка GitHub Pages

1. Перейдите в ваш репозиторий на GitHub
2. Нажмите на вкладку **Settings**
3. Прокрутите вниз до раздела **Pages**
4. В разделе **Source** выберите **Deploy from a branch**
5. В разделе **Branch** выберите **main**
6. Нажмите **Save**

### 3. Доступ к приложению

После настройки GitHub Pages ваше приложение будет доступно по адресу:
```
https://yourusername.github.io/russian-language-project/
```

## 📁 Файлы для GitHub

### Включить в репозиторий:
- ✅ `russian_language_practice.html` - основное приложение
- ✅ `opencorpora_optimized.json` - оптимизированный корпус (1.7MB)
- ✅ `README.md` - документация
- ✅ `TROUBLESHOOTING.md` - решение проблем
- ✅ `optimize_corpus.py` - скрипт оптимизации
- ✅ `parse_opencorpora.py` - парсер OpenCorpora
- ✅ `.gitignore` - исключения для Git

### Исключить из репозитория:
- ❌ `annot.opcorpora.xml` - слишком большой (200MB+)
- ❌ `annot.opcorpora.no_ambig.xml` - слишком большой (50MB+)
- ❌ `opencorpora_no_ambig.json` - слишком большой (8.6MB)
- ❌ `test_corpus.json` - временный файл
- ❌ `package.json` - не нужен для веб-версии

## 🔧 Оптимизация для веб-хостинга

### Размер файлов:
- **opencorpora_optimized.json**: 1.7MB (4,256 слов)
- **russian_language_practice.html**: ~50KB
- **Общий размер**: ~1.8MB

### Преимущества оптимизации:
- ✅ Быстрая загрузка страницы
- ✅ Меньше трафика
- ✅ Лучший пользовательский опыт
- ✅ Совместимость с GitHub Pages

## 🌐 Обновление приложения

### Добавление изменений:
```bash
# Добавление изменений
git add .

# Коммит с описанием
git commit -m "Описание изменений"

# Отправка в GitHub
git push origin main
```

### GitHub Pages автоматически обновится через несколько минут.

## 📊 Мониторинг

### Проверка статуса развертывания:
1. Перейдите в **Actions** в вашем репозитории
2. Проверьте статус последнего развертывания
3. При ошибках проверьте логи

### Проверка доступности:
1. Откройте URL вашего приложения
2. Проверьте консоль браузера (F12)
3. Убедитесь, что корпус загружается

## 🎯 Результат

После развертывания у вас будет:
- 🌐 **Публично доступное приложение** на GitHub Pages
- 📱 **Работает на любых устройствах** (компьютер, планшет, телефон)
- 🚀 **Быстрая загрузка** благодаря оптимизации
- 🔄 **Автоматическое обновление** при изменениях
- 📊 **Статистика использования** через GitHub Analytics

## 🔗 Полезные ссылки

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [OpenCorpora Project](https://opencorpora.org/)
- [Russian Language Learning Resources](https://www.russianforfree.com/)

---

**Готово! Ваше приложение теперь доступно всему миру! 🌍**
