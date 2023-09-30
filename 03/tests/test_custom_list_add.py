from custom_list import CustomList


def test_custom_list_type():
    cl1 = CustomList([1, 2, 3])

    assert isinstance(cl1, list)
    assert isinstance(cl1, CustomList)

    result = cl1 + cl1
    assert result is not cl1


def test_custom_list_adding_empty():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([])

    assert list(cl1 + cl2) == [1, 2, 3]
    assert list(cl2 + cl1) == [1, 2, 3]


def test_custom_list_adding_emptys():
    cl1 = CustomList([])
    cl2 = CustomList([])

    assert list(cl1 + cl2) == []
    assert list(cl2 + cl1) == []


# ADD
def test_result_different_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    result = cl1 + cl2

    assert result is not cl1
    assert result is not cl2


def test_custom_list_add_grower_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    should_be = "CustomList([6, 3, 10, 7]) = 26"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_add_less_len_custom_list():
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = CustomList([1, 2, 7])

    should_be = "CustomList([6, 3, 10, 7]) = 26"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_add_equal_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3])

    should_be = "CustomList([6, 3, 10]) = 19"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_add_grower_len_list():
    cl1 = CustomList([1])
    cl2 = [2, 5]

    should_be = "CustomList([3, 5]) = 8"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_add_less_len_list():
    cl1 = CustomList([1, 5, 8])
    cl2 = [9]

    should_be = "CustomList([10, 5, 8]) = 23"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_add_equal_len_list():
    cl1 = CustomList([1, 5, 8])
    cl2 = [9, 5, 8]

    should_be = "CustomList([10, 10, 16]) = 36"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_radd_grower_len_list():
    cl1 = [2, 5]
    cl2 = CustomList([1])

    should_be = "CustomList([3, 5]) = 8"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_radd_less_len_list():
    cl1 = [9]
    cl2 = CustomList([1, 5, 8])

    should_be = "CustomList([10, 5, 8]) = 23"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_radd_equal_len_list():
    cl1 = [9, 5, 8]
    cl2 = CustomList([1, 5, 8])

    should_be = "CustomList([10, 10, 16]) = 36"
    result = cl1 + cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)
