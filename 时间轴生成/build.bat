@echo off
rem 设置编码为 UTF-8，确保支持中文显示
chcp 65001 > nul

rem 清理之前的临时文件和目录
echo 删除构建过程中创建的临时文件和目录...
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q _internal

rem 开始编译生成代码工具
echo 编译 encrypt_html.py...
pyinstaller --onefile --windowed generate_timeline.py

rem 进入dist目录并修改exe文件名
echo 将生成的exe文件重命名为 🔒网页加密工具.exe...
cd dist
ren generate_timeline.exe "⏰时间轴生成.exe"

echo 编译成功！可执行文件位于dist目录中.
pause
