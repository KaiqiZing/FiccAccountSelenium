# coding=utf-8
import time
import unittest
from selenium import webdriver
from log.user_log import UserLog
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from AccountUtils.AccountPandasExcel import Read_Pandas_Excel
from business.RY_Login_Business import RYLoginBusiness
from log.user_log import UserLog
from util.CheckErrorCapture import check_and_capture_error
LOGIN_URL = "http://localhost:1024/login?redirect=%2Findex"


class AccountRegisterCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        :return:
        """
        cls.log = UserLog()
        cls.logger = cls.log.get_log()
        cls.driver = webdriver.Chrome()
        cls.driver.get(LOGIN_URL)
        cls.driver.maximize_window()
    def setUp(self):
        self.driver.refresh()
        self.UserManagePages = RYLoginBusiness(self.driver)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.driver.close()

    def test_register_success(self):

        GetPandasValues = Read_Pandas_Excel(file_path="../config/RYAccountData.csv")
        data_dict, num_rows = GetPandasValues.read_excel()
        for i in range(0, num_rows - 1):
            test_account = GetPandasValues.get_value("测试账号", i)
            test_password = GetPandasValues.get_value("测试密码", i)
            with self.subTest(row=i):
                pass
                    # success = self.UserManagePages.LoginTest(test_account, test_password, i)
                # self.assertTrue(success == None)  # 根据实际情况调整断言逻辑

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(AccountRegisterCase('test_register_success'))