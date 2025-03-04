@echo off

:: 检查当前用户是否具有管理员权限
net session >nul 2>nul
if %errorlevel% NEQ 0 (
    echo 当前没有管理员权限，正在以管理员权限重启...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

setlocal

:: 设置源文件夹和目标文件夹路径（路径包含中文）
set "SOURCE_DIR=C:\Users\29706\Desktop\个人项目\test\test1"
set "DEST_DIR=C:\Users\29706\Desktop\个人项目\test\test2"

:: 设置复制模式
set MODE=2

:: 设置定时模式
set TIMED_MODE=3

:: 定时任务：指定时间执行
set SPECIFIC_TIME=14:00

:: 定时任务：每隔多少小时执行
set INTERVAL_HOURS=0

:: 定时任务：每隔多少分钟执行
set INTERVAL_MINUTES=1

:: 立即执行一次复制操作
call :run_copy

:: 选择定时模式
if %TIMED_MODE%==2 (
    echo [定时模式] 任务将于 %SPECIFIC_TIME% 执行...
    call :schedule_specific_time
) else if %TIMED_MODE%==3 (
    echo [间隔模式] 任务已设定...
    call :schedule_interval
) else (
    echo [手动模式] 复制已完成，未创建定时任务。
    call :countdown_exit
    exit /b
)

call :countdown_exit
exit /b

:: 执行复制操作
:run_copy
if not exist "%SOURCE_DIR%" (
    echo [错误] 源文件夹不存在: "%SOURCE_DIR%"
    pause
    exit /b
)

if not exist "%DEST_DIR%" (
    echo [提示] 目标文件夹不存在，正在创建: "%DEST_DIR%"
    mkdir "%DEST_DIR%"
)

echo [开始复制]...
:: 注意这里使用双引号包裹路径
robocopy "%SOURCE_DIR%" "%DEST_DIR%" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL
if %errorlevel% GEQ 1 (
    echo [警告] robocopy 执行时遇到错误，错误代码: %errorlevel%（但文件已成功复制）
)
echo [完成] 文件已成功复制！
exit /b

:: 设置任务每隔一定时间执行
:schedule_interval
echo [后台] 任务计划：
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: 校验时间间隔设置
if %INTERVAL_MINUTES% GTR 0 (
    echo 任务将每隔 %INTERVAL_MINUTES% 分钟执行...
    :: 确保 robocopy 命令格式正确，转义引号
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc minute /mo %INTERVAL_MINUTES% /RL HIGHEST /F
) else if %INTERVAL_HOURS% GTR 0 (
    echo 任务将每隔 %INTERVAL_HOURS% 小时执行...
    :: 确保 robocopy 命令格式正确，转义引号
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc hourly /mo %INTERVAL_HOURS% /RL HIGHEST /F
) else (
    echo [错误] 没有设置有效的时间间隔！请检查 INTERVAL_HOURS 和 INTERVAL_MINUTES 变量。
)
exit /b

:: 设置任务每天在指定时间执行
:schedule_specific_time
echo [后台] 任务计划：每天 %SPECIFIC_TIME% 执行...
schtasks /delete /tn "CopyTask" /f >nul 2>&1
:: 确保 robocopy 命令格式正确，转义引号
schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc daily /st %SPECIFIC_TIME% /RL HIGHEST /F
exit /b

:: 5秒后自动关闭窗口
:countdown_exit
echo.
echo [窗口关闭] 请稍候...
timeout /t 5 >nul
exit /b
