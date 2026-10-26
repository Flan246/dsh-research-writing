@echo off
REM 注册季度期刊名单核验任务（每年 1/4/7/10 月 1 日 09:00）。
REM 用法：右键“以管理员身份运行”或直接双击（当前用户任务即可）。
if /i "%~1"=="--run" goto run_check

if not exist "D:\cursor_file\dsh-research-writing\logs" mkdir "D:\cursor_file\dsh-research-writing\logs"
schtasks /create /tn "KimiJournalWhitelistCheck" /tr "C:\Windows\System32\cmd.exe /d /c D:\cursor_file\dsh-research-writing\scripts\install-journal-check-task.cmd --run" /sc monthly /m JAN,APR,JUL,OCT /d 1 /st 09:00 /f
if errorlevel 1 exit /b %errorlevel%
schtasks /query /tn "KimiJournalWhitelistCheck"
exit /b %errorlevel%

:run_check
if not exist "D:\cursor_file\dsh-research-writing\logs" mkdir "D:\cursor_file\dsh-research-writing\logs"
set "HTTPS_PROXY=http://127.0.0.1:7897"
set "HTTP_PROXY=http://127.0.0.1:7897"
"C:\Users\范双双\AppData\Local\Programs\Python\Python313\python.exe" "D:\cursor_file\dsh-research-writing\scripts\check-journal-lists.py" >> "D:\cursor_file\dsh-research-writing\logs\journal-check.log" 2>&1
exit /b %errorlevel%
