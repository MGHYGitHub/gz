import os
import subprocess
from datetime import datetime, timedelta
import re
import tkinter as tk
from tkinter import messagebox

# 获取 git 日志
def get_git_log():
    result = subprocess.run(['git', 'log', '--pretty=format:%h %ad %s', '--date=short'], stdout=subprocess.PIPE)
    log = result.stdout.decode('utf-8')
    return log

# 解析 git 日志
def parse_git_log(log):
    entries = log.split('\n')
    log_dict = {}
    for entry in entries:
        match = re.match(r'(\w+)\s(\d{4}-\d{2}-\d{2})\s(.+)', entry)
        if match:
            commit_hash, date, message = match.groups()
            if date not in log_dict:
                log_dict[date] = []
            log_dict[date].append(f'- {commit_hash} - {message}')
    return log_dict

# 生成时间轴
def generate_timeline(log_dict, start_date, end_date, existing_manual_entries):
    current_date = end_date
    timeline = "## **时间轴**\n\n"

    while current_date >= start_date:
        date_str = current_date.strftime('%Y-%m-%d')
        entries = log_dict.get(date_str, [])
        manual_entries = existing_manual_entries.get(date_str, [])

        # 合并自动生成的条目和手动添加的条目，避免重复
        combined_entries = manual_entries[:]
        for entry in entries:
            if entry not in combined_entries:
                combined_entries.append(entry)

        if combined_entries:
            timeline += f"::: timeline {date_str}\n"
            for entry in combined_entries:
                timeline += f"{entry}\n"
            timeline += ":::\n\n"

        current_date -= timedelta(days=1)

    return timeline

# 读取现有的 Time.md 文件
def read_existing_timeline(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 提取手动添加的时间轴条目
def extract_manual_entries(existing_timeline):
    manual_entries = {}
    blocks = existing_timeline.split("\n\n")
    for block in blocks:
        if "📝" in block:
            match = re.search(r'::: timeline (\d{4}-\d{2}-\d{2})', block)
            if match:
                date_str = match.group(1)
                if date_str not in manual_entries:
                    manual_entries[date_str] = []
                manual_entries[date_str].extend([line for line in block.split('\n') if '📝' in line])
    return manual_entries

# 写入 Time.md 文件
def write_timeline(file_path, timeline):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(timeline)

# 主函数
def main():
    log = get_git_log()
    log_dict = parse_git_log(log)

    # 获取最早和最晚的日期
    dates = list(log_dict.keys())
    if not dates:
        messagebox.showinfo("信息", "未找到 Git 历史记录。")
        return

    start_date = datetime.strptime(min(dates), '%Y-%m-%d')
    end_date = datetime.strptime(max(dates), '%Y-%m-%d')

    # 读取现有的 Time.md 文件
    existing_timeline = read_existing_timeline('Time.md')
    
    # 提取手动添加的时间轴条目
    manual_entries = extract_manual_entries(existing_timeline)

    # 生成新的时间轴
    new_timeline = generate_timeline(log_dict, start_date, end_date, manual_entries)

    if existing_timeline.strip() != new_timeline.strip():
        write_timeline('Time.md', new_timeline)
        messagebox.showinfo("信息", "Time.md 已更新。")
    else:
        messagebox.showinfo("信息", "Git 历史记录没有变化。")

# 创建 GUI
def create_gui():
    root = tk.Tk()
    root.title("Git 时间轴生成器")

    label = tk.Label(root, text="点击按钮生成或更新 Time.md 文件")
    label.pack(pady=10)

    generate_button = tk.Button(root, text="生成时间轴", command=main)
    generate_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
