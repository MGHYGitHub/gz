import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class ExcelMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel 合并工具")
        self.root.geometry("500x500")

        self.files = []
        self.data = {}
        self.merged_data = pd.DataFrame()

        tk.Button(self.root, text="选择 Excel 文件", command=self.select_files).pack(pady=10)
        tk.Label(self.root, text="请输入需要保留的标题行数：").pack()
        self.header_rows_entry = tk.Entry(self.root)
        self.header_rows_entry.pack(pady=5)
        tk.Label(self.root, text="请输入需要跳过的开始行数：").pack()
        self.skip_rows_entry = tk.Entry(self.root)
        self.skip_rows_entry.pack(pady=5)
        tk.Label(self.root, text="请输入需要跳过的结束行数：").pack()
        self.skip_footer_entry = tk.Entry(self.root)
        self.skip_footer_entry.pack(pady=5)
        self.deduplicate_var = tk.IntVar()
        # 更新为输入日期列的索引
        tk.Label(self.root, text="请输入日期列的索引（从0开始）：").pack()
        self.date_col_index_entry = tk.Entry(self.root)
        self.date_col_index_entry.pack(pady=5)
        tk.Checkbutton(self.root, text="去重并统计频次", variable=self.deduplicate_var).pack(pady=10)

        self.merge_button = tk.Button(self.root, text="合并文件", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.pack(pady=10)

        self.export_button = tk.Button(self.root, text="导出合并文件", command=self.export_file, state=tk.DISABLED)
        self.export_button.pack(pady=10)

        self.result_text = tk.Text(self.root, height=15, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("Excel/CSV Files", "*.xls;*.xlsx;*.xlsm;*.csv")])
        if self.files:
            messagebox.showinfo("文件选择", f"已选择 {len(self.files)} 个文件")
            self.merge_button.config(state=tk.NORMAL)

    def read_file(self, file):
        try:
            header_rows = [int(i) for i in self.header_rows_entry.get().strip().split(',')] if self.header_rows_entry.get().strip() else [0]
            skip_rows = [int(i) for i in self.skip_rows_entry.get().strip().split(',')] if self.skip_rows_entry.get().strip() else []
            skip_footer = int(self.skip_footer_entry.get().strip()) if self.skip_footer_entry.get().strip() else 0

            ext = os.path.splitext(file)[1].lower()
            if ext == '.csv':
                for encoding in ['utf-8', 'latin1', 'gb18030', 'gbk', 'gb2312']:
                    try:
                        df = pd.read_csv(file, encoding=encoding, engine='python', skiprows=skip_rows, skipfooter=skip_footer, on_bad_lines='skip')
                        return df
                    except UnicodeDecodeError:
                        continue
                raise ValueError("无法读取CSV文件，可能是未知的编码")
            elif ext in ['.xls', '.xlsx', '.xlsm']:
                df = pd.read_excel(file, engine='openpyxl', sheet_name=None, skiprows=skip_rows, skipfooter=skip_footer)
                return df
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
        except Exception as e:
            raise Exception(f"无法读取文件 {file}: {e}")



    def merge_files(self):
        self.merged_data = pd.DataFrame()

        all_data = []

        for file in self.files:
            try:
                data = self.read_file(file)
                if isinstance(data, dict):
                    for sheet_name, sheet_data in data.items():
                        all_data.append(sheet_data)
                else:
                    all_data.append(data)

            except Exception as e:
                messagebox.showerror("错误", f"处理文件 {file} 时出错: {e}")

        if all_data:
            self.merged_data = pd.concat(all_data, ignore_index=True)

        if self.deduplicate_var.get() == 1:
            date_col_index = self.date_col_index_entry.get().strip()
            if date_col_index:
                try:
                    date_col_index = int(date_col_index)
                    # 将指定索引的列转换为日期格式
                    self.merged_data.iloc[:, date_col_index] = pd.to_datetime(self.merged_data.iloc[:, date_col_index])
                    # 根据log列和日期列进行分组，然后计算每组的大小
                    grouped_data = self.merged_data.groupby([self.merged_data.columns[0], self.merged_data.columns[date_col_index]]).size().reset_index(name='每日频次')
                    # 同时，计算总次数
                    total_counts = self.merged_data.iloc[:, 0].value_counts().reset_index()
                    total_counts.columns = [self.merged_data.columns[0], '总频次']
                    # 合并每日频次和总频次的结果
                    self.merged_data = pd.merge(grouped_data, total_counts, on=self.merged_data.columns[0], how='left')
                except Exception as e:
                    messagebox.showerror("错误", f"处理日期列时出错: {e}")
            else:
                self.merged_data = self.merged_data.value_counts().reset_index()
                self.merged_data.columns = list(self.merged_data.columns[:-1]) + ["总频次"]

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, self.merged_data.to_string())
        self.export_button.config(state=tk.NORMAL)



    def export_file(self):
        if self.merged_data.empty:
            messagebox.showerror("错误", "没有统计的数据，无法导出。")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if save_path:
            try:
                self.merged_data.to_excel(save_path, index=False)
                messagebox.showinfo("导出成功", f"合并文件已导出到: {save_path}")
            except PermissionError:
                messagebox.showerror("错误", "文件可能已打开或无写入权限，请关闭文件或选择其他路径。")

root = tk.Tk()
app = ExcelMergerApp(root)
root.mainloop()
