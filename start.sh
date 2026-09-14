#!/bin/bash
# Windows 11 視窗鎖定器 - Bash 啟動腳本（Linux/Mac）

echo "===================================="
echo "Windows 11 Window Locker"
echo "===================================="
echo ""

# 檢查 Python 是否已安裝
if ! command -v python3 &> /dev/null; then
    echo "✗ 錯誤：找不到 Python"
    echo "請先安裝 Python 3.8 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "✓ 找到 Python: $PYTHON_VERSION"
echo ""

echo "正在檢查依賴..."

# 檢查是否已安裝 pywin32
if python3 -m pip list | grep -q pywin32; then
    echo "✓ 依賴已安裝"
else
    echo "正在安裝依賴（pywin32）..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "✗ 安裝失敗，請檢查您的網絡連接"
        exit 1
    fi
    echo "✓ 依賴安裝完成！"
fi

echo ""
echo "正在啟動應用..."
echo ""

python3 gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ 應用啟動失敗！"
    exit 1
fi

exit 0
