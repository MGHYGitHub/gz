@echo off
rem 设置编码为 UTF-8，确保支持中文显示
chcp 65001 > nul

rem 清理之前的临时文件和目录
echo 删除构建过程中创建的临时文件和目录...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q _internal

rem 开始编译生成代码工具
echo 编译 rename_files_gui.py...
pyinstaller --onefile --windowed --hidden-import=Crypto --hidden-import=Crypto.Cipher --hidden-import=Crypto.Util.Padding encrypt_html.py

rem 进入dist目录并修改exe文件名
echo 将生成的exe文件重命名为 批量代码生成工具.exe...
cd dist
ren rename_files_gui.exe "批量改名工具.exe"

echo 编译成功！可执行文件位于dist目录中.
pause
