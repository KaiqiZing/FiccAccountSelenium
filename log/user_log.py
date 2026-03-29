# coding=utf-8
from __future__ import annotations

import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler


class SensitiveFilter(logging.Filter):
    """对常见敏感字段做日志脱敏。"""

    PATTERNS = [
        re.compile(r"(?i)(password\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r"(?i)(token\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r"(?i)(authorization\s*[=:]\s*)(['\"]?)([^,'\"\s]+)(\2)"),
        re.compile(r'(?i)("password"\s*:\s*")([^"]+)(")'),
        re.compile(r'(?i)("token"\s*:\s*")([^"]+)(")'),
        re.compile(r'(?i)("authorization"\s*:\s*")([^"]+)(")'),
    ]

    @classmethod
    def mask(cls, message: str) -> str:
        masked = message
        for pattern in cls.PATTERNS:
            def _replace(match: re.Match[str]) -> str:
                groups = match.groups()
                if len(groups) == 4:
                    return f"{groups[0]}{groups[1]}******{groups[3]}"
                if len(groups) == 3:
                    return f"{groups[0]}******{groups[2]}"
                return "******"

            masked = pattern.sub(_replace, masked)
        return masked

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.mask(record.getMessage())
        record.args = ()
        return True


def get_logger(logger_name="RYTest"):
    """
    获取配置好的全局 Logger 对象
    """
    logger = logging.getLogger(logger_name)

    # 标准做法：判断当前 logger 是否已经添加过 handler，防止日志重复打印
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        # 1. 安全的路径处理
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "logs")

        # 自动创建 logs 文件夹，防止报错
        os.makedirs(log_dir, exist_ok=True)

        log_file = f"{logger_name}.log"
        log_name = os.path.join(log_dir, log_file)  # 统一使用 os.path.join

        # 2. 配置文件 Handler
        file_handle = TimedRotatingFileHandler(
            filename=log_name,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8",
        )
        file_handle.suffix = "%Y-%m-%d.log"
        file_handle.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s--> %(funcName)s %(levelno)s: %(levelname)s ----->%(message)s')
        file_handle.setFormatter(formatter)
        file_handle.addFilter(SensitiveFilter())

        # 3. 控制台输出
        console_handle = logging.StreamHandler()
        console_handle.setLevel(logging.INFO)
        console_handle.setFormatter(formatter)
        console_handle.addFilter(SensitiveFilter())

        logger.addHandler(file_handle)
        logger.addHandler(console_handle)

    return logger


if __name__ == '__main__':
    # 测试调用
    log = get_logger()
    log.info("这是一条测试日志，你再也不用手动 close_handle 了！")