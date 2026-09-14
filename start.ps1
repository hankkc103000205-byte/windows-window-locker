# Windows 11 視窗鎖定器 - PowerShell 啟動腳本

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Windows 11 Window Locker" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Python 是否已安裝
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ 找到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 錯誤：找不到 Python" -ForegroundColor Red
    Write-Host "請先安裝 Python 3.8 或更高版本" -ForegroundColor Yellow
    Write-Host "訪問: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

Write-Host ""
Write-Host "正在檢查依賴..." -ForegroundColor Yellow

# 檢查是否已安裝 pywin32
$pipList = python -m pip list
if ($pipList -match "pywin32") {
    Write-Host "✓ 依賴已安裝" -ForegroundColor Green
} else {
    Write-Host "正在安裝依賴（pywin32）..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ 安裝失敗，請檢查您的網絡連接" -ForegroundColor Red
        Read-Host "按 Enter 退出"
        exit 1
    }
    Write-Host "✓ 依賴安裝完成！" -ForegroundColor Green
}

Write-Host ""
Write-Host "正在啟動應用..." -ForegroundColor Cyan
Write-Host ""

python gui.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "✗ 應用啟動失敗！" -ForegroundColor Red
    Write-Host "請嘗試以管理員身份運行此腳本" -ForegroundColor Yellow
    Read-Host "按 Enter 退出"
    exit 1
}

exit 0
