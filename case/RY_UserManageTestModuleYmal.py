# coding=utf-8
import pytest
from log.user_log import get_logger
from util.data_manager import DataManager
from business.RY_UserManage_Business import RYUserManageBusiness
from handle.RY_Handle.RY_UserManage_Handle import RYUserManageHandle
from util.CheckErrorCapture import check_and_capture_error

logger = get_logger()


class TestRYUserManageYaml:

    def test_add_user_workflow_from_yaml(self, driver):
        logger.info("========== 开始执行：YAML 数据驱动的用户管理工作流 ==========")

        all_data = DataManager().get_yaml("user_manage.yaml")
        user_manage_data = all_data.get("user_manage_page_add", {})

        if not user_manage_data:
            pytest.fail("YAML 数据加载异常：未找到 user_manage_page_add 节点")

        login_name = user_manage_data.get("LoginName")
        login_password = user_manage_data.get("LoginPassword")

        logger.info(f"动态数据加载成功 -> 用户: [{user_manage_data.get('UserName')}], "
                     f"手机号: [{user_manage_data.get('MobilePhone')}]")

        # 步骤 A：只做登录（调新方法 Login，不触发用户管理）
        login_biz = RYUserManageBusiness(driver)
        login_biz.Login(login_name, login_password)

        # 步骤 B：用 YAML 数据执行用户管理
        user_manage_handle = RYUserManageHandle(driver)
        user_manage_handle.RY_UserManage_From_Dict(user_manage_data)

        # 步骤 C：业务断言
        if check_and_capture_error(driver):
            pytest.fail(f"业务执行失败，页面出现红色错误弹窗！(用户: {user_manage_data.get('UserName')})")

        logger.info(f"========== 执行成功：用户 [{user_manage_data.get('UserName')}] 工作流测试通过 ==========")
