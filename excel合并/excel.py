import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class ExcelMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 合并工具")
        self.root.geometry("800x700")
        # 设置窗口标题栏
        self.root.title("Excel 合并工具 - Liao Gong - 适用范围:Log简单筛选")


        # # 创建一个简单的导航栏
        # self.navbar = tk.Frame(self.root)
        # self.navbar.pack(fill="x", pady=10)
        
        # # 在导航栏中添加防伪信息
        # self.security_label = tk.Label(self.navbar, text="防伪信息: 正品保证", font=("Arial", 14, "bold"), fg="red")
        # self.security_label.pack(side="right", padx=20)

        # # 添加“著名”和“作者”信息
        # self.author_label = tk.Label(self.navbar, text="作者: 张三", font=("Arial", 12), fg="blue")
        # self.author_label.pack(side="left", padx=20)

        # self.famous_label = tk.Label(self.navbar, text="著名: Excel 合并工具", font=("Arial", 12), fg="green")
        # self.famous_label.pack(side="left", padx=20)

        self.files = []
        self.merged_data = pd.DataFrame()
        self.column_to_merge = None
        self.date_column = None
        self.merged_counts = pd.DataFrame()  # 记录统计结果

        tk.Button(self.root, text="选择 Excel 文件", command=self.select_files).pack(pady=10)
        tk.Label(self.root, text="请输入需要统计的列（如: 报警日志,代码丨英文,隔开）：").pack()
        self.column_entry = tk.Entry(self.root)
        self.column_entry.pack(pady=5)

        tk.Label(self.root, text="（可选）请输入日期列：").pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(pady=5)

        self.merge_button = tk.Button(self.root, text="合并文件", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.pack(pady=10)

        self.export_button = tk.Button(self.root, text="导出合并文件", command=self.export_file, state=tk.DISABLED)
        self.export_button.pack(pady=10)

        self.result_text = tk.Text(self.root, height=15, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("Excel Files", "*.xls;*.xlsx;*.xlsm")])
        if self.files:
            messagebox.showinfo("文件选择", f"已选择 {len(self.files)} 个文件")
            self.merge_button.config(state=tk.NORMAL)

    def merge_files(self):
        self.merged_data = pd.DataFrame()
        column_input = self.column_entry.get().strip()  # 获取用户输入
        self.date_column = self.date_entry.get().strip()

        if not column_input:
            messagebox.showerror("错误", "请输入需要统计的列（如: 报警日志）！")
            return

        # **支持多列输入**
        columns_to_merge = [col.strip() for col in column_input.split(",")]  # 处理多个列

        all_data = []  # 存放所有表格数据

        for file in self.files:
            try:
                data = pd.read_excel(file, engine='openpyxl', sheet_name=None)  # 读取所有工作表
                for sheet_name, sheet_data in data.items():
                    # **检查所有列是否存在**
                    if not set(columns_to_merge).issubset(set(sheet_data.columns)):
                        raise ValueError(f"文件 {file} 的工作表 '{sheet_name}' 缺少 {columns_to_merge} 列！")

                    # **处理日期列**
                    if self.date_column and self.date_column in sheet_data.columns:
                        sheet_data[self.date_column] = pd.to_datetime(sheet_data[self.date_column], errors='coerce').dt.date
                        filtered_data = sheet_data[columns_to_merge + [self.date_column]]  # 选取多个列+日期列
                    else:
                        filtered_data = sheet_data[columns_to_merge]  # 只选取用户输入的列

                    all_data.append(filtered_data)

            except Exception as e:
                messagebox.showerror("错误", f"处理文件 {file} 时出错: {e}")

        if all_data:
            self.merged_data = pd.concat(all_data, ignore_index=True)

        self.calculate_statistics()
        self.export_button.config(state=tk.NORMAL)


    def calculate_statistics(self):
        """统计重复项，并在 GUI 界面显示"""
        self.result_text.delete(1.0, tk.END)

        if self.merged_data.empty:
            messagebox.showerror("错误", "没有数据可统计！")
            return

        # 解析多列
        columns_to_merge = [col.strip() for col in self.column_entry.get().strip().split(",") if col.strip()]
        
        if not columns_to_merge:
            messagebox.showerror("错误", "请输入需要统计的列！")
            return

        # **处理日期列**
        if self.date_column and self.date_column in self.merged_data.columns:
            try:
                count_data = self.merged_data.groupby(columns_to_merge + [self.date_column]).size().reset_index(name="当天次数")
                total_count_data = self.merged_data.groupby(columns_to_merge).size().reset_index(name="总次数")
                self.merged_counts = pd.merge(count_data, total_count_data, on=columns_to_merge, how="left")
            except Exception as e:
                messagebox.showerror("错误", f"统计数据时出错: {e}")
                return
        else:
            try:
                self.merged_counts = self.merged_data.groupby(columns_to_merge).size().reset_index(name="总次数")
            except Exception as e:
                messagebox.showerror("错误", f"统计数据时出错: {e}")
                return

        # **显示统计结果**
        self.result_text.insert(tk.END, "重复统计结果：\n")
        for _, row in self.merged_counts.iterrows():
            result_str = ''
            for col in columns_to_merge:
                result_str += f"{col}: {row[col]}   "
            if "当天次数" in row:
                result_str += f"当天次数: {row['当天次数']}  "
            result_str += f"总次数: {row['总次数']}\n"
            
            self.result_text.insert(tk.END, result_str)


    def export_file(self):
        if self.merged_counts.empty:
            messagebox.showerror("错误", "没有统计的数据，无法导出。")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if save_path:
            try:
                self.merged_counts.to_excel(save_path, index=False)
                messagebox.showinfo("导出成功", f"合并文件已导出到: {save_path}")
            except PermissionError:
                messagebox.showerror("错误", "文件可能已打开或无写入权限，请关闭文件或选择其他路径。")


root = tk.Tk()
app = ExcelMergerApp(root)
root.mainloop()
