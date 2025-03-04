@echo off

:: ��鵱ǰ�û��Ƿ���й���ԱȨ��
net session >nul 2>nul
if %errorlevel% NEQ 0 (
    echo ��ǰû�й���ԱȨ�ޣ������Թ���ԱȨ������...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

setlocal

:: ����Դ�ļ��к�Ŀ���ļ���·����·���������ģ�
set "SOURCE_DIR=C:\Users\29706\Desktop\������Ŀ\copy\test1"
set "DEST_DIR=C:\Users\29706\Desktop\������Ŀ\copy\test2"

:: ���ø���ģʽ
:: 1: �ֶ�ģʽ - �û��ֶ�ִ�нű������ļ�����
:: 2: ��������ģʽ - ����Դ�ļ����е������ļ���Ŀ���ļ���
:: 3: ����5���ļ�����ģʽ - ֻ����Ŀ���ļ����е�����10���ļ�
set MODE=2

:: ���ö�ʱģʽ
:: 1: �ֶ�ģʽ - ��������ʱ����
:: 2: ָ��ʱ��ģʽ - ÿ����ָ��ʱ��ִ��
:: 3: ���ģʽ - ÿ��һ��ʱ��ִ��
set TIMED_MODE=2

:: ��ʱ����ָ��ʱ��ִ��
set SPECIFIC_TIME=19:00

:: ��ʱ����ÿ������Сʱִ��
set INTERVAL_HOURS=0

:: ��ʱ����ÿ�����ٷ���ִ��
set INTERVAL_MINUTES=1

:: �����ܿ��أ�1: ��������0: ��������
set CLEANUP_ENABLED=0

:: ����ִ��һ�θ��Ʋ���
call :run_copy

:: ѡ��ʱģʽ
if %TIMED_MODE%==2 (
    echo [��ʱģʽ] ������ %SPECIFIC_TIME% ִ��...
    call :schedule_specific_time
) else if %TIMED_MODE%==3 (
    echo [���ģʽ] ����ÿ�� %INTERVAL_MINUTES% ����ִ��...
    call :schedule_interval
) else (
    echo [�ֶ�ģʽ] ��������ɣ�δ������ʱ����
    call :countdown_exit
    exit /b
)

call :countdown_exit
exit /b

:: ִ�и��Ʋ���
:run_copy
if not exist "%SOURCE_DIR%" (
    echo [����] Դ�ļ��в�����: "%SOURCE_DIR%"
    pause
    exit /b
)

if not exist "%DEST_DIR%" (
    echo [��ʾ] Ŀ���ļ��в����ڣ����ڴ���: "%DEST_DIR%"
    mkdir "%DEST_DIR%"
)

echo [��ʼ����]...
:: ���ݸ���ģʽѡ���Ʒ�ʽ
if %MODE%==1 (
    echo [�ֶ�ģʽ] �û��ֶ�ִ�и��ơ�
    :: �ֶ�ģʽ�£��û���Ҫ�ֶ�ִ�в���
    exit /b
) else if %MODE%==2 (
    echo [��������ģʽ] ���������ļ���Ŀ���ļ��С�
    :: ʹ�� /COPY:DAT ѡ���Ա���Ȩ������
    robocopy "%SOURCE_DIR%" "%DEST_DIR%" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL
) else if %MODE%==3 (
    echo [����5���ļ�����ģʽ] ֻ�������µ�5���ļ���Ŀ���ļ��С�
    for /f "delims=" %%F in ('dir /b /o-d "%SOURCE_DIR%\*"') do (
        echo [����] �����ļ�: %%F
        copy "%SOURCE_DIR%\%%F" "%DEST_DIR%"
        set /a file_count+=1
        if !file_count! GEQ 5 (
            echo [��ʾ] �Ѹ���5���ļ���ֹͣ���ơ�
            exit /b
        )
    )
)

echo [���] �ļ��ѳɹ����Ƶ�: "%DEST_DIR%"��

:: ���ݿ��ؾ����Ƿ���������ļ�
if %CLEANUP_ENABLED%==1 (
    call :cleanup_old_files
) else (
    echo [��ʾ] �������ѽ��ã��������ֶ�ɾ���ļ���
)

exit /b

:: ��������ļ����������µ�10��
:cleanup_old_files
setlocal enabledelayedexpansion

set "file_count=0"
for /f "delims=" %%F in ('dir /b /o-d "%DEST_DIR%\*"') do (
    set /a file_count+=1
    if !file_count! GTR 10 (
        echo [ɾ��] ɾ���ļ�: %%F
        del "%DEST_DIR%\%%F"
    )
)

echo [�������] Ŀ���ļ�������ౣ��5�������ļ���
endlocal
exit /b

:: ��������ÿ��һ��ʱ��ִ��
:schedule_interval
echo [��̨] ����ƻ���
:: ɾ�����е�����
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: У��ʱ��������
if %INTERVAL_MINUTES% GTR 0 (
    echo ����ÿ�� %INTERVAL_MINUTES% ����ִ��...
    :: ȷ�� robocopy �����ʽ��ȷ��ת������
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc minute /mo %INTERVAL_MINUTES% /RL HIGHEST /F
) else if %INTERVAL_HOURS% GTR 0 (
    echo ����ÿ�� %INTERVAL_HOURS% Сʱִ��...
    :: ȷ�� robocopy �����ʽ��ȷ��ת������
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc hourly /mo %INTERVAL_HOURS% /RL HIGHEST /F
) else (
    echo [����] û��������Ч��ʱ���������� INTERVAL_HOURS �� INTERVAL_MINUTES ������
)
exit /b

:: ��������ÿ����ָ��ʱ��ִ��
:schedule_specific_time
echo [��̨] ����ƻ���ÿ�� %SPECIFIC_TIME% ִ��...
:: ɾ�����е�����
schtasks /delete /tn "CopyTask" /f >nul 2>&1
:: ȷ�� robocopy �����ʽ��ȷ��ת������
schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPY:DAT /R:0 /W:0 /NFL /NDL && cmd /c call \"%~f0\" :cleanup_old_files" /sc daily /st %SPECIFIC_TIME% /RL HIGHEST /F
echo [��ʾ] ��ʱ�����Ѵ���������ÿ�� %SPECIFIC_TIME% ִ�С�
exit /b

:: 5����Զ��رմ���
:countdown_exit
echo.
echo [���ڹر�] ���Ժ�...
timeout /t 5 >nul
exit /b
