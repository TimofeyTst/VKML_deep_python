import pytest
from custom_meta import CustomMeta


def test_custom_meta():
    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self, val=99):
            self.val = val

        def line(self):
            return 100

        def __str__(self):
            return "Custom_by_metaclass"

    assert CustomClass.custom_x == 50

    with pytest.raises(AttributeError):
        CustomClass.x


def test_custom_meta_instance():
    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self, val=99):
            self.val = val

        def line(self):
            return 100

        def __str__(self):
            return "Custom_by_metaclass"

    inst = CustomClass()
    assert inst.custom_x == 50
    assert inst.custom_val == 99
    assert inst.custom_line() == 100
    assert str(inst) == "Custom_by_metaclass"

    with pytest.raises(AttributeError):
        inst.x

    with pytest.raises(AttributeError):
        inst.val

    with pytest.raises(AttributeError):
        inst.val

    with pytest.raises(AttributeError):
        inst.line()

    with pytest.raises(AttributeError):
        inst.yyy

    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"
    with pytest.raises(AttributeError):
        inst.dynamic


def test_custom_meta_private_attrs():
    class CustomClass(metaclass=CustomMeta):
        __x = 51

        def __init__(self, val=99, val2=11):
            self.__val = val
            self._val2 = val2

    cm = CustomClass()
    cm.custom__CustomClass__x == 51
    cm.custom__CustomClass__val == 50
    cm.custom__val2 == 11

    with pytest.raises(AttributeError):
        cm.__x

    with pytest.raises(AttributeError):
        cm.__val

    with pytest.raises(AttributeError):
        cm.__val2


def test_custom_meta_dynamic_attrs():
    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self):
            pass

    inst = CustomClass()
    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"

    CustomClass.new_static_attr = 100
    assert CustomClass.custom_new_static_attr == 100

    with pytest.raises(AttributeError):
        inst.dynamic

    with pytest.raises(AttributeError):
        inst.new_static_attr


def test_custom_meta_dynamic_attrs_multiple():
    class CustomClass(metaclass=CustomMeta):
        x = 50

        def __init__(self):
            pass

    inst = CustomClass()
    inst.dynamic = "added later"
    assert inst.custom_dynamic == "added later"
    inst.dynamic = "added later2"
    assert inst.custom_dynamic == "added later2"

    with pytest.raises(AttributeError):
        inst.dynamic


def test_custom_meta_method():
    class CustomClass(metaclass=CustomMeta):
        def some_method(self):
            return "original"

        def __str__(self):
            return "Custom_by_metaclass"

    inst = CustomClass()
    assert inst.custom_some_method() == "original"
    assert str(inst) == "Custom_by_metaclass"
