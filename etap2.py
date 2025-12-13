import tkinter as tk
from tkinter import messagebox, filedialog

TABLE_SIZE = 10
hash_table = [[] for _ in range(TABLE_SIZE)]

def h(key):
    return sum(ord(c) for c in key)

CELL_W = 120
CELL_H = 45
CELL_MARGIN = 5

def draw_table(highlight_index=None):
    canvas.delete("all")
    y_offset = 10
    line_height = 15

    for i in range(TABLE_SIZE):
        bucket = hash_table[i]
        bucket_height = max(CELL_H, line_height * len(bucket) + 10)

        x1 = 10
        y1 = y_offset
        x2 = x1 + CELL_W
        y2 = y1 + bucket_height

        color = "white"
        if i == highlight_index:
            color = "yellow"

        canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        canvas.create_text(x1 + 20, y1 + 20, text=str(i), font=("Arial", 12, "bold"))

        for j, (k, v) in enumerate(bucket):
            canvas.create_text(
                x2 + 10,
                y1 + 5 + j * line_height,
                text=f"{k}:{v}",
                font=("Consolas", 11),
                anchor="nw",
            )
        y_offset += bucket_height + CELL_MARGIN

    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def update_chart():
    chart_canvas.delete("all")
    bucket_sizes = [len(b) for b in hash_table]
    max_height = max(bucket_sizes + [1])
    width = 30
    spacing = 10
    margin = 10
    canvas_height = int(chart_canvas['height'])

    for i, size in enumerate(bucket_sizes):
        x0 = margin + i * (width + spacing)
        y0 = canvas_height - (size / max_height * (canvas_height - 20))
        x1 = x0 + width
        y1 = canvas_height
        chart_canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")
        chart_canvas.create_text(x0 + width/2, y0 - 5, text=str(size), anchor="s")
        chart_canvas.create_text(x0 + width/2, y1 + 10, text=str(i), anchor="n")

def do_search(key=None):
    key = key or entry_key.get()
    if not key:
        messagebox.showwarning("Uwaga", "Podaj klucz!")
        return
    index = h(key) % TABLE_SIZE
    draw_table(index)
    bucket = hash_table[index]
    for k, v in bucket:
        if k == key:
            update_chart()
            return
    update_chart()

def do_insert(key=None, value=None):
    key = key or entry_key.get()
    value = value or entry_val.get()
    if not key or not value:
        messagebox.showwarning("Uwaga", "Podaj klucz i wartość!")
        return
    index = h(key) % TABLE_SIZE
    bucket = hash_table[index]
    for i, (k, v) in enumerate(bucket):
        if k == key:
            bucket[i] = (key, value)
            draw_table(index)
            update_chart()
            return
    bucket.append((key, value))
    draw_table(index)
    update_chart()

def do_delete(key=None):
    key = key or entry_key.get()
    if not key:
        messagebox.showwarning("Uwaga", "Podaj klucz!")
        return
    index = h(key) % TABLE_SIZE
    bucket = hash_table[index]
    for i, (k, v) in enumerate(bucket):
        if k == key:
            del bucket[i]
            draw_table(index)
            update_chart()
            return
    draw_table(index)
    update_chart()

def load_file():
    file_path = filedialog.askopenfilename(title="Wybierz plik", filetypes=[("Text Files","*.txt"),("All files","*.*")])
    if not file_path:
        return
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            cmd = parts[0].upper()
            if cmd=="INSERT" and len(parts)>=3:
                key,value = parts[1], " ".join(parts[2:])
                do_insert(key,value)
            elif cmd=="SEARCH" and len(parts)==2:
                do_search(parts[1])
            elif cmd=="DELETE" and len(parts)==2:
                do_delete(parts[1])

root = tk.Tk()
root.title("Hashowanie łańcuchowe")

controls = tk.Frame(root, padx=10, pady=10)
controls.pack(side="left", fill="y")

tk.Label(controls, text="Klucz:").pack()
entry_key = tk.Entry(controls); entry_key.pack(pady=5)
tk.Label(controls, text="Wartość:").pack()
entry_val = tk.Entry(controls); entry_val.pack(pady=5)

tk.Button(controls,text="SEARCH",command=do_search).pack(pady=5)
tk.Button(controls,text="INSERT",command=do_insert).pack(pady=5)
tk.Button(controls,text="DELETE",command=do_delete).pack(pady=5)
tk.Button(controls,text="ZALADUJ Z PLIKU",command=load_file).pack(pady=5)

tk.Label(controls,text="Rozkład elementów w bucketach:").pack(pady=5)
chart_canvas = tk.Canvas(controls, width=450, height=300, bg="white")
chart_canvas.pack(pady=5)

canvas_frame = tk.Frame(root)
canvas_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

canvas_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
canvas_scrollbar.pack(side="right", fill="y")

canvas = tk.Canvas(canvas_frame, width=450, height=600, bg="white",
                   yscrollcommand=canvas_scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

canvas_scrollbar.config(command=canvas.yview)

draw_table()
update_chart()
root.mainloop()
