"""
    An example of using private attributes in Python.
    This is a common pattern in Python, but it is not enforced by the language.
    The private attribute is prefixed with two underscores, and a method is used to access it.
    The private attribute is not directly accessible outside of the class, but it is stored in a mangled name.
    The mangled name is the name of the class prefixed with an underscore and the name of the attribute.
    The mangled name can be used to access the private attribute outside of the class.
    E.g. private_attrs._PrivateAttrs__private_attr
"""


class PrivateAttrs:
    def __init__(self):
        self.__private_attr = "private_attr"
        self.public_attr = "public_attr"

    def get_private_attr(self):
        return self.__private_attr

    def get_public_attr(self):
        return self.public_attr


def main():
    private_attrs = PrivateAttrs()
    print(private_attrs.get_private_attr())
    print(private_attrs.get_public_attr())

    try:
        print(private_attrs.__private_attr)
    except AttributeError as e:
        print(e)


if __name__ == "__main__":
    main()
