import pytest
from custom_list import CustomList


def test_custom_list_comparison_with_number():
    cl1 = CustomList([1, 2, 3])
    number = 4

    with pytest.raises(TypeError):
        cl1 > number

    with pytest.raises(TypeError):
        cl1 < number

    with pytest.raises(TypeError):
        cl1 >= number

    with pytest.raises(TypeError):
        cl1 <= number

    assert not (cl1 == number)
    assert cl1 != number

    with pytest.raises(TypeError):
        cl1 + number

    with pytest.raises(TypeError):
        number + cl1

    with pytest.raises(TypeError):
        cl1 - number

    with pytest.raises(TypeError):
        number - cl1


def test_custom_list_comparison_with_string():
    cl1 = CustomList([1, 2, 3])
    string = "4"

    with pytest.raises(TypeError):
        cl1 > string

    with pytest.raises(TypeError):
        cl1 < string

    with pytest.raises(TypeError):
        cl1 >= string

    with pytest.raises(TypeError):
        cl1 <= string

    assert not (cl1 == string)
    assert cl1 != string

    with pytest.raises(TypeError):
        cl1 + string

    with pytest.raises(TypeError):
        string + cl1

    with pytest.raises(TypeError):
        cl1 - string

    with pytest.raises(TypeError):
        string - cl1
