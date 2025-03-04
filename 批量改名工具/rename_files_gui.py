import os
import tkinter as tk
from tkinter import filedialog, messagebox

def rename_files_in_directory(directory, start_number, extensions):
    files = [f for f in os.listdir(directory) if any(f.endswith(ext) for ext in extensions)]
    files.sort()  # 排序文件名

    # 临时重命名所有文件以防止名称冲突
    temp_names = []
    for filename in files:
        temp_name = f"temp_{filename}"
        os.rename(os.path.join(directory, filename), os.path.join(directory, temp_name))
        temp_names.append(temp_name)
    
    # 按照最终名称重命名文件
    for index, temp_name in enumerate(temp_names):
        ext = os.path.splitext(temp_name)[1]
        new_name = f"{start_number + index}{ext}"
        os.rename(os.path.join(directory, temp_name), os.path.join(directory, new_name))
        print(f"重命名 {temp_name} 为 {new_name}")

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def start_renaming():
    folder_path = folder_entry.get()
    start_number = int(start_number_entry.get())
    extensions = [extension_var.get()]

    try:
        rename_files_in_directory(folder_path, start_number, extensions)
        messagebox.showinfo("完成", "文件重命名完成！")
    except Exception as e:
        messagebox.showerror("错误", str(e))

# 创建GUI
root = tk.Tk()
root.title("批量重命名工具")

tk.Label(root, text="文件夹路径:").grid(row=0, column=0, sticky=tk.W)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="选择文件夹", command=select_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="起始编号:").grid(row=1, column=0, sticky=tk.W)
start_number_entry = tk.Entry(root)
start_number_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="文件扩展名:").grid(row=2, column=0, sticky=tk.W)
extension_var = tk.StringVar(root)
extension_var.set(".jpg")  # 默认选项
extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".ico"]
extension_menu = tk.OptionMenu(root, extension_var, *extensions)
extension_menu.grid(row=2, column=1, padx=5, pady=5)

tk.Button(root, text="开始重命名", command=start_renaming).grid(row=3, columnspan=3, pady=10)

root.mainloop()
