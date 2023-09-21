from filter_lines import filter_lines


def test_filter_lines(temp_file):
    search_words = ["роза", "азора"]

    result = list(filter_lines(temp_file, search_words))
    assert len(result) == 1
    assert result[0] == "а Роза упала на лапу Азора\n"


def test_filter_lines_with_diff_register(temp_file):
    search_words = ["роза", "АзОрА"]
    result = list(filter_lines(temp_file, search_words))
    assert len(result) == 1
    assert result[0] == "а Роза упала на лапу Азора\n"


def test_filter_lines_with_empty_result(temp_file):
    search_words = ["слово1", "слово2"]
    result = list(filter_lines(temp_file, search_words))
    assert len(result) == 0
