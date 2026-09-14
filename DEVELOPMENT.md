# Windows 11 視窗鎖定器 - 開發指南

## 項目結構

```
windows-window-locker/
├── window_locker.py          # 核心鎖定引擎
├── gui.py                    # GUI 應用程式
├── cli.py                    # 命令行工具
├── test_window_locker.py     # 測試套件
├── requirements.txt          # Python 依賴
├── config.json               # 配置文件
├── start.bat                 # Windows 批次腳本
├── start.ps1                 # PowerShell 腳本
├── start.sh                  # Bash 腳本
├── README.md                 # 說明文件
└── DEVELOPMENT.md            # 本文件
```

## 開發環境設置

### 1. 克隆儲存庫

```bash
git clone https://github.com/hankkc103000205-byte/windows-window-locker.git
cd windows-window-locker
```

### 2. 建立虛擬環境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

### 4. 安裝開發依賴

```bash
pip install pytest pytest-cov black flake8
```

## 代碼風格

### 使用 Black 格式化代碼

```bash
black window_locker.py gui.py cli.py
```

### 使用 Flake8 檢查代碼

```bash
flake8 window_locker.py gui.py cli.py
```

## 運行測試

```bash
# 運行所有測試
python -m pytest test_window_locker.py -v

# 運行並生成覆蓋率報告
python -m pytest test_window_locker.py --cov=. --cov-report=html
```

## 核心模組說明

### window_locker.py

**主要類：**
- `WindowInfo` - 儲存視窗資訊的數據類
- `WindowLocker` - 視窗鎖定器主類

**主要方法：**
- `lock_window(hwnd)` - 鎖定視窗
- `unlock_window(hwnd)` - 解鎖視窗
- `start_monitoring()` - 啟動監控線程
- `stop_monitoring()` - 停止監控線程
- `restore_window_position(hwnd, info)` - 恢復視窗位置

### gui.py

**主要類：**
- `WindowLockerGUI` - GUI 應用程式主類

**主要方法：**
- `create_widgets()` - 建立 GUI 元件
- `lock_selected_window()` - 鎖定選中的視窗
- `unlock_selected_window()` - 解鎖選中的視窗
- `update_window_list()` - 更新視窗列表顯示

### cli.py

**主要函數：**
- `main()` - 命令行工具主入口
- `find_window_by_name()` - 按名稱查找視窗
- `list_all_windows()` - 列出所有視窗

## 擴展功能建議

### 1. 熱鍵支援

在 `gui.py` 中添加全局熱鍵支援，快速鎖定/解鎖當前活動視窗。

```python
from pynput import keyboard

def on_hotkey_lock():
    # 實現熱鍵鎖定功能
    pass

listener = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>+l': on_hotkey_lock
})
```

### 2. 儲存鎖定狀態

將已鎖定視窗列表持久化到文件，應用重啟時自動恢復。

```python
import json

def save_locked_windows(windows):
    with open('locked_windows.json', 'w') as f:
        json.dump(windows, f)

def load_locked_windows():
    with open('locked_windows.json', 'r') as f:
        return json.load(f)
```

### 3. 系統托盤集成

將應用集成到系統托盤，最小化時在後台運行。

```python
from pystray import Icon, Menu, MenuItem

def create_tray_icon():
    icon = Icon("Window Locker", menu=Menu(
        MenuItem("Show", show_window),
        MenuItem("Exit", exit_app)
    ))
    icon.run()
```

### 4. 日誌系統

添加詳細的日誌記錄以便調試。

```python
import logging

logging.basicConfig(
    filename='window_locker.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 已知問題和限制

1. **系統視窗** - 某些系統視窗（如任務管理員）可能無法被鎖定
2. **管理員權限** - 某些操作需要管理員權限才能生效
3. **多屏支援** - 在多屏幕環境下可能需要額外的邊界檢查
4. **性能** - 監控過多視窗時可能影響性能

## 貢獻指南

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 許可證

MIT License

## 聯絡方式

如有問題或建議，請提交 Issue 或 Pull Request。
