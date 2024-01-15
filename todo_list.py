import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Todo List App")
        self.geometry("400x400")
        style = ttk.Style()
        style.theme_use("clam")

        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

        self.task_input = ttk.Entry(self, font=(
            "TkDefaultFont", 16), width=30)
        self.task_input.pack(pady=10)

        self.task_input.insert(0, "Enter your todo here...")

        self.task_input.bind("<FocusIn>", self.clear_placeholder)
        self.task_input.bind("<FocusOut>", self.restore_placeholder)

        ttk.Button(self, text="Add", command=self.add_task).pack(pady=5)

        self.task_list = tk.Listbox(self, font=(
            "TkDefaultFont", 16), height=10, selectmode=tk.NONE)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(self, text="Done", command=self.mark_done).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(self, text="Delete", command=self.delete_task).pack(side=tk.RIGHT, padx=10, pady=10)

        ttk.Button(self, text="View Stats", command=self.view_stats).pack(side=tk.BOTTOM, pady=10)

        ttk.Button(self, text="Exit", command=self.exit_app).pack(side=tk.BOTTOM, pady=10)

        self.load_tasks()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    color TEXT
                )
            ''')

    def view_stats(self):
        done_count = 0
        total_count = self.task_list.size()
        for i in range(total_count):
            if self.task_list.itemcget(i, "fg") == "green":
                done_count += 1
        messagebox.showinfo("Task Statistics", f"Total tasks: {total_count}\nCompleted tasks: {done_count}")

    def add_task(self):
        task = self.task_input.get()
        if task != "Enter your todo here...":
            self.task_list.insert(tk.END, task)
            self.task_list.itemconfig(tk.END, fg="orange")
            self.task_input.delete(0, tk.END)
            self.save_task_to_db(task, "orange")

    def mark_done(self):
        task_index = self.task_list.curselection()
        if task_index:
            self.task_list.itemconfig(task_index, fg="green")
            task_id = task_index[0] + 1
            self.update_task_in_db(task_id, "green")

    def delete_task(self):
        task_index = self.task_list.curselection()
        if task_index:
            task_id = task_index[0] + 1 
            self.task_list.delete(task_index)
            self.delete_task_from_db(task_id)

    def exit_app(self):
        result = messagebox.askokcancel("Exit Application", "Are you sure you want to exit?")
        if result:
            self.destroy()

    def clear_placeholder(self, event):
        if self.task_input.get() == "Enter your todo here...":
            self.task_input.delete(0, tk.END)

    def restore_placeholder(self, event):
        if self.task_input.get() == "":
            self.task_input.insert(0, "Enter your todo here...")

    def load_tasks(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM tasks")
            for row in cursor:
                task_id, text, color = row
                self.task_list.insert(tk.END, text)
                self.task_list.itemconfig(tk.END, fg=color)

    def save_task_to_db(self, text, color):
        with self.conn:
            self.conn.execute("INSERT INTO tasks (text, color) VALUES (?, ?)", (text, color))

    def update_task_in_db(self, task_id, color):
        with self.conn:
            self.conn.execute("UPDATE tasks SET color = ? WHERE id = ?", (color, task_id))

    def delete_task_from_db(self, task_id):
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def __del__(self):
        self.conn.close()

if __name__ == '__main__':
    app = TodoListApp()
    app.mainloop()