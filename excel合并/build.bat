@echo off
rem 设置编码为 UTF-8，确保支持中文显示
chcp 65001 > nul

rem 清理之前的临时文件和目录
echo 删除构建过程中创建的临时文件和目录...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

rem 开始编译生成代码工具
echo 编译 excel.py...
pyinstaller --onefile --windowed --hidden-import=pandas --hidden-import=openpyxl excel.py

rem 检查编译是否成功
if errorlevel 1 (
    echo 编译失败，终止脚本执行.
    pause
    exit /b
)

rem 进入 dist 目录并修改 exe 文件名
echo 将生成的 exe 文件重命名为 Excel合并工具.exe...
cd dist
if exist "excel.exe" (
    ren "excel.exe" "Excel合并工具.exe"
) else (
    echo 未找到 excel.exe，无法重命名.
    pause
    exit /b
)

echo 编译成功！可执行文件位于 dist 目录中.
pause
