from custom_list import CustomList


def test_custom_list_eq_reverse_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1])

    assert cl1 == cl2


def test_custom_list_not_eq_lower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([6])

    assert cl1 == cl2


def test_custom_list_not_eq_added_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 + cl1 - cl1

    assert cl1 == cl2
    assert cl2 is not cl1


def test_custom_list_not_eq():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([4, 5, 6])

    assert not (cl1 == cl2)


def test_custom_list_not_eq_empty():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([])

    assert not (cl1 == cl2)


# ne
def test_custom_list_ne_reverse_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1])

    assert not (cl1 != cl2)


def test_custom_list_not_ne_lower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([6])

    assert not (cl1 != cl2)


def test_custom_list_ne_added_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 + cl1

    assert cl1 != cl2
    assert cl2 is not cl1


def test_custom_list_ne():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([4, 5, 6])

    assert cl1 != cl2


def test_custom_list_ne_empty():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([])

    assert cl1 != cl2
