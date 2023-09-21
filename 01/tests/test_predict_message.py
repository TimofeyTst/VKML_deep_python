from model import SomeModel
from predict_message import predict_message_mood
import pytest


def test_predict_message_mood_bad(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.59

    result = predict_message_mood(
        "Тестовые согласные: цкнгшщзхфвпрлджчсмтб", mock_model, bad_thresholds=0.6
    )
    assert result == "неуд"


def test_predict_message_mood_good(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.61

    result = predict_message_mood(
        "Тестовые гласные: aeiouаеёиоуиэюя", mock_model, good_thresholds=0.6
    )
    assert result == "отл"


def test_predict_message_mood_normal(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.6

    result = predict_message_mood("Доля гласных в сообщении", mock_model)
    assert result == "норм"


def test_predict_message_with_custom_tresholds_med(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.65

    result = predict_message_mood(
        "Доля гласных в сообщении", mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    assert result == "норм"


def test_predict_message_mood_with_custom_tresholds_good(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.71

    result = predict_message_mood(
        "Доля гласных в сообщении", mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    assert result == "отл"


def test_predict_message_mood_with_custom_tresholds_bad(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.01

    result = predict_message_mood(
        "Доля гласных в сообщении", mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    assert result == "неуд"


def test_predict_message_mood_with_bad_threshold_greater_good(mocker):
    from predict_message import InvalidThresholdsError

    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.01

    with pytest.raises(InvalidThresholdsError):
        predict_message_mood(
            "Доля гласных в сообщении",
            mock_model,
            bad_thresholds=0.8,
            good_thresholds=0.2,
        )
