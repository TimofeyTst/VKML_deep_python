from custom_list import CustomList


# SUB
def test_result_different_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    result = cl1 - cl2

    assert result is not cl1
    assert result is not cl2


def test_custom_list_sub_empty():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([])

    assert list(cl1 - cl2) == [1, 2, 3]
    assert list(cl2 - cl1) == [-1, -2, -3]
    assert list(cl1 - cl1) == [0, 0, 0]
    assert list(cl2 - cl2) == []


def test_custom_list_sub_emptys():
    cl1 = CustomList([])
    cl2 = CustomList([])

    assert list(cl1 - cl2) == []
    assert list(cl2 - cl1) == []


# CustomList - CustomList
def test_custom_list_sub_grower_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    should_be = "CustomList([-4, 1, 4, -7]) = -6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_sub_less_len_custom_list():
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = CustomList([1, 2, 7])

    should_be = "CustomList([4, -1, -4, 7]) = 6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_sub_equal_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3])

    should_be = "CustomList([-4, 1, 4]) = 1"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


# CustomList - list
def test_custom_list_sub_less_len_list():
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = [1, 2, 7]

    should_be = "CustomList([4, -1, -4, 7]) = 6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_sub_grower_len_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = [5, 1, 3, 7]

    should_be = "CustomList([-4, 1, 4, -7]) = -6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_custom_list_sub_equal_len_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = [5, 1, 3]

    should_be = "CustomList([-4, 1, 4]) = 1"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


#  list - CustomList
def test_list_sub_less_len_custom_list():
    cl1 = [2, 5]
    cl2 = CustomList([1])

    should_be = "CustomList([1, 5]) = 6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_list_sub_grower_len_custom_list():
    cl1 = CustomList([1])
    cl2 = [2, 5]

    should_be = "CustomList([-1, -5]) = -6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)


def test_list_sub_equal_len_custom_list():
    cl1 = [5, 1, 3]
    cl2 = CustomList([1, 2, 7])

    should_be = "CustomList([4, -1, -4]) = -1"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert isinstance(result, CustomList)
