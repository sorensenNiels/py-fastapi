"""
    An example of using protected attributes in Python. 
    This is a common pattern in Python, but it is not enforced by the language.
    The protected attribute is prefixed with an underscore, and a property is used to access it.
    The property can be overridden in a subclass, but the subclass must use the same name for the property.
    The subclass can also override the protected attribute, but it must use a different name.
"""


from abc import ABC, abstractmethod
from typing import override


class ProtectedAttrsBase(ABC):
    def __init__(self):
        self._protected_attr = "protected_attr"

    @property
    def protected_attr(self):
        return self._protected_attr

    @protected_attr.setter
    def protected_attr(self, value):
        self._protected_attr = value

    @abstractmethod
    def abstract_method(self):
        pass


class ProtectedAttrs(ProtectedAttrsBase):
    def __init__(self):
        super().__init__()
        self._protected_attr = "protected_attr"

    @override
    def abstract_method(self):
        pass

    def annother_method(self):
        pass


def main():
    pa = ProtectedAttrs()
    pa.protected_attr = "new value"
    print(pa.protected_attr)
    pa.abstract_method()
    pa.annother_method()


if __name__ == "__main__":
    main()
