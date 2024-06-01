import abc


class Adapter(abc.ABC):
    """协议适配器的基类

    在 Adapter 中编写与系统交互的相关代码，如：更换壁纸，创建播放壁纸的窗口等。

    虽然部分交互如环境信息能通过 os 和 sys 库实现，但是部分系统更换壁纸的功能无法直接通过这俩个库实现。

    参数:
        暂无
    """

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"Adapter(name={self.get_name()!r})"

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """当前协议适配器的名称。"""
        raise NotImplementedError

    @abc.abstractmethod
    async def async_update_wallpaper(cls):
        """异步更新壁纸所需要用到的函数。"""
        raise NotImplementedError

    def update_wallpaper(self):
        """同步更新壁纸所需要用到的函数。

        ### 注意
        这个函数是为了防止异步的不完全支持所预设的，不一定要在子类中实现，未来可能会删除。
        """
        raise NotImplementedError
