# coding=utf-8
import logging
import os
import datetime


def get_logger(logger_name="RYTest"):
    """
    获取配置好的全局 Logger 对象
    """
    logger = logging.getLogger(logger_name)

    # 标准做法：判断当前 logger 是否已经添加过 handler，防止日志重复打印
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 1. 安全的路径处理
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "logs")

        # 自动创建 logs 文件夹，防止报错
        os.makedirs(log_dir, exist_ok=True)

        log_file = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        log_name = os.path.join(log_dir, log_file)  # 统一使用 os.path.join

        # 2. 配置文件 Handler
        file_handle = logging.FileHandler(log_name, 'a', encoding='utf-8')
        file_handle.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s--> %(funcName)s %(levelno)s: %(levelname)s ----->%(message)s')
        file_handle.setFormatter(formatter)

        # 3. 如果需要同时在控制台看到日志，可以取消下面三行的注释
        # console_handle = logging.StreamHandler()
        # console_handle.setFormatter(formatter)
        # logger.addHandler(console_handle)

        logger.addHandler(file_handle)

    return logger


if __name__ == '__main__':
    # 测试调用
    log = get_logger()
    log.info("这是一条测试日志，你再也不用手动 close_handle 了！")