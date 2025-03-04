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
set "SOURCE_DIR=C:\Users\29706\Desktop\个人项目\copy\test1"
set "DEST_DIR=C:\Users\29706\Desktop\个人项目\copy\test2"

:: 设置复制模式
:: 1: 手动模式 - 用户手动执行脚本进行文件复制
:: 2: 完整复制模式 - 复制源文件夹中的所有文件到目标文件夹
:: 3: 最新5个文件复制模式 - 只复制目标文件夹中的最新10个文件
set MODE=2

:: 设置定时模式
:: 1: 手动模式 - 不创建定时任务
:: 2: 指定时间模式 - 每天在指定时间执行
:: 3: 间隔模式 - 每隔一定时间执行
set TIMED_MODE=2

:: 定时任务：指定时间执行
set SPECIFIC_TIME=19:00

:: 定时任务：每隔多少小时执行
set INTERVAL_HOURS=0

:: 定时任务：每隔多少分钟执行
set INTERVAL_MINUTES=1

:: 清理功能开关（1: 启用清理，0: 禁用清理）
set CLEANUP_ENABLED=0

:: 立即执行一次复制操作
call :run_copy

:: 选择定时模式
if %TIMED_MODE%==2 (
    echo [定时模式] 任务将于 %SPECIFIC_TIME% 执行...
    call :schedule_specific_time
) else if %TIMED_MODE%==3 (
    echo [间隔模式] 任务将每隔 %INTERVAL_MINUTES% 分钟执行...
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
:: 根据复制模式选择复制方式
if %MODE%==1 (
    echo [手动模式] 用户手动执行复制。
    :: 手动模式下，用户需要手动执行操作
    exit /b
) else if %MODE%==2 (
    echo [完整复制模式] 复制所有文件到目标文件夹。
    :: 使用 /COPY:DAT 选项以避免权限问题
    robocopy "%SOURCE_DIR%" "%DEST_DIR%" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL
) else if %MODE%==3 (
    echo [最新5个文件复制模式] 只复制最新的5个文件到目标文件夹。
    for /f "delims=" %%F in ('dir /b /o-d "%SOURCE_DIR%\*"') do (
        echo [复制] 复制文件: %%F
        copy "%SOURCE_DIR%\%%F" "%DEST_DIR%"
        set /a file_count+=1
        if !file_count! GEQ 5 (
            echo [提示] 已复制5个文件，停止复制。
            exit /b
        )
    )
)

echo [完成] 文件已成功复制到: "%DEST_DIR%"！

:: 根据开关决定是否清理多余文件
if %CLEANUP_ENABLED%==1 (
    call :cleanup_old_files
) else (
    echo [提示] 清理功能已禁用，您可以手动删除文件。
)

exit /b

:: 清理多余文件，保留最新的10份
:cleanup_old_files
setlocal enabledelayedexpansion

set "file_count=0"
for /f "delims=" %%F in ('dir /b /o-d "%DEST_DIR%\*"') do (
    set /a file_count+=1
    if !file_count! GTR 10 (
        echo [删除] 删除文件: %%F
        del "%DEST_DIR%\%%F"
    )
)

echo [清理完成] 目标文件夹中最多保留5个最新文件。
endlocal
exit /b

:: 设置任务每隔一定时间执行
:schedule_interval
echo [后台] 任务计划：
:: 删除已有的任务
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: 校验时间间隔设置
if %INTERVAL_MINUTES% GTR 0 (
    echo 任务将每隔 %INTERVAL_MINUTES% 分钟执行...
    :: 确保 robocopy 命令格式正确，转义引号
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc minute /mo %INTERVAL_MINUTES% /RL HIGHEST /F
) else if %INTERVAL_HOURS% GTR 0 (
    echo 任务将每隔 %INTERVAL_HOURS% 小时执行...
    :: 确保 robocopy 命令格式正确，转义引号
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc hourly /mo %INTERVAL_HOURS% /RL HIGHEST /F
) else (
    echo [错误] 没有设置有效的时间间隔！请检查 INTERVAL_HOURS 和 INTERVAL_MINUTES 变量。
)
exit /b

:: 设置任务每天在指定时间执行
:schedule_specific_time
echo [后台] 任务计划：每天 %SPECIFIC_TIME% 执行...
:: 删除已有的任务
schtasks /delete /tn "CopyTask" /f >nul 2>&1
:: 确保 robocopy 命令格式正确，转义引号
schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc daily /st %SPECIFIC_TIME% /RL HIGHEST /F
echo [提示] 定时任务已创建，将于每天 %SPECIFIC_TIME% 执行。
exit /b

:: 5秒后自动关闭窗口
:countdown_exit
echo.
echo [窗口关闭] 请稍候...
timeout /t 5 >nul
exit /b
