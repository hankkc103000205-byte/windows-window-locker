"""
測試套件 - Windows 視窗鎖定器
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from window_locker import WindowLocker, WindowInfo

class TestWindowLocker(unittest.TestCase):
    """測試 WindowLocker 類"""
    
    def setUp(self):
        """設定測試環境"""
        self.locker = WindowLocker()
    
    def test_initialization(self):
        """測試初始化"""
        self.assertIsNotNone(self.locker)
        self.assertEqual(len(self.locker.locked_windows), 0)
        self.assertFalse(self.locker.monitoring)
    
    @patch('win32gui.GetWindowText')
    @patch('win32gui.GetWindowRect')
    def test_get_window_info(self, mock_rect, mock_text):
        """測試獲取視窗資訊"""
        mock_text.return_value = "Test Window"
        mock_rect.return_value = (100, 200, 300, 400)
        
        info = self.locker.get_window_info(12345)
        
        self.assertIsNotNone(info)
        self.assertEqual(info.hwnd, 12345)
        self.assertEqual(info.title, "Test Window")
        self.assertEqual(info.x, 100)
        self.assertEqual(info.y, 200)
        self.assertEqual(info.width, 200)  # 300 - 100
        self.assertEqual(info.height, 200)  # 400 - 200
    
    @patch('window_locker.WindowLocker.get_window_info')
    def test_lock_window(self, mock_get_info):
        """測試鎖定視窗"""
        mock_info = WindowInfo(
            hwnd=12345,
            title="Test Window",
            x=100, y=200,
            width=200, height=200
        )
        mock_get_info.return_value = mock_info
        
        result = self.locker.lock_window(12345)
        
        self.assertTrue(result)
        self.assertIn(12345, self.locker.locked_windows)
        self.assertEqual(self.locker.locked_windows[12345], mock_info)
    
    def test_unlock_window(self):
        """測試解鎖視窗"""
        # 先鎖定視窗
        test_info = WindowInfo(
            hwnd=12345,
            title="Test Window",
            x=100, y=200,
            width=200, height=200
        )
        self.locker.locked_windows[12345] = test_info
        
        # 解鎖視窗
        result = self.locker.unlock_window(12345)
        
        self.assertTrue(result)
        self.assertNotIn(12345, self.locker.locked_windows)
    
    def test_is_window_locked(self):
        """測試檢查視窗是否被鎖定"""
        test_info = WindowInfo(
            hwnd=12345,
            title="Test Window",
            x=100, y=200,
            width=200, height=200
        )
        self.locker.locked_windows[12345] = test_info
        
        self.assertTrue(self.locker.is_window_locked(12345))
        self.assertFalse(self.locker.is_window_locked(54321))
    
    @patch('ctypes.windll.user32.SetWindowPos')
    def test_restore_window_position(self, mock_set_pos):
        """測試恢復視窗位置"""
        mock_set_pos.return_value = True
        
        test_info = WindowInfo(
            hwnd=12345,
            title="Test Window",
            x=100, y=200,
            width=200, height=200
        )
        
        result = self.locker.restore_window_position(12345, test_info)
        
        self.assertTrue(result)
        mock_set_pos.assert_called_once()
    
    def test_list_locked_windows(self):
        """測試列出所有已鎖定的視窗"""
        test_info1 = WindowInfo(
            hwnd=12345,
            title="Test Window 1",
            x=100, y=200,
            width=200, height=200
        )
        test_info2 = WindowInfo(
            hwnd=54321,
            title="Test Window 2",
            x=300, y=400,
            width=300, height=300
        )
        
        self.locker.locked_windows[12345] = test_info1
        self.locker.locked_windows[54321] = test_info2
        
        windows = self.locker.list_locked_windows()
        
        self.assertEqual(len(windows), 2)
        self.assertEqual(windows[0]['hwnd'], 12345)
        self.assertEqual(windows[0]['title'], "Test Window 1")
        self.assertEqual(windows[1]['hwnd'], 54321)
        self.assertEqual(windows[1]['title'], "Test Window 2")
    
    def test_start_monitoring(self):
        """測試啟動監控"""
        self.assertFalse(self.locker.monitoring)
        self.locker.start_monitoring()
        self.assertTrue(self.locker.monitoring)
        self.assertIsNotNone(self.locker.monitor_thread)
        
        # 清理
        self.locker.stop_monitoring()
    
    def test_stop_monitoring(self):
        """測試停止監控"""
        self.locker.start_monitoring()
        self.assertTrue(self.locker.monitoring)
        
        self.locker.stop_monitoring()
        self.assertFalse(self.locker.monitoring)

class TestWindowInfo(unittest.TestCase):
    """測試 WindowInfo 類"""
    
    def test_window_info_creation(self):
        """測試建立 WindowInfo 對象"""
        info = WindowInfo(
            hwnd=12345,
            title="Test",
            x=10, y=20,
            width=100, height=200
        )
        
        self.assertEqual(info.hwnd, 12345)
        self.assertEqual(info.title, "Test")
        self.assertEqual(info.x, 10)
        self.assertEqual(info.y, 20)
        self.assertEqual(info.width, 100)
        self.assertEqual(info.height, 200)

if __name__ == '__main__':
    unittest.main()
