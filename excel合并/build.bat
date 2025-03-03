@echo off
rem 设置编码为 UTF-8，确保支持中文显示
chcp 65001 > nul

rem 清理之前的临时文件和目录
echo 删除构建过程中创建的临时文件和目录...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q _internal

rem 开始编译生成代码工具
echo 编译 excel.py...
pyinstaller --onefile --windowed --hidden-import=pandas --hidden-import=openpyxl excel.py

rem 进入 dist 目录并修改 exe 文件名
echo 将生成的 exe 文件重命名为 Excel合并工具.exe...
cd dist
ren excel.exe "Excel合并工具.exe"

echo 编译成功！可执行文件位于 dist 目录中.
pause
