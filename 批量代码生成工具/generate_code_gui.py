# 批量代码生成工具
# generate_code_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox

def generate_code_snippets(start_num, end_num, category, prefix='images/fun/', ext='.jpg'):
    """生成代码片段"""
    snippets = []
    for num in range(start_num, end_num + 1):
        snippet = f"{{src: '{prefix}{num}{ext}', category: '{category}'}}"
        snippets.append(snippet)
    return snippets

def save_to_file(snippets, filename='output.txt'):
    """将代码片段保存到文件"""
    with open(filename, 'w') as file:
        for snippet in snippets:
            file.write(snippet + ',\n')

def generate_and_save():
    try:
        start_num = int(start_num_entry.get())
        end_num = int(end_num_entry.get())
        category = category_entry.get() or 'fun'
        prefix = prefix_entry.get() or 'images/fun/'
        ext = ext_entry.get() or '.jpg'
        filename = filename_entry.get() or 'output.txt'
        
        snippets = generate_code_snippets(start_num, end_num, category, prefix, ext)
        save_to_file(snippets, filename)
        
        messagebox.showinfo("成功", f"代码片段已保存到 {filename}")
    except ValueError:
        messagebox.showerror("错误", "起始编号和结束编号必须是整数。")

app = tk.Tk()
app.title("批量代码生成工具")

tk.Label(app, text="起始编号:").grid(row=0, column=0, padx=10, pady=5)
start_num_entry = tk.Entry(app)
start_num_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="结束编号:").grid(row=1, column=0, padx=10, pady=5)
end_num_entry = tk.Entry(app)
end_num_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="类别 (默认为 'fun'):").grid(row=2, column=0, padx=10, pady=5)
category_entry = tk.Entry(app)
category_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="前缀 (默认为 'images/fun/'):").grid(row=3, column=0, padx=10, pady=5)
prefix_entry = tk.Entry(app)
prefix_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(app, text="文件扩展名 (默认为 '.jpg'):").grid(row=4, column=0, padx=10, pady=5)
ext_entry = tk.Entry(app)
ext_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(app, text="输出文件名 (默认为 'output.txt'):").grid(row=5, column=0, padx=10, pady=5)
filename_entry = tk.Entry(app)
filename_entry.grid(row=5, column=1, padx=10, pady=5)

generate_button = tk.Button(app, text="生成代码", command=generate_and_save)
generate_button.grid(row=6, columnspan=2, pady=10)

app.mainloop()
