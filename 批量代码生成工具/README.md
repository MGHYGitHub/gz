## 批量代码生成工具

### 工具介绍

批量代码生成工具用于生成包含图片路径和类别信息的代码片段，并将这些代码片段保存到指定的文本文件中。用户可以自定义起始编号、结束编号、类别、前缀以及文件扩展名。

### 使用方法

1. 将以下Python脚本保存为`generate_code.py`：

    ```python
    # 批量代码生成工具
    # generate_code.py

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

    if __name__ == "__main__":
        start_num = int(input("请输入起始编号: "))
        end_num = int(input("请输入结束编号: "))
        category = input("请输入类别 (默认为 'fun'): ") or 'fun'
        prefix = input("请输入前缀 (默认为 'images/fun/'): ") or 'images/fun/'
        ext = input("请输入文件扩展名 (默认为 '.jpg'): ") or '.jpg'
        filename = input("请输入输出文件名 (默认为 'output.txt'): ") or 'output.txt'
        
        snippets = generate_code_snippets(start_num, end_num, category, prefix, ext)
        save_to_file(snippets, filename)
        print(f"代码片段已保存到 {filename}")
    ```

2. 在终端运行该脚本：

    ```bash
    python generate_code.py
    ```

3. 根据提示输入相应的参数，脚本会生成代码片段并保存到指定的文本文件中。

### 示例

假设你输入了以下参数：
- 起始编号：1
- 结束编号：5
- 类别：fun
- 前缀：images/fun/
- 文件扩展名：.jpg
- 输出文件名：output.txt

脚本会生成以下代码片段并保存到`output.txt`文件中：

```plaintext
{src: 'images/fun/1.jpg', category: 'fun'},
{src: 'images/fun/2.jpg', category: 'fun'},
{src: 'images/fun/3.jpg', category: 'fun'},
{src: 'images/fun/4.jpg', category: 'fun'},
{src: 'images/fun/5.jpg', category: 'fun'},
```