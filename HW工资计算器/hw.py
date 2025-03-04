import tkinter as tk
from tkinter import ttk

# 工资计算函数
def calculate_salary():
    try:
        # 获取标准工资
        base_salary = float(base_salary_entry.get())
        
        # 获取加班时数，如果为空则默认设为0
        g1_hours = float(g1_hours_entry.get() or 0)
        g2_hours = float(g2_hours_entry.get() or 0)
        g3_hours = float(g3_hours_entry.get() or 0)
        
        # 定义加班费率
        g1_rate = 39.65517
        g2_rate = 52.87356
        g3_rate = 79.31035
        
        # 计算加班工资
        g1_overtime_pay = g1_rate * g1_hours
        g2_overtime_pay = g2_rate * g2_hours
        g3_overtime_pay = g3_rate * g3_hours
        
        # 更新加班工资显示
        g1_pay_label.config(text=f"{g1_overtime_pay:.2f}")
        g2_pay_label.config(text=f"{g2_overtime_pay:.2f}")
        g3_pay_label.config(text=f"{g3_overtime_pay:.2f}")
        
        # 计算总工资
        total_salary = base_salary + g1_overtime_pay + g2_overtime_pay + g3_overtime_pay
        
        # 更新实时工资显示
        total_salary_label.config(text=f"{total_salary:.2f}")
    
    except ValueError:
        total_salary_label.config(text="输入无效，请检查输入的数值")

# 创建主窗口
root = tk.Tk()
root.title("工资计算器")

# 标准工资标签和输入框
base_salary_label = tk.Label(root, text="标准工资:")
base_salary_label.grid(row=0, column=0, padx=10, pady=10)
base_salary_entry = tk.Entry(root)
base_salary_entry.grid(row=0, column=1, padx=10, pady=10)
base_salary_entry.insert(0, "4600")  # 默认值4600

# 加班工资标题
overtime_label = tk.Label(root, text="加班类别")
overtime_label.grid(row=1, column=0, padx=10, pady=10)
overtime_rate_label = tk.Label(root, text="加班费率")
overtime_rate_label.grid(row=1, column=1, padx=10, pady=10)
overtime_hours_label = tk.Label(root, text="加班时数")
overtime_hours_label.grid(row=1, column=2, padx=10, pady=10)
overtime_pay_label = tk.Label(root, text="加班工资")
overtime_pay_label.grid(row=1, column=3, padx=10, pady=10)

# G1 加班
g1_label = tk.Label(root, text="G1")
g1_label.grid(row=2, column=0, padx=10, pady=10)
g1_rate_label = tk.Label(root, text="1.5倍")
# g1_rate_label = tk.Label(root, text="39.65517")
g1_rate_label.grid(row=2, column=1, padx=10, pady=10)
g1_hours_entry = tk.Entry(root)
g1_hours_entry.grid(row=2, column=2, padx=10, pady=10)
g1_hours_entry.insert(0, "0")  # 默认值0
g1_pay_label = tk.Label(root, text="0.00")
g1_pay_label.grid(row=2, column=3, padx=10, pady=10)

# G2 加班
g2_label = tk.Label(root, text="G2")
g2_label.grid(row=3, column=0, padx=10, pady=10)
g2_rate_label = tk.Label(root, text="2倍")
# g2_rate_label = tk.Label(root, text="52.87356")
g2_rate_label.grid(row=3, column=1, padx=10, pady=10)
g2_hours_entry = tk.Entry(root)
g2_hours_entry.grid(row=3, column=2, padx=10, pady=10)
g2_hours_entry.insert(0, "0")  # 默认值0
g2_pay_label = tk.Label(root, text="0.00")
g2_pay_label.grid(row=3, column=3, padx=10, pady=10)

# G3 加班
g3_label = tk.Label(root, text="G3")
g3_label.grid(row=4, column=0, padx=10, pady=10)
g3_rate_label = tk.Label(root, text="3倍")
# g3_rate_label = tk.Label(root, text="79.31035")
g3_rate_label.grid(row=4, column=1, padx=10, pady=10)
g3_hours_entry = tk.Entry(root)
g3_hours_entry.grid(row=4, column=2, padx=10, pady=10)
g3_hours_entry.insert(0, "0")  # 默认值0
g3_pay_label = tk.Label(root, text="0.00")
g3_pay_label.grid(row=4, column=3, padx=10, pady=10)

# 实时工资标签
total_salary_text_label = tk.Label(root, text="实时工资:")
total_salary_text_label.grid(row=5, column=0, padx=10, pady=10)
total_salary_label = tk.Label(root, text="0.00")
total_salary_label.grid(row=5, column=1, padx=10, pady=10)

# 计算按钮
calculate_button = tk.Button(root, text="开始计算", command=calculate_salary)
calculate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# 添加公告
notice_label = tk.Label(root, text="PS: 派遣工专用\n本程序仅供参考使用\n作者:廖工", font=("Arial", 10), fg="red")
notice_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # 右下角放置公告

# 启动主循环
root.mainloop()
