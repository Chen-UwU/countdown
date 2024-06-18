from typing import TYPE_CHECKING, Any, Type, Optional
from pydantic import BaseModel
from dataclasses import field, dataclass


@dataclass(eq=False)
class PluginMetadata:
    """插件元信息，由插件编写者提供"""

    name: str
    """插件名称"""
    description: str
    """插件功能介绍"""
    usage: str
    """插件使用方法"""
    type: Optional[str] = None
    """插件类型，用于商店分类"""
    homepage: Optional[str] = None
    """插件主页"""
    config: Optional[Type[BaseModel]] = None
    """插件配置项"""
    supported_adapters: Optional[set[str]] = None
    """插件支持的适配器模块路径

    格式为 `<module>[:<Adapter>]`，`~` 为 `nonebot.adapters.` 的缩写。

    `None` 表示支持**所有适配器**。
    """
    extra: dict[Any, Any] = field(default_factory=dict)
    """插件额外信息，可由插件编写者自由扩展定义"""
