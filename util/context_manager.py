# util/context_manager.py
class GlobalContext:
    """全局上下文管理器，用于在不同用例或步骤间共享数据"""
    _cache = {}

    @classmethod
    def set(cls, key, value):
        cls._cache[key] = value

    @classmethod
    def get(cls, key, default=None):
        return cls._cache.get(key, default)

    @classmethod
    def clear(cls):
        cls._cache.clear()