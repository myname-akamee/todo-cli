# -*- coding: utf-8 -*-
"""
Графическое приложение Todo-лист (Tkinter)
Полностью совместимо с CLI (todo.py) и файлом tasks.json.
Расширение .pyw позволяет запускать приложение без консольного окна.
"""

import json
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, font

# Путь к файлу с задачами (в той же директории)
BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.json"

# Цветовая палитра (современный минималистичный дизайн)
COLORS = {
    "bg": "#F3F4F6",            # Светло-серый фон
    "card_bg": "#FFFFFF",       # Белый фон карточек
    "card_done": "#F9FAFB",     # Фон выполненной карточки
    "primary": "#4F46E5",       # Индиго / фиолетовый акцент
    "primary_hover": "#4338CA",
    "text": "#111827",          # Основной текст
    "text_muted": "#6B7280",    # Второстепенный текст
    "text_done": "#9CA3AF",     # Текст завершенной задачи
    "border": "#E5E7EB",        # Границы
    "danger": "#EF4444",        # Красный (удаление)
    "danger_hover": "#DC2626",
    "success": "#10B981",       # Зеленый
}


def load_tasks():
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить задачи:\n{e}")


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Мой Todo Лист")
        self.geometry("520x680")
        self.minsize(450, 500)
        self.configure(bg=COLORS["bg"])

        # Центрирование окна
        self.center_window(520, 680)

        self.current_filter = "all"  # 'all', 'active', 'completed'
        self.tasks = load_tasks()

        self.setup_fonts()
        self.create_widgets()
        self.refresh_tasks_display()

    def center_window(self, width, height):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = max(0, int((screen_w - width) / 2))
        y = max(0, int((screen_h - height) / 2) - 40)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_fonts(self):
        self.font_title = font.Font(family="Segoe UI", size=18, weight="bold")
        self.font_sub = font.Font(family="Segoe UI", size=10)
        self.font_main = font.Font(family="Segoe UI", size=11)
        self.font_done = font.Font(family="Segoe UI", size=11, overstrike=True)
        self.font_btn = font.Font(family="Segoe UI", size=10, weight="bold")
        self.font_small = font.Font(family="Segoe UI", size=9)

    def create_widgets(self):
        # 1. Шапка (Заголовок и счетчик)
        header_frame = tk.Frame(self, bg=COLORS["bg"])
        header_frame.pack(fill="x", padx=24, pt=0, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="Мои задачи",
            font=self.font_title,
            fg=COLORS["text"],
            bg=COLORS["bg"]
        )
        title_label.pack(side="left")

        self.counter_label = tk.Label(
            header_frame,
            text="",
            font=self.font_sub,
            fg=COLORS["text_muted"],
            bg=COLORS["bg"]
        )
        self.counter_label.pack(side="right", pady=(8, 0))

        # 2. Поле ввода новой задачи
        input_card = tk.Frame(self, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1)
        input_card.pack(fill="x", padx=24, pady=10)

        self.entry_task = tk.Entry(
            input_card,
            font=self.font_main,
            fg=COLORS["text"],
            bg=COLORS["card_bg"],
            relief="flat",
            bd=0
        )
        self.entry_task.pack(side="left", fill="x", expand=True, padx=14, pady=12)
        self.entry_task.bind("<Return>", lambda e: self.add_task())

        btn_add = tk.Button(
            input_card,
            text="+ Добавить",
            font=self.font_btn,
            fg="#FFFFFF",
            bg=COLORS["primary"],
            activebackground=COLORS["primary_hover"],
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=8,
            command=self.add_task
        )
        btn_add.pack(side="right", padx=6, pady=6)

        # 3. Фильтры (Все / В работе / Готово)
        filter_frame = tk.Frame(self, bg=COLORS["bg"])
        filter_frame.pack(fill="x", padx=24, pady=(6, 10))

        self.btn_filter_all = self.create_filter_btn(filter_frame, "Все", "all")
        self.btn_filter_active = self.create_filter_btn(filter_frame, "В работе", "active")
        self.btn_filter_done = self.create_filter_btn(filter_frame, "Выполненные", "completed")

        self.btn_filter_all.pack(side="left", padx=(0, 6))
        self.btn_filter_active.pack(side="left", padx=6)
        self.btn_filter_done.pack(side="left", padx=6)

        # 4. Прокручиваемый список задач
        list_container = tk.Frame(self, bg=COLORS["bg"])
        list_container.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        self.canvas = tk.Canvas(list_container, bg=COLORS["bg"], bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(list_container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg"])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=None, yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Привязка скролла мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        # 5. Нижняя панель (Очистить выполненные)
        bottom_frame = tk.Frame(self, bg=COLORS["bg"])
        bottom_frame.pack(fill="x", padx=24, pady=(0, 16))

        btn_clear_done = tk.Button(
            bottom_frame,
            text="Очистить выполненные",
            font=self.font_small,
            fg=COLORS["text_muted"],
            bg=COLORS["bg"],
            activebackground=COLORS["border"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_completed
        )
        btn_clear_done.pack(side="left")

        btn_clear_all = tk.Button(
            bottom_frame,
            text="Удалить все",
            font=self.font_small,
            fg=COLORS["danger"],
            bg=COLORS["bg"],
            activebackground=COLORS["border"],
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_all
        )
        btn_clear_all.pack(side="right")

    def _on_mousewheel(self, event):
        if self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_frame_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def create_filter_btn(self, parent, text, mode):
        btn = tk.Button(
            parent,
            text=text,
            font=self.font_small,
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=lambda: self.set_filter(mode)
        )
        return btn

    def set_filter(self, mode):
        self.current_filter = mode
        self.update_filter_buttons()
        self.refresh_tasks_display()

    def update_filter_buttons(self):
        buttons = [
            (self.btn_filter_all, "all"),
            (self.btn_filter_active, "active"),
            (self.btn_filter_done, "completed"),
        ]
        for btn, mode in buttons:
            if self.current_filter == mode:
                btn.configure(
                    bg=COLORS["primary"],
                    fg="#FFFFFF",
                    activebackground=COLORS["primary_hover"],
                    activeforeground="#FFFFFF"
                )
            else:
                btn.configure(
                    bg=COLORS["card_bg"],
                    fg=COLORS["text_muted"],
                    activebackground=COLORS["border"],
                    activeforeground=COLORS["text"]
                )

    def add_task(self):
        text = self.entry_task.get().strip()
        if not text:
            return

        new_id = len(self.tasks) + 1
        self.tasks.append({
            "id": new_id,
            "description": text,
            "done": False
        })
        save_tasks(self.tasks)
        self.entry_task.delete(0, "end")
        self.refresh_tasks_display()

    def toggle_task(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = not t["done"]
                break
        save_tasks(self.tasks)
        self.refresh_tasks_display()

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        # Пересчет ID
        for idx, t in enumerate(self.tasks, start=1):
            t["id"] = idx
        save_tasks(self.tasks)
        self.refresh_tasks_display()

    def clear_completed(self):
        done_count = sum(1 for t in self.tasks if t["done"])
        if done_count == 0:
            return
        self.tasks = [t for t in self.tasks if not t["done"]]
        for idx, t in enumerate(self.tasks, start=1):
            t["id"] = idx
        save_tasks(self.tasks)
        self.refresh_tasks_display()

    def clear_all(self):
        if not self.tasks:
            return
        if messagebox.askyesno("Подтверждение", "Удалить абсолютно все задачи?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.refresh_tasks_display()

    def refresh_tasks_display(self):
        self.update_filter_buttons()

        # Очистить список
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["done"])
        self.counter_label.config(text=f"Выполнено {completed} из {total}")

        # Фильтрация
        filtered = []
        for t in self.tasks:
            if self.current_filter == "active" and t["done"]:
                continue
            if self.current_filter == "completed" and not t["done"]:
                continue
            filtered.append(t)

        if not filtered:
            msg = "Задач пока нет"
            if self.current_filter == "active":
                msg = "Все задачи выполнены! 🎉"
            elif self.current_filter == "completed":
                msg = "Пока нет завершённых задач"

            empty_frame = tk.Frame(self.scrollable_frame, bg=COLORS["bg"])
            empty_frame.pack(fill="x", pady=40)
            tk.Label(
                empty_frame,
                text=msg,
                font=self.font_main,
                fg=COLORS["text_muted"],
                bg=COLORS["bg"]
            ).pack()
            return

        for task in filtered:
            self.render_task_card(task)

    def render_task_card(self, task):
        t_id = task["id"]
        is_done = task["done"]

        bg_color = COLORS["card_done"] if is_done else COLORS["card_bg"]

        card = tk.Frame(
            self.scrollable_frame,
            bg=bg_color,
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )
        card.pack(fill="x", pady=4)

        # Кнопка-чекбокс (галочка / кружок)
        check_text = "✔" if is_done else "○"
        check_color = COLORS["success"] if is_done else COLORS["text_muted"]

        btn_check = tk.Button(
            card,
            text=check_text,
            font=("Segoe UI", 12, "bold"),
            fg=check_color,
            bg=bg_color,
            activebackground=bg_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            command=lambda tid=t_id: self.toggle_task(tid)
        )
        btn_check.pack(side="left", pady=10)

        # Текст задачи
        txt_font = self.font_done if is_done else self.font_main
        txt_color = COLORS["text_done"] if is_done else COLORS["text"]

        lbl_desc = tk.Label(
            card,
            text=f"{task['description']}",
            font=txt_font,
            fg=txt_color,
            bg=bg_color,
            anchor="w",
            wraplength=320,
            justify="left"
        )
        lbl_desc.pack(side="left", fill="x", expand=True, pady=10)
        # Клик по тексту также переключает статус
        lbl_desc.bind("<Button-1>", lambda e, tid=t_id: self.toggle_task(tid))

        # Кнопка удаления
        btn_del = tk.Button(
            card,
            text="✕",
            font=("Segoe UI", 10, "bold"),
            fg=COLORS["text_muted"],
            bg=bg_color,
            activebackground=bg_color,
            activeforeground=COLORS["danger"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            command=lambda tid=t_id: self.delete_task(tid)
        )
        btn_del.pack(side="right", pady=10)

        # Подсветка кнопки удаления при наведении
        def on_enter(e, b=btn_del):
            b.config(fg=COLORS["danger"])
        def on_leave(e, b=btn_del):
            b.config(fg=COLORS["text_muted"])
        btn_del.bind("<Enter>", on_enter)
        btn_del.bind("<Leave>", on_leave)


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
