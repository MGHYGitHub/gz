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
