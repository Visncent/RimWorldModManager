# RimWorld Mod Manager

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

Программа для управления модами RimWorld с поддержкой:
- Автосортировки по зависимостям
- Проверки конфликтов
- Контроля целостности файлов

## 📦 Установка
1. Клонируйте репозиторий:
     ```bash
     git clone https://github.com/ваш-ник/RimWorldModManager.git
     cd RimWorldModManager
2. Установите зависимости:
    bash
    pip install -r requirements.txt
## 🔧 Функционал
Функция	                      Описание
Топологическая сортировка	    Автоматический порядок загрузки модов
Проверка зависимостей	        Поиск отсутствующих модов
Валидация файлов	            Сравнение хешей критических DLL
Резервное копирование	        Автосохранение ModsConfig.xml
