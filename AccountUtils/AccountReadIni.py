#coding=utf-8
import configparser


class ReadIni(object):

    def __init__(self,file_name=None,node=None, file_path=None):
        """
        ini文件的操作方法

        :param file_name:文件名
        :param node:
        :param file_path:文件路径
        """
        if file_name == None:
            self.file_name = "../config/LocalElement.ini"
        else:
            self.file_name = file_name

        if node == None:
            self.node = "RegisterElement"
        if file_path == None:
            self.file_path = "../config/PlateformRegisterCompanyData.txt"
        else:

            self.file_path= file_path
            self.node = node
        self.cf = self.load_ini()
    #加载文件
    def load_ini(self):
        """
        加载ini文件
        :return:
        """
        try:
            cf = configparser.ConfigParser()
            cf.read(self.file_name,encoding="utf-8")
            return cf
        except FileNotFoundError:
            print("FIle not found:", self.file_name)
            return None
        except Exception as e:
            print("An error occured:", e)
            return None
    def get_value(self,key):
        """
            #从加载的ini文件中，获取value得值
        :param key:
        :return:
        """
        try:
            data = self.cf.get(self.node,key)
            return data
        except Exception as e:
            print("从加载的ini文件中,获取值失败报错：", e)
            return None

    def read_txt_file(self):
        """
        加载txt文件
        :return:
        """
        try:
            content = []
            with open(self.file_path, "r",encoding='utf-8') as file:
                for line in file:
                    content.append(line.strip())
            return content
        except FileNotFoundError:
            print("FIle not found:", self.file_path)
            return None
        except Exception as e:
            print("An error occured:", e)
            return None


if __name__ == '__main__':
    getdata = ReadIni()
    print(getdata.read_txt_file())