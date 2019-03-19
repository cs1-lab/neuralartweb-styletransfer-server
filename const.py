"""
constant types in python
"""


class StyleConst:
    """
    styleに渡す定数を管理するクラス
    argsの代わり。
    """
    class ConstError(TypeError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            # 変更でいないよいうにする
            raise self.ConstError("Can't rebind const {}".format(key))
        self.__dict__[key] = value
