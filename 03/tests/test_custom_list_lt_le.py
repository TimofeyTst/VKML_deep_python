from custom_list import CustomList


# lt
def test_custom_list_lt_grower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1, 5])

    assert cl1 < cl2


def test_custom_list_not_lt_equal_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([1, 2, 3])

    assert not (cl1 < cl2)


def test_custom_list_not_lt_lower_list():
    cl1 = CustomList([3, 2, 1, 5])
    cl2 = CustomList([1, 2, 3])

    assert not (cl1 < cl2)


def test_custom_list_not_lt_added_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 + cl1

    assert cl1 < cl2
    assert cl2 is not cl1


# le
def test_custom_list_le_grower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1, 5])

    assert cl1 <= cl2


def test_custom_list_le_equal_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1])

    assert cl1 <= cl2


def test_custom_list_not_le_equal_list():
    cl1 = CustomList([2, 2, 3])
    cl2 = CustomList([3, 2, 1])

    assert not (cl1 <= cl2)


def test_custom_list_not_le_lower_list():
    cl1 = CustomList([3, 2, 1, 5])
    cl2 = CustomList([1, 2, 3])

    assert not (cl1 <= cl2)


def test_custom_list_not_le_added_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 + cl1

    assert cl1 <= cl2
    assert cl2 is not cl1
