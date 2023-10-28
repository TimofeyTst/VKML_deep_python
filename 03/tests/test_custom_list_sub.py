from custom_list import CustomList


# SUB
def test_result_different_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    result = cl1 - cl2

    assert result is not cl1
    assert result is not cl2
    assert list(cl1) == [1, 2, 7]
    assert list(cl2) == [5, 1, 3, 7]


def test_custom_list_sub_empty():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([])

    assert list(cl1 - cl2) == [1, 2, 3]
    assert list(cl2 - cl1) == [-1, -2, -3]
    assert list(cl1 - cl1) == [0, 0, 0]
    assert list(cl2 - cl2) == []
    assert list(cl1) == [1, 2, 3]
    assert list(cl2) == []


def test_custom_list_sub_emptys():
    cl1 = CustomList([])
    cl2 = CustomList([])

    assert list(cl1 - cl2) == []
    assert list(cl2 - cl1) == []
    assert list(cl1) == []
    assert list(cl2) == []


# CustomList - CustomList
def test_custom_list_sub_grower_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3, 7])

    result = cl1 - cl2

    assert list(result) == [-4, 1, 4, -7]
    assert isinstance(result, CustomList)
    assert list(cl1) == [1, 2, 7]
    assert list(cl2) == [5, 1, 3, 7]


def test_custom_list_sub_less_len_custom_list():
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = CustomList([1, 2, 7])

    result = cl1 - cl2

    assert list(result) == [4, -1, -4, 7]
    assert isinstance(result, CustomList)
    assert list(cl1) == [5, 1, 3, 7]
    assert list(cl2) == [1, 2, 7]


def test_custom_list_sub_equal_len_custom_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = CustomList([5, 1, 3])

    result = cl1 - cl2

    assert list(result) == [-4, 1, 4]
    assert isinstance(result, CustomList)
    assert list(cl1) == [1, 2, 7]
    assert list(cl2) == [5, 1, 3]



# CustomList - list
def test_custom_list_sub_less_len_list():
    cl1 = CustomList([5, 1, 3, 7])
    cl2 = [1, 2, 7]

    result = cl1 - cl2

    assert list(result) == [4, -1, -4, 7]
    assert isinstance(result, CustomList)
    assert list(cl1) == [5, 1, 3, 7]
    assert cl2 == [1, 2, 7]



def test_custom_list_sub_grower_len_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = [5, 1, 3, 7]

    result = cl1 - cl2

    assert list(result) == [-4, 1, 4, -7]
    assert isinstance(result, CustomList)
    assert list(cl1) == [1, 2, 7]
    assert cl2 == [5, 1, 3, 7]



def test_custom_list_sub_equal_len_list():
    cl1 = CustomList([1, 2, 7])
    cl2 = [5, 1, 3]

    result = cl1 - cl2

    assert list(result) == [-4, 1, 4]
    assert isinstance(result, CustomList)
    assert list(cl1) == [1, 2, 7]
    assert cl2 == [5, 1, 3]



#  list - CustomList
def test_list_sub_less_len_custom_list():
    cl1 = [2, 5]
    cl2 = CustomList([1])

    result = cl1 - cl2

    assert list(result) == [1, 5]
    assert isinstance(result, CustomList)
    assert cl1 == [2, 5]
    assert list(cl2) == [1]



def test_list_sub_grower_len_custom_list():
    cl1 = CustomList([1])
    cl2 = [2, 5]

    should_be = "CustomList([-1, -5]) = -6"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert list(result) == [-1, -5]
    assert isinstance(result, CustomList)
    assert list(cl1) == [1]
    assert cl2 == [2, 5]


def test_list_sub_equal_len_custom_list():
    cl1 = [5, 1, 3]
    cl2 = CustomList([1, 2, 7])

    should_be = "CustomList([4, -1, -4]) = -1"
    result = cl1 - cl2

    assert result.__str__() == should_be
    assert list(result) == [4, -1, -4]
    assert isinstance(result, CustomList)
    assert cl1 == [5, 1, 3]
    assert list(cl2) == [1, 2, 7]

