import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect(':memory:')  # use ':memory:' or 'notes.db'
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
''')
conn.commit()

# ---------------- TKINTER SETUP ----------------
root = tk.Tk()
root.title("Sticky Notes!")
root.configure(bg="#87CEEB")

# ---------------- FUNCTIONS ----------------
def add_note(title, content):
    if not title.strip():
        messagebox.showwarning("Warning", "Title cannot be empty!")
        return

    c.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content.strip())
    )
    conn.commit()

    messagebox.showinfo("Note Created", "Note added successfully!")
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    view_notes()

def view_notes():
    notes_listbox.delete(0, tk.END)
    for row in c.execute("SELECT id, title, content FROM notes"):
        notes_listbox.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]}")

def delete_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a note to delete")
        return

    note_text = notes_listbox.get(selected[0])
    note_id = int(note_text.split(".")[0])

    c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()

    messagebox.showinfo("Note Deleted", "Note deleted successfully!")
    view_notes()

# ---------------- GUI COMPONENTS ----------------
title_label = tk.Label(root, text="Title:", bg="#FFC0CB")
title_label.pack(pady=5)

title_entry = tk.Entry(root, width=50)
title_entry.pack()

content_label = tk.Label(root, text="Content:", bg="#FFC0CB")
content_label.pack(pady=5)

content_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
content_text.pack()

add_button = tk.Button(
    root,
    text="Add Note",
    bg="#FDFD96",
    command=lambda: add_note(
        title_entry.get(),
        content_text.get("1.0", tk.END)
    )
)
add_button.pack(pady=5)

view_button = tk.Button(
    root,
    text="View Notes",
    bg="#FDFD96",
    command=view_notes
)
view_button.pack(pady=5)

delete_button = tk.Button(
    root,
    text="Delete Note",
    bg="#FDFD96",
    command=delete_note
)
delete_button.pack(pady=5)

notes_label = tk.Label(root, text="Saved Notes:", bg="#FFC0CB")
notes_label.pack(pady=5)

notes_listbox = tk.Listbox(root, width=60)
notes_listbox.pack(pady=5)

# ---------------- RUN APP ----------------
root.mainloop()
