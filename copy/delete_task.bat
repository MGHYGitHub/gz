@echo off

:: ��鵱ǰ�û��Ƿ���й���ԱȨ��
net session >nul 2>nul
if %errorlevel% NEQ 0 (
    echo ��ǰû�й���ԱȨ�ޣ������Թ���ԱȨ������...
    powershell -Command "Start-Process cmd -ArgumentList '/c', '%~s0' -Verb runAs"
    exit /b
)

setlocal

:: ɾ������ƻ�
echo [ɾ������ƻ�] ����ɾ����ʱ���� "CopyTask"...
schtasks /delete /tn "CopyTask" /f >nul 2>&1

:: ɾ�������ļ�
:: echo [ɾ�������ļ�] ����ɾ�������ļ�...
:: del "%~dp0copy_script.bat" >nul 2>&1
:: echo [ɾ�������ļ�] �����ļ���ɾ����������ڣ���

echo [���] ��ʱ����͸����ļ��ѳɹ�ɾ����
exit /b
