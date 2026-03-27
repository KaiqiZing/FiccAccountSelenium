import time
import pyautogui
class PyautoguiUpDown:

    def __init__(self, file_path=None):
        self.file_path = file_path if file_path else "C:\\Users\\GTJA\\Pictures\\testfilepdf"

    def PyautoguiWrite(self,file_path=None):
        """

        :param file_path:
        :return:
        """
        file_path = file_path if file_path else self.file_path
        pyautogui.write(file_path)
        pyautogui.press('enter')
        pyautogui.press('enter')


