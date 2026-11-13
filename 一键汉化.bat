@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "SRC=%~1"
if "%SRC%"=="" (
  echo 请把 BDS Addon Manager.exe 拖到本窗口，或直接输入它的完整路径，然后回车：
  set /p SRC=
)

if "%SRC%"=="" (
  echo 没有提供文件，已退出。
  pause
  exit /b 1
)

echo.
echo 正在汉化：%SRC%
echo.
python "%~dp0src\patch.py" "%SRC%"
if errorlevel 1 (
  echo.
  echo 汉化失败，请检查上面提示的信息。
  pause
  exit /b 1
)

echo.
echo 完成。汉化版已生成在同一个目录下。
pause
