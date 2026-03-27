import pandas as pd

class Read_Pandas_Excel:

    def __init__(self, file_path=None, n=None):
        if file_path == None:
            self.file_path = "../config/acoountdata.csv"
        else:
            self.file_path = file_path

        if n == None:
            self.n = 1
        else:
            self.n = n

    def read_excel(self):
        """
        读取CSV文件，第一行作为 key，后续行作为对应 key 的 values 返回键值对
        :return: 键值对字典
        """
        try:
            df = pd.read_csv(self.file_path, header=None, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(self.file_path, header=None, encoding='gbk')

        data_dict = {}
        keys = df.iloc[0]  # First row as keys
        num_rows = df.shape[0]  # Number of rows in the DataFrame excluding header
        for col in range(len(keys)):
            key = keys[col]
            values = df.iloc[1:num_rows, col].tolist()  # Values for each key (from row 1 to num_rows)
            data_dict[key] = values

        return data_dict, num_rows

    def get_value(self, key,nums):
        try:
            data_dict = self.read_excel()[0]
            if key not in data_dict:
                raise KeyError(f"Key '{key}' not found in data.")
            else:
                return data_dict[key][nums]
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def handle_labels(self, x,y,z):
        ssjm_label = f"ssjm_label{x}"
        jgss_label = f"jgss_label{y}"
        czrss_label = f"czrss_label{z}"
        return ssjm_label, jgss_label, czrss_label

if __name__ == "__main__":
    getPandas = Read_Pandas_Excel()
    data_dict, num_rows = getPandas.read_excel()
    result = [{'phone': number} for number in data_dict["测试账号"]]
    print(result)
"""
目前以csv文件形式做数据的保存，其中以行数据作为每条测试用例来执行
case1,case2,case3...caseN为第一行，第二行，第三行...第N行；
执行结果以断言成功为准；
失败结果使用日志进行记录，将每个页面划分为多个模块，如果某个模块有问题，则可以直接定位到大致模块位置
后期拓展：如果有报错信息，则进行截图并将截图信息保存在固定位置，截图信息以当日时间精确到秒级别命名保存在同一文件夹中
，其中文件夹以每日为分割进行划分，保证数据可以分类；
"""