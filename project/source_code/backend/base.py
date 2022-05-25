from abc import ABC
class BaseClass(ABC):
    @classmethod
    def key_str(cls):
        s = ""
        for c in cls.__name__:
            s += c if c.islower() else " " + c.lower()
        return s[1:]