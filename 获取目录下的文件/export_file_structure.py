import os

def get_sorted_files_and_dirs(path='.'):
    files_and_dirs = []
    
    for root, dirs, files in os.walk(path):
        relative_path = os.path.relpath(root, path)
        if relative_path == '.':
            relative_path = ''
        
        for dir_name in sorted(dirs):
            files_and_dirs.append((os.path.join(relative_path, dir_name), True))
        
        for file_name in sorted(files):
            files_and_dirs.append((os.path.join(relative_path, file_name), False))
    
    return files_and_dirs

def build_tree(files_and_dirs):
    tree_structure = {}
    
    for item, is_dir in files_and_dirs:
        parts = item.split(os.sep)
        current_level = tree_structure
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        # Add the last part (file or directory)
        current_level[parts[-1]] = None if not is_dir else {}
    
    return tree_structure

def format_tree(tree, prefix=''):
    formatted_lines = []
    for key, value in tree.items():
        formatted_lines.append(f"{prefix}├─ {key}")
        if isinstance(value, dict):
            formatted_lines.extend(format_tree(value, prefix + '│  '))
    return formatted_lines

def write_to_file(file_path, formatted_lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in formatted_lines:
            file.write(f"{line}\n")

if __name__ == "__main__":
    sorted_files_and_dirs = get_sorted_files_and_dirs()
    tree_structure = build_tree(sorted_files_and_dirs)
    formatted_lines = format_tree(tree_structure)
    if formatted_lines:
        formatted_lines[0] = f".\n{formatted_lines[0]}"
    write_to_file('文件结构.txt', formatted_lines)
    print("文件结构已输出到 '文件结构.txt'")
