"""项目通用异常定义。"""
from __future__ import annotations

from typing import Any, Optional


class FrameworkError(Exception):
    """框架基础异常，统一保留 message。"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class ElementNotFoundError(FrameworkError):
    """元素查找失败异常。"""

    def __init__(
        self,
        message: str,
        locator: Optional[Any] = None,
        screenshot_path: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.locator = locator
        self.screenshot_path = screenshot_path

    def __str__(self) -> str:
        parts = [self.message]
        if self.locator is not None:
            parts.append(f"定位器: {self.locator}")
        if self.screenshot_path:
            parts.append(f"截图: {self.screenshot_path}")
        return " / ".join(parts)


class BusinessError(FrameworkError):
    """业务流程执行失败异常。"""

    def __init__(self, message: str, business_context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.business_context = business_context or {}

    def __str__(self) -> str:
        if not self.business_context:
            return self.message
        return f"{self.message} / 上下文: {self.business_context}"


class ConfigError(FrameworkError):
    """配置读取/解析失败异常。"""

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_file: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.config_key = config_key
        self.config_file = config_file

    def __str__(self) -> str:
        parts = [self.message]
        if self.config_key:
            parts.append(f"配置键: {self.config_key}")
        if self.config_file:
            parts.append(f"配置文件: {self.config_file}")
        return " / ".join(parts)
