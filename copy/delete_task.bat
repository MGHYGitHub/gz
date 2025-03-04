@echo off

:: 检查当前用户是否具有管理员权限
net session >nul 2>nul
if %errorlevel% NEQ 0 (
    echo 当前没有管理员权限，正在以管理员权限重启...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

setlocal

:: 删除任务计划
echo [删除任务计划] 正在删除定时任务 "CopyTask"...
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: 删除附属文件
:: echo [删除附属文件] 正在删除附属文件...
:: del "%~dp0copy_script.bat" >nul 2>&1
:: echo [删除附属文件] 附属文件已删除（如果存在）。

echo [完成] 定时任务和附属文件已成功删除！
exit /b
