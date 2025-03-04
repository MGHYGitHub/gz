## 批量改名工具

### 工具介绍

批量改名工具用于批量重命名指定文件夹中的图片文件。用户可以选择编号方式（升序、降序、自定义编号等）、自定义前缀，并可以选择字母大小写混合编号。同时可以排除某个编号范围以避免与已有文件名冲突。

### 使用方法

1. 将以下Python脚本保存为`rename_files.py`：

    ```python
    # 批量改名工具
    # rename_files.py

    import os
    import string

    def get_file_list(folder_path):
        """获取指定文件夹中的所有文件"""
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    def rename_files(folder_path, start_num=1, order='asc', prefix='', mode='numeric', exclude_range=None):
        """重命名文件"""
        files = get_file_list(folder_path)
        
        # 根据顺序排序文件
        files.sort(reverse=(order == 'desc'))
        
        for i, filename in enumerate(files):
            name, ext = os.path.splitext(filename)
            
            # 生成新的编号
            if mode == 'numeric':
                new_num = start_num + i if order == 'asc' else start_num - i
            elif mode == 'alphabet':
                letters = string.ascii_lowercase if order == 'asc' else string.ascii_lowercase[::-1]
                new_num = letters[i % len(letters)]
                if i >= len(letters):
                    new_num += str(i // len(letters))
            elif mode == 'mixed':
                new_num = str(start_num + i) + string.ascii_letters[i % len(string.ascii_letters)]
            else:
                raise ValueError("Unsupported mode. Please use 'numeric', 'alphabet' or 'mixed'.")
            
            # 检查是否在排除范围内
            if exclude_range and mode == 'numeric':
                if new_num in exclude_range:
                    continue
            
            # 生成新的文件名
            new_name = f"{prefix}{new_num}{ext}"
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
            print(f"重命名 {filename} 为 {new_name}")

    if __name__ == "__main__":
        folder_path = input("请输入包含图片的文件夹路径: ")
        start_num = int(input("请输入起始编号 (默认为1): ") or 1)
        order = input("请输入顺序 (升序 'asc' 或 降序 'desc', 默认为升序 'asc'): ") or 'asc'
        prefix = input("请输入前缀 (默认为空): ") or ''
        mode = input("请输入编号模式 (数字 'numeric', 字母 'alphabet', 混合 'mixed'; 默认为数字 'numeric'): ") or 'numeric'
        exclude_range_input = input("请输入排除范围 (例如 '1-3', 留空表示无排除范围): ")
        
        exclude_range = None
        if exclude_range_input:
            try:
                exclude_start, exclude_end = map(int, exclude_range_input.split('-'))
                exclude_range = range(exclude_start, exclude_end + 1)
            except ValueError:
                print("无效的排除范围格式。应为 '开始-结束' 形式。")
                exit(1)
        
        rename_files(folder_path, start_num, order, prefix, mode, exclude_range)
    ```

2. 在终端运行该脚本：

    ```bash
    python rename_files.py
    ```

3. 根据提示输入相应的参数，脚本会按你的要求重命名文件夹中的图片。

### 示例

假设你输入了以下参数：
- 文件夹路径：`./images`
- 起始编号：1
- 排序顺序：asc
- 前缀：img_
- 编号模式：numeric
- 排除范围：1-3

脚本会将`./images`文件夹中的文件按升序重命名为`img_4.jpg`，`img_5.jpg`，`img_6.jpg`等，排除1-3编号。
