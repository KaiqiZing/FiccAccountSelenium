import time
import pyautogui
class PyautoguiUpDown:

    def __init__(self, file_path=None):
        """
        上传测试过程中的文件
        :param file_path:
        """
        self.file_path = file_path if file_path else "C:\\Users\\GTJA\\Pictures\\test111.png"

    def PyautoguiWrite(self,file_path=None):
        """
              使用 PyAutoGUI 写入文件路径，并按下回车键两次。
              Args:
              file_path (str, optional): 文件路径。如果未提供，则使用初始化时的默认路径。默认为 None.
      """
        file_path = file_path if file_path else self.file_path
        pyautogui.write(file_path)
        pyautogui.press('enter')
        pyautogui.press('enter')


