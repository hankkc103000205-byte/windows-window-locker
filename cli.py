"""
Windows 11 Window Locker - 命令行工具
"""

import argparse
import sys
from window_locker import WindowLocker
import win32gui

def find_window_by_name(window_name):
    """根據視窗名稱查找視窗句柄"""
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd == 0:
        return None
    return hwnd

def list_all_windows():
    """列出所有視窗"""
    windows = []
    
    def enum_windows(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                windows.append((hwnd, title))
        return True
    
    win32gui.EnumWindows(enum_windows, None)
    return windows

def main():
    parser = argparse.ArgumentParser(
        description='Windows 11 視窗鎖定器 - 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s --list                          # 列出所有視窗
  %(prog)s --lock "Notepad"                # 鎖定 Notepad 視窗
  %(prog)s --unlock "Notepad"              # 解鎖 Notepad 視窗
  %(prog)s --lock-all                      # 鎖定所有視窗（不推薦）
  %(prog)s --unlock-all                    # 解鎖所有視窗
        '''
    )
    
    parser.add_argument('--list', action='store_true', 
                        help='列出所有打開的視窗')
    parser.add_argument('--lock', metavar='WINDOW_NAME', 
                        help='鎖定指定名稱的視窗')
    parser.add_argument('--unlock', metavar='WINDOW_NAME',
                        help='解鎖指定名稱的視窗')
    parser.add_argument('--lock-all', action='store_true',
                        help='鎖定所有視窗（不推薦）')
    parser.add_argument('--unlock-all', action='store_true',
                        help='解鎖所有視窗')
    parser.add_argument('--monitor', action='store_true',
                        help='啟動監控模式（持續監控已鎖定的視窗）')
    parser.add_argument('--gui', action='store_true',
                        help='啟動 GUI 應用')
    
    args = parser.parse_args()
    
    # 如果沒有提供任何參數，顯示幫助信息
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # 啟動 GUI 模式
    if args.gui:
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError:
            print("錯誤：無法導入 GUI 模組")
            sys.exit(1)
        return
    
    # 初始化鎖定器
    locker = WindowLocker()
    
    # 列出所有視窗
    if args.list:
        windows = list_all_windows()
        if not windows:
            print("沒有找到打開的視窗")
            return
        
        print("\n=== 打開的視窗列表 ===\n")
        for hwnd, title in windows:
            locked_status = "🔒" if locker.is_window_locked(hwnd) else "  "
            print(f"{locked_status} [{hwnd:10d}] {title}")
        print(f"\n共 {len(windows)} 個視窗\n")
    
    # 鎖定指定視窗
    elif args.lock:
        hwnd = find_window_by_name(args.lock)
        if hwnd is None:
            print(f"錯誤：未找到名為 '{args.lock}' 的視窗")
            sys.exit(1)
        
        if locker.lock_window(hwnd):
            print(f"✓ 已鎖定視窗: {args.lock}")
            if args.monitor:
                locker.start_monitoring()
                try:
                    import time
                    print("監控已啟動（按 Ctrl+C 停止）...")
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n監控已停止")
                    locker.stop_monitoring()
        else:
            print(f"✗ 無法鎖定視窗: {args.lock}")
            sys.exit(1)
    
    # 解鎖指定視窗
    elif args.unlock:
        hwnd = find_window_by_name(args.unlock)
        if hwnd is None:
            print(f"錯誤：未找到名為 '{args.unlock}' 的視窗")
            sys.exit(1)
        
        if locker.unlock_window(hwnd):
            print(f"✓ 已解鎖視窗: {args.unlock}")
        else:
            print(f"✗ 視窗未被鎖定或解鎖失敗: {args.unlock}")
            sys.exit(1)
    
    # 鎖定所有視窗
    elif args.lock_all:
        windows = list_all_windows()
        count = 0
        for hwnd, title in windows:
            if locker.lock_window(hwnd):
                count += 1
        
        print(f"✓ 已鎖定 {count} 個視窗")
        if args.monitor:
            locker.start_monitoring()
            try:
                import time
                print("監控已啟動（按 Ctrl+C 停止）...")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n監控已停止")
                locker.stop_monitoring()
    
    # 解鎖所有視窗
    elif args.unlock_all:
        locked_windows = locker.list_locked_windows()
        count = 0
        for window in locked_windows:
            if locker.unlock_window(window['hwnd']):
                count += 1
        
        print(f"✓ 已解鎖 {count} 個視窗")
    
    # 監控模式
    elif args.monitor:
        locker.start_monitoring()
        try:
            import time
            print("監控已啟動（按 Ctrl+C 停止）...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n監控已停止")
            locker.stop_monitoring()

if __name__ == '__main__':
    main()
