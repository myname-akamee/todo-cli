# 📋 TaskFlow CLI & GUI (Todo Manager)

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-brightgreen?style=flat)](https://docs.python.org/3/library/tkinter.html)
[![Web](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3%20%2F%20JS-E34F26?style=flat&logo=html5&logoColor=white)](index.html)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Универсальный менеджер задач с поддержкой трех форматов работы: **консольная утилита (CLI)**, **десктопный интерфейс (Desktop GUI)** и **легковесный веб-интерфейс**. Все форматы синхронизируются через единое JSON-хранилище.

---

## ✨ Возможности

- ⚡ **CLI (Консоль):** мгновенное добавление, закрытие, просмотр и фильтрация задач из любого терминала.
- 🖥️ **Desktop GUI:** лаконичный нативный оконный интерфейс на Python Tkinter.
- 🌐 **Web UI:** адаптивный минималистичный веб-интерфейс (Notion/Apple style), темная/светлая тема, шкала прогресса, импорт/экспорт данных.
- 💾 **Автономность:** работает без внешних баз данных и тяжелых зависимостей, данные сохраняются локально.

---

## 🚀 Быстрый старт

### 1. Консольный интерфейс (CLI)

```bash
# Добавить задачу
python todo.py add "Подготовить резюме"

# Посмотреть активные задачи
python todo.py list

# Посмотреть все задачи (включая выполненные)
python todo.py list --all

# Отметить задачу как выполненную (по ID)
python todo.py done 1

# Удалить задачу
python todo.py delete 1

# Очистить список
python todo.py clear
```

### 2. Десктопный интерфейс (GUI)
- Запустите двойным кликом файл `run_gui.bat` или выполните:
```bash
python gui.pyw
```

### 3. Веб-интерфейс
- Откройте `index.html` в любом браузере (или запустите `open_web.bat`).

---

## 📂 Структура проекта

```text
├── todo.py        # CLI-утилита для управления задачами
├── gui.pyw        # Десктопное приложение (Tkinter)
├── index.html     # Веб-версия приложения
├── run_gui.bat    # Скрипт быстрого запуска GUI
├── open_web.bat   # Скрипт быстрого запуска Web-интерфейса
└── .gitignore     # Исключение временных файлов и пользовательской БД
```

---

## 🛠️ Стек технологий
- **Языки:** Python, JavaScript, HTML5, CSS3
- **Интерфейсы:** Tkinter, CLI, Modern Responsive Web
- **Хранение данных:** JSON Serialization
