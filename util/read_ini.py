#coding=utf-8
import configparser
import os

# 动态获取项目根目录 (假设 util 文件夹在项目根目录下)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ReadIni(object):
    def __init__(self, file_name=None, node=None):
        """
        :param file_name: 文件路径
        :param node: ini的节点名称
        """
        # 如果未传参，默认指向 LocalElement.ini
        if file_name is None:
            self.file_name = os.path.join(BASE_DIR, "config", "LocalElement.ini")
        else:
            # 兼容老代码中传入的 "../config/xxx.ini" 相对路径，智能转为绝对路径
            if file_name.startswith("../"):
                self.file_name = os.path.join(BASE_DIR, file_name.replace("../", ""))
            else:
                self.file_name = file_name

        self.node = node if node else "RegisterElement"
        self.cf = self.load_ini()

    def load_ini(self):
        """加载ini文件"""
        cf = configparser.ConfigParser()
        try:
            cf.read(self.file_name, encoding="utf-8")
            return cf
        except Exception as e:
            print(f"配置文件读取失败: {self.file_name}, Error: {e}")
            return None

    def get_value(self, key):
        """获取具体的value"""
        try:
            return self.cf.get(self.node, key)
        except Exception as e:
            print(f"未找到节点 [{self.node}] 下的 key [{key}], Error: {e}")
            return None

if __name__ == "__main__":
    # 测试INI文件读取
    ini_reader = ReadIni(file_name="../config/LocalElement.ini")

    # 测试获取值
    user_name = ini_reader.get_value("user_name")
    print(f"user_name: {user_name}")

    # 测试TXT文件读取（如果需要）
    # txt_reader = ReadIni(file_path="../config/PlateformRegisterCompanyData.txt")
    # company_names = txt_reader.read_txt_file()
    # print(f"company_names: {company_names}")