#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания офлайн-пакета приложения "Русский язык"
Создает папку со всеми необходимыми файлами для работы без интернета
"""

import os
import shutil
import sys
from pathlib import Path

def create_offline_package():
    """Создает папку с файлами для офлайн работы"""
    
    # Определяем пути
    current_dir = Path(__file__).parent
    offline_dir = current_dir / "russian_language_offline"
    
    # Список файлов для копирования
    required_files = [
        "index.html",
        "opencorpora.json", 
        "Lesha-1.png"
    ]
    
    optional_files = [
        "README.md",
        "OFFLINE_SETUP.md"
    ]
    
    print("🚀 Создание офлайн-пакета для приложения 'Русский язык'...")
    print(f"📁 Целевая папка: {offline_dir}")
    
    # Создаем папку
    if offline_dir.exists():
        print("⚠️  Папка уже существует. Удаляем старую версию...")
        shutil.rmtree(offline_dir)
    
    offline_dir.mkdir()
    print("✅ Папка создана")
    
    # Копируем обязательные файлы
    print("\n📋 Копируем обязательные файлы:")
    for file_name in required_files:
        source_file = current_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, offline_dir)
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} - файл не найден!")
            return False
    
    # Копируем опциональные файлы
    print("\n📋 Копируем дополнительные файлы:")
    for file_name in optional_files:
        source_file = current_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, offline_dir)
            print(f"  ✅ {file_name}")
        else:
            print(f"  ⚠️  {file_name} - файл не найден (пропускаем)")
    
    # Создаем файл с инструкциями по настройке браузера
    browser_setup_content = """# 🌐 Настройка браузера для офлайн работы

## Путь к файлу для домашней страницы:

### Windows:
file:///C:/путь/к/папке/russian_language_offline/index.html

### macOS:
file:///Users/имя_пользователя/путь/к/папке/russian_language_offline/index.html

### Linux:
file:///home/имя_пользователя/путь/к/папке/russian_language_offline/index.html

## Инструкции по настройке:

### Chrome/Edge:
1. Откройте chrome://settings/
2. В разделе "При запуске" выберите "Открыть определенную страницу"
3. Нажмите "Добавить новую страницу"
4. Вставьте путь к файлу выше

### Firefox:
1. Откройте about:preferences
2. В разделе "Общие" найдите "Домашняя страница"
3. Вставьте путь к файлу выше

### Safari (macOS):
1. Safari → Настройки → Общие
2. В поле "Домашняя страница" вставьте путь к файлу выше

## Проверка работы:
Откройте файл index.html в браузере для проверки.
"""
    
    browser_setup_file = offline_dir / "BROWSER_SETUP.txt"
    with open(browser_setup_file, 'w', encoding='utf-8') as f:
        f.write(browser_setup_content)
    print(f"  ✅ BROWSER_SETUP.txt")
    
    # Выводим итоговую информацию
    print(f"\n🎉 Офлайн-пакет создан успешно!")
    print(f"📁 Расположение: {offline_dir}")
    print(f"📄 Главный файл: {offline_dir / 'index.html'}")
    
    print(f"\n📋 Содержимое папки:")
    for item in sorted(offline_dir.iterdir()):
        size = item.stat().st_size if item.is_file() else 0
        size_str = f"({size:,} байт)" if size > 0 else "(папка)"
        print(f"  📄 {item.name} {size_str}")
    
    print(f"\n🌐 Для настройки браузера:")
    print(f"   1. Откройте файл: {offline_dir / 'index.html'}")
    print(f"   2. Скопируйте путь из адресной строки")
    print(f"   3. Используйте этот путь как домашнюю страницу")
    
    return True

if __name__ == "__main__":
    try:
        success = create_offline_package()
        if success:
            print(f"\n✅ Готово! Приложение готово для офлайн работы.")
            sys.exit(0)
        else:
            print(f"\n❌ Ошибка при создании пакета.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
