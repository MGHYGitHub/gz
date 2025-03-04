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
set "SOURCE_DIR=C:\Users\29706\Desktop\������Ŀ\test\test1"
set "DEST_DIR=C:\Users\29706\Desktop\������Ŀ\test\test2"

:: ���ø���ģʽ
set MODE=2

:: ���ö�ʱģʽ
set TIMED_MODE=3

:: ��ʱ����ָ��ʱ��ִ��
set SPECIFIC_TIME=14:00

:: ��ʱ����ÿ������Сʱִ��
set INTERVAL_HOURS=0

:: ��ʱ����ÿ�����ٷ���ִ��
set INTERVAL_MINUTES=1

:: ����ִ��һ�θ��Ʋ���
call :run_copy

:: ѡ��ʱģʽ
if %TIMED_MODE%==2 (
    echo [��ʱģʽ] ������ %SPECIFIC_TIME% ִ��...
    call :schedule_specific_time
) else if %TIMED_MODE%==3 (
    echo [���ģʽ] �������趨...
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
:: ע������ʹ��˫���Ű���·��
robocopy "%SOURCE_DIR%" "%DEST_DIR%" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL
if %errorlevel% GEQ 1 (
    echo [����] robocopy ִ��ʱ�������󣬴������: %errorlevel%�����ļ��ѳɹ����ƣ�
)
echo [���] �ļ��ѳɹ����ƣ�
exit /b

:: ��������ÿ��һ��ʱ��ִ��
:schedule_interval
echo [��̨] ����ƻ���
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: У��ʱ��������
if %INTERVAL_MINUTES% GTR 0 (
    echo ����ÿ�� %INTERVAL_MINUTES% ����ִ��...
    :: ȷ�� robocopy �����ʽ��ȷ��ת������
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc minute /mo %INTERVAL_MINUTES% /RL HIGHEST /F
) else if %INTERVAL_HOURS% GTR 0 (
    echo ����ÿ�� %INTERVAL_HOURS% Сʱִ��...
    :: ȷ�� robocopy �����ʽ��ȷ��ת������
    schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc hourly /mo %INTERVAL_HOURS% /RL HIGHEST /F
) else (
    echo [����] û��������Ч��ʱ���������� INTERVAL_HOURS �� INTERVAL_MINUTES ������
)
exit /b

:: ��������ÿ����ָ��ʱ��ִ��
:schedule_specific_time
echo [��̨] ����ƻ���ÿ�� %SPECIFIC_TIME% ִ��...
schtasks /delete /tn "CopyTask" /f >nul 2>&1
:: ȷ�� robocopy �����ʽ��ȷ��ת������
schtasks /create /tn "CopyTask" /tr "cmd /c robocopy \"%SOURCE_DIR%\" \"%DEST_DIR%\" /E /Z /COPYALL /R:0 /W:0 /NFL /NDL" /sc daily /st %SPECIFIC_TIME% /RL HIGHEST /F
exit /b

:: 5����Զ��رմ���
:countdown_exit
echo.
echo [���ڹر�] ���Ժ�...
timeout /t 5 >nul
exit /b
