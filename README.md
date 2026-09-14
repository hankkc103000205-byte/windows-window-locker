# Windows 11 視窗鎖定器

一個強大的工具，可以鎖定 Windows 11 視窗的位置和大小，防止意外的拖曳和調整大小。

## 功能特性

- 🔒 **鎖定視窗位置和大小** - 防止視窗被移動或調整
- 📋 **實時監控** - 持續監控已鎖定的視窗
- 🖥️ **圖形界面** - 友善的 GUI 應用程式
- 🔄 **多視窗支援** - 同時鎖定多個視窗
- 🔓 **快速解鎖** - 輕鬆解鎖單個或全部視窗

## 系統需求

- Windows 11（也支援 Windows 10）
- Python 3.8 或更高版本
- 管理員權限（建議）

## 安裝

### 1. 克隆儲存庫

```bash
git clone https://github.com/hankkc103000205-byte/windows-window-locker.git
cd windows-window-locker
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

如果遇到 pywin32 安裝問題，請執行：

```bash
python Scripts/pywin32_postinstall.py -install
```

## 使用方法

### 啟動應用

```bash
python gui.py
```

### GUI 操作說明

1. **查看所有視窗** - 應用啟動時會顯示所有打開的視窗
2. **鎖定視窗** - 選擇視窗並點擊「🔒 鎖定選中視窗」按鈕
3. **解鎖視窗** - 選擇已鎖定的視窗並點擊「🔓 解鎖選中視窗」按鈕
4. **刷新列表** - 點擊「🔄 刷新列表」更新視窗列表
5. **解鎖全部** - 點擊「🔓 解鎖全部」解鎖所有已鎖定的視窗
6. **退出應用** - 點擊「❌ 退出」關閉應用

### 程式化使用

```python
from window_locker import WindowLocker
import win32gui

# 建立鎖定器實例
locker = WindowLocker()

# 啟動監控
locker.start_monitoring()

# 取得視窗句柄（hwnd）
hwnd = win32gui.FindWindow(None, "Notepad")

# 鎖定視窗
locker.lock_window(hwnd)

# 列出所有已鎖定的視窗
locked = locker.list_locked_windows()
print(locked)

# 解鎖視窗
locker.unlock_window(hwnd)

# 停止監控
locker.stop_monitoring()
```

## 工作原理

該工具通過以下方式工作：

1. **位置監控** - 每 100ms 檢查一次已鎖定視窗的位置和大小
2. **自動恢復** - 如果檢測到視窗位置或大小改變，立即恢復到鎖定狀態
3. **後台運行** - 使用獨立線程在後台監控，不影響其他操作

## 文件說明

- `window_locker.py` - 核心鎖定引擎
- `gui.py` - 圖形使用者介面
- `requirements.txt` - Python 依賴列表
- `README.md` - 本文件

## 限制事項

- 需要對目標視窗有操作權限
- 某些系統視窗可能無法鎖定
- 需要 Python 和 pywin32 支援

## 故障排查

### 問題：應用無法找到視窗

**解決方案：** 確保視窗已打開並可見，點擊「🔄 刷新列表」重新掃描視窗。

### 問題：鎖定不生效

**解決方案：** 
- 以管理員身份運行應用
- 檢查目標應用是否有特殊的視窗保護
- 嘗試重新啟動應用

### 問題：ImportError: No module named 'win32gui'

**解決方案：**
```bash
pip install pywin32
python Scripts/pywin32_postinstall.py -install
```

## 安全性注意事項

- 該工具可能被防病毒軟體標記，這是正常的行為
- 建議僅在受信任的環境中使用
- 某些應用程式可能禁止視窗被鎖定

## 許可證

MIT License - 詳見 LICENSE 文件

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 作者

hankkc103000205-byte

## 更新日誌

### v1.0.0 (2026-09-14)
- 初始版本發布
- 核心鎖定功能
- GUI 應用程式
- 實時監控系統
