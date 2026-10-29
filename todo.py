# -*- coding: utf-8 -*-
import argparse
import json
import sys
from pathlib import Path

# Принудительно UTF-8 для вывода в Windows-терминале
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

TASKS_FILE = Path(__file__).with_name('tasks.json')


def load_tasks():
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description):
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "description": description, "done": False})
    save_tasks(tasks)
    print(f'✅ Задача #{len(tasks)} добавлена.')


def list_tasks(show_all):
    tasks = load_tasks()
    if not tasks:
        print('📭 Задач нет.')
        return
    shown = 0
    for t in tasks:
        if not show_all and t["done"]:
            continue
        status = '✔' if t["done"] else '✖'
        print(f"#{t['id']} [{status}] {t['description']}")
        shown += 1
    if shown == 0:
        print('🎉 Все задачи выполнены! Используйте --all чтобы показать их.')


def mark_done(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            if t['done']:
                print(f'ℹ️  Задача #{task_id} уже была отмечена как выполненная.')
                return
            t['done'] = True
            save_tasks(tasks)
            print(f'✔ Задача #{task_id} отмечена как выполненная.')
            return
    print(f'❌ Задача #{task_id} не найдена.')


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        print(f'❌ Задача #{task_id} не найдена.')
        return
    # Пересчитываем ID, чтобы не было «дырок»
    for i, t in enumerate(new_tasks, start=1):
        t['id'] = i
    save_tasks(new_tasks)
    print(f'🗑 Задача #{task_id} удалена.')


def clear_tasks():
    if TASKS_FILE.exists():
        TASKS_FILE.unlink()
    print('🗑 Все задачи удалены.')


def main():
    parser = argparse.ArgumentParser(
        prog='todo',
        description='📋 Простой Todo-лист в командной строке',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest='command', metavar='команда')

    # добавить
    parser_add = subparsers.add_parser('add', help='Добавить новую задачу')
    parser_add.add_argument('description', nargs='+', help='Текст задачи')

    # список
    parser_list = subparsers.add_parser('list', help='Показать задачи')
    parser_list.add_argument('-a', '--all', action='store_true',
                             help='Показать в том числе выполненные задачи')

    # выполнено
    parser_done = subparsers.add_parser('done', help='Отметить задачу как выполненную')
    parser_done.add_argument('id', type=int, help='ID задачи')

    # удалить
    parser_del = subparsers.add_parser('delete', help='Удалить задачу')
    parser_del.add_argument('id', type=int, help='ID задачи')

    # очистить
    subparsers.add_parser('clear', help='Удалить все задачи')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(' '.join(args.description))
    elif args.command == 'list':
        list_tasks(args.all)
    elif args.command == 'done':
        mark_done(args.id)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'clear':
        clear_tasks()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()