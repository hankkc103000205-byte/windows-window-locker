"""
Windows 11 Window Locker GUI - 圖形使用者介面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import win32gui
import threading
from window_locker import WindowLocker

class WindowLockerGUI:
    """視窗鎖定器 GUI 應用"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 11 視窗鎖定器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 初始化鎖定器
        self.locker = WindowLocker()
        
        # 設定 GUI 樣式
        self.setup_styles()
        
        # 建立 GUI 元件
        self.create_widgets()
        
        # 自動啟動監控
        self.locker.start_monitoring()
        
        # 定期更新視窗列表
        self.update_window_list()
    
    def setup_styles(self):
        """設定 GUI 樣式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 設定顏色主題
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Normal.TLabel', font=('Arial', 10))
        style.configure('Button.TButton', font=('Arial', 10))
    
    def create_widgets(self):
        """建立 GUI 元件"""
        # 標題
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10, padx=10, fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="Windows 11 視窗鎖定器", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # 狀態標籤
        status_frame = ttk.LabelFrame(self.root, text="監控狀態", padding=10)
        status_frame.pack(pady=5, padx=10, fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="監控: 運行中", foreground='green')
        self.status_label.pack(side=tk.LEFT)
        
        # 所有視窗列表
        windows_frame = ttk.LabelFrame(self.root, text="所有視窗", padding=10)
        windows_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # 視窗列表框
        self.windows_listbox = tk.Listbox(windows_frame, height=10, width=70, font=('Arial', 9))
        self.windows_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 捲軸
        scrollbar = ttk.Scrollbar(windows_frame, orient=tk.VERTICAL, command=self.windows_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.windows_listbox.config(yscrollcommand=scrollbar.set)
        
        # 按鈕框架
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # 鎖定按鈕
        self.lock_button = ttk.Button(button_frame, text="🔒 鎖定選中視窗", command=self.lock_selected_window)
        self.lock_button.pack(side=tk.LEFT, padx=5)
        
        # 解鎖按鈕
        self.unlock_button = ttk.Button(button_frame, text="🔓 解鎖選中視窗", command=self.unlock_selected_window)
        self.unlock_button.pack(side=tk.LEFT, padx=5)
        
        # 刷新按鈕
        refresh_button = ttk.Button(button_frame, text="🔄 刷新列表", command=self.refresh_windows)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # 被鎖定視窗列表
        locked_frame = ttk.LabelFrame(self.root, text="已鎖定的視窗", padding=10)
        locked_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        self.locked_listbox = tk.Listbox(locked_frame, height=6, width=70, font=('Arial', 9))
        self.locked_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 捲軸
        locked_scrollbar = ttk.Scrollbar(locked_frame, orient=tk.VERTICAL, command=self.locked_listbox.yview)
        locked_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.locked_listbox.config(yscrollcommand=locked_scrollbar.set)
        
        # 底部按鈕
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(pady=10, padx=10, fill=tk.X)
        
        exit_button = ttk.Button(bottom_frame, text="❌ 退出", command=self.exit_app)
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        unlock_all_button = ttk.Button(bottom_frame, text="🔓 解鎖全部", command=self.unlock_all_windows)
        unlock_all_button.pack(side=tk.RIGHT, padx=5)
    
    def get_all_windows(self):
        """取得所有視窗"""
        windows = []
        
        def enum_windows(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # 只顯示有標題的視窗
                    windows.append((hwnd, title))
            return True
        
        win32gui.EnumWindows(enum_windows, None)
        return windows
    
    def update_window_list(self):
        """更新視窗列表"""
        self.windows_listbox.delete(0, tk.END)
        self.locked_listbox.delete(0, tk.END)
        
        # 取得所有視窗
        all_windows = self.get_all_windows()
        
        # 新增到列表框
        for hwnd, title in all_windows:
            if len(title) > 60:
                display_title = title[:57] + "..."
            else:
                display_title = title
            
            if self.locker.is_window_locked(hwnd):
                self.windows_listbox.insert(tk.END, f"🔒 {display_title}")
                self.windows_listbox.itemconfig(tk.END, {'bg': '#e8f5e9'})
            else:
                self.windows_listbox.insert(tk.END, f"   {display_title}")
        
        # 更新已鎖定視窗列表
        locked_windows = self.locker.list_locked_windows()
        for window in locked_windows:
            title = window['title']
            if len(title) > 60:
                display_title = title[:57] + "..."
            else:
                display_title = title
            
            pos_x, pos_y = window['position']
            width, height = window['size']
            info_text = f"🔒 {display_title} | 位置: ({pos_x}, {pos_y}) | 大小: {width}x{height}"
            self.locked_listbox.insert(tk.END, info_text)
        
        # 每 1000ms 更新一次
        self.root.after(1000, self.update_window_list)
    
    def lock_selected_window(self):
        """鎖定選中的視窗"""
        selection = self.windows_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "請先選擇要鎖定的視窗")
            return
        
        index = selection[0]
        all_windows = self.get_all_windows()
        
        if index < len(all_windows):
            hwnd, title = all_windows[index]
            if self.locker.lock_window(hwnd):
                messagebox.showinfo("成功", f"已鎖定視窗: {title}")
            else:
                messagebox.showerror("失敗", "無法鎖定此視窗")
    
    def unlock_selected_window(self):
        """解鎖選中的視窗"""
        selection = self.windows_listbox.curselection()
        if not selection:
            messagebox.showwarning("提示", "請先選擇要解鎖的視窗")
            return
        
        index = selection[0]
        all_windows = self.get_all_windows()
        
        if index < len(all_windows):
            hwnd, title = all_windows[index]
            if self.locker.unlock_window(hwnd):
                messagebox.showinfo("成功", f"已解鎖視窗: {title}")
            else:
                messagebox.showwarning("提示", "此視窗未被鎖定")
    
    def unlock_all_windows(self):
        """解鎖所有視窗"""
        if not self.locker.locked_windows:
            messagebox.showinfo("提示", "沒有已鎖定的視窗")
            return
        
        confirm = messagebox.askyesno("確認", "確定要解鎖所有視窗嗎?")
        if confirm:
            hwnd_list = list(self.locker.locked_windows.keys())
            for hwnd in hwnd_list:
                self.locker.unlock_window(hwnd)
            messagebox.showinfo("成功", f"已解鎖 {len(hwnd_list)} 個視窗")
    
    def refresh_windows(self):
        """刷新視窗列表"""
        self.update_window_list()
        messagebox.showinfo("完成", "視窗列表已刷新")
    
    def exit_app(self):
        """退出應用"""
        confirm = messagebox.askyesno("確認退出", "確定要退出嗎?\n(所有鎖定將被移除)")
        if confirm:
            self.locker.stop_monitoring()
            self.root.quit()

def main():
    """主函數"""
    root = tk.Tk()
    app = WindowLockerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
