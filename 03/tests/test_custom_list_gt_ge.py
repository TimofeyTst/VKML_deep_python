from custom_list import CustomList


# gt
def test_custom_list_gt_grower_list():
    cl1 = CustomList([3, 2, 1, 5])
    cl2 = CustomList([1, 2, 3])

    assert cl1 > cl2


def test_custom_list_not_gt_equal_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([1, 2, 3])

    assert not (cl1 > cl2)


def test_custom_list_not_gt_lower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1, 5])

    assert not (cl1 > cl2)


def test_custom_list_not_gt_sub_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 - cl1

    assert cl1 > cl2
    assert cl2 is not cl1


# ge
def test_custom_list_ge_grower_list():
    cl1 = CustomList([3, 2, 1, 5])
    cl2 = CustomList([1, 2, 3])

    assert cl1 >= cl2


def test_custom_list_ge_equal_list():
    cl1 = CustomList([3, 2, 1])
    cl2 = CustomList([1, 2, 3])

    assert cl1 >= cl2


def test_custom_list_not_ge_equal_list():
    cl1 = CustomList([3, 2, 1])
    cl2 = CustomList([2, 2, 3])

    assert not (cl1 >= cl2)


def test_custom_list_not_ge_lower_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = CustomList([3, 2, 1, 5])

    assert not (cl1 >= cl2)


def test_custom_list_not_ge_sub_list():
    cl1 = CustomList([1, 2, 3])
    cl2 = cl1 - cl1

    assert cl1 >= cl2
    assert cl2 is not cl1
