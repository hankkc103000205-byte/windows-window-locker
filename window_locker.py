"""
Windows 11 Window Locker - Prevents window position and size changes
"""

import ctypes
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass
from typing import Dict, Optional
import win32gui
import win32con

# Windows API 常數
WM_MOVING = 0x0216
WM_SIZING = 0x0214
WM_WINDOWPOSCHANGING = 0x0046

@dataclass
class WindowInfo:
    """視窗資訊類"""
    hwnd: int
    title: str
    x: int
    y: int
    width: int
    height: int
    
class WindowLocker:
    """Windows 視窗鎖定器"""
    
    def __init__(self):
        self.locked_windows: Dict[int, WindowInfo] = {}
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
    def get_window_info(self, hwnd: int) -> Optional[WindowInfo]:
        """獲取視窗資訊"""
        try:
            title = win32gui.GetWindowText(hwnd)
            rect = win32gui.GetWindowRect(hwnd)
            x, y, right, bottom = rect
            width = right - x
            height = bottom - y
            
            return WindowInfo(
                hwnd=hwnd,
                title=title,
                x=x,
                y=y,
                width=width,
                height=height
            )
        except Exception as e:
            print(f"無法獲取視窗資訊: {e}")
            return None
    
    def lock_window(self, hwnd: int) -> bool:
        """鎖定指定的視窗"""
        window_info = self.get_window_info(hwnd)
        if window_info:
            self.locked_windows[hwnd] = window_info
            print(f"已鎖定視窗: {window_info.title}")
            return True
        return False
    
    def unlock_window(self, hwnd: int) -> bool:
        """解鎖指定的視窗"""
        if hwnd in self.locked_windows:
            window_info = self.locked_windows[hwnd]
            del self.locked_windows[hwnd]
            print(f"已解鎖視窗: {window_info.title}")
            return True
        return False
    
    def is_window_locked(self, hwnd: int) -> bool:
        """檢查視窗是否被鎖定"""
        return hwnd in self.locked_windows
    
    def restore_window_position(self, hwnd: int, window_info: WindowInfo) -> bool:
        """恢復視窗位置和大小"""
        try:
            # 使用 SetWindowPos 恢復視窗位置和大小
            ctypes.windll.user32.SetWindowPos(
                ctypes.c_void_p(hwnd),
                None,
                window_info.x,
                window_info.y,
                window_info.width,
                window_info.height,
                0x0010  # SWP_NOZORDER
            )
            return True
        except Exception as e:
            print(f"無法恢復視窗位置: {e}")
            return False
    
    def start_monitoring(self):
        """開始監控被鎖定的視窗"""
        if self.monitoring:
            print("監控已在運行中")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("視窗監控已啟動")
    
    def stop_monitoring(self):
        """停止監控"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("視窗監控已停止")
    
    def _monitor_loop(self):
        """監控循環 - 檢查被鎖定視窗是否被移動或調整大小"""
        while self.monitoring:
            for hwnd, locked_info in list(self.locked_windows.items()):
                try:
                    # 檢查視窗是否仍然存在
                    if not win32gui.IsWindow(hwnd):
                        del self.locked_windows[hwnd]
                        continue
                    
                    # 獲取當前視窗位置和大小
                    current_info = self.get_window_info(hwnd)
                    if not current_info:
                        continue
                    
                    # 檢查位置或大小是否改變
                    if (current_info.x != locked_info.x or
                        current_info.y != locked_info.y or
                        current_info.width != locked_info.width or
                        current_info.height != locked_info.height):
                        
                        # 恢復到鎖定的位置和大小
                        self.restore_window_position(hwnd, locked_info)
                        print(f"已恢復視窗位置: {locked_info.title}")
                
                except Exception as e:
                    print(f"監控錯誤: {e}")
            
            time.sleep(0.1)  # 每 100ms 檢查一次
    
    def list_locked_windows(self) -> list:
        """列出所有被鎖定的視窗"""
        windows = []
        for hwnd, info in self.locked_windows.items():
            windows.append({
                'hwnd': hwnd,
                'title': info.title,
                'position': (info.x, info.y),
                'size': (info.width, info.height)
            })
        return windows
