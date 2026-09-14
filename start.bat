@echo off
REM Windows 11 視窗鎖定器 - 快速啟動腳本

echo ====================================
echo Windows 11 Window Locker
echo ====================================
echo.

REM 檢查 Python 是否已安裝
python --version >nul 2>&1
if errorlevel 1 (
    echo 錯誤：找不到 Python
    echo 請先安裝 Python 3.8 或更高版本
    echo 訪問: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在檢查依賴...
python -m pip list | find "pywin32" >nul
if errorlevel 1 (
    echo.
    echo 正在安裝依賴（pywin32）...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 安裝失敗，請檢查您的網絡連接
        pause
        exit /b 1
    )
    echo 依賴安裝完成！
    echo.
)

echo 正在啟動應用...
echo.

python gui.py

if errorlevel 1 (
    echo.
    echo 應用啟動失敗！
    echo 請嘗試以管理員身份運行此腳本
    pause
    exit /b 1
)

exit /b 0
