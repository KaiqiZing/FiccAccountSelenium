# coding=utf-8
import allure
import pytest

from business.RY_UserManage_Business import RYUserManageBusiness
from log.user_log import get_logger
from util.CheckErrorCapture import check_and_capture_error
from util.data_manager import DataManager

logger = get_logger()


@allure.feature("用户管理")
@allure.story("YAML 数据驱动新增用户")
class TestRYUserManageYaml:

    def test_add_user_workflow_from_yaml(self, driver):
        logger.info("========== 开始执行：YAML 数据驱动的用户管理工作流 ==========")

        with allure.step("加载 YAML 测试数据"):
            all_data = DataManager().get_yaml("user_manage.yaml")
            user_manage_data = all_data.get("user_manage_page_add", {})

            if not user_manage_data:
                pytest.fail("YAML 数据加载异常：未找到 user_manage_page_add 节点")

            login_name = user_manage_data.get("LoginName")
            login_password = user_manage_data.get("LoginPassword")

            logger.info(f"动态数据加载成功 -> 用户: [{user_manage_data.get('UserName')}], "
                         f"手机号: [{user_manage_data.get('MobilePhone')}]")

        biz = RYUserManageBusiness(driver)

        with allure.step("登录系统"):
            biz.Login(login_name, login_password)

        with allure.step(f"新增用户: {user_manage_data.get('UserName')}"):
            biz.AddUser(user_manage_data)

        with allure.step("检查是否出现错误弹窗"):
            if check_and_capture_error(driver):
                pytest.fail(f"业务执行失败，页面出现红色错误弹窗！(用户: {user_manage_data.get('UserName')})")

        logger.info(f"========== 执行成功：用户 [{user_manage_data.get('UserName')}] 工作流测试通过 ==========")
