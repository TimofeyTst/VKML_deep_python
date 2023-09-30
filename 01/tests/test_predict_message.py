from model import SomeModel
from predict_message import predict_message_mood
import pytest


def test_predict_message_mood_good_biggest_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.99999999

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "отл"


def test_predict_message_mood_good_greater_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.8000001

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "отл"


def test_predict_message_mood_norm_lower_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.7999999

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "норм"


def test_predict_message_mood_norm_greater_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.3000001

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "норм"


def test_predict_message_mood_bad_lower_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.2999999

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "неуд"


def test_predict_message_mood_bad_zero_value(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.0000001

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "неуд"


def test_predict_message_mood_bad(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.59

    message = "Тестовые согласные: цкнгшщзхфвпрлджчсмтб"
    result = predict_message_mood(message, mock_model, bad_thresholds=0.6)
    mock_model.predict.assert_called_once_with(message)
    assert result == "неуд"


def test_predict_message_mood_good(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.61

    message = "Тестовые гласные: aeiouаеёиоуиэюя"
    result = predict_message_mood(message, mock_model, good_thresholds=0.6)
    mock_model.predict.assert_called_once_with(message)
    assert result == "отл"


def test_predict_message_mood_normal(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.6

    message = "Доля гласных в сообщении"
    result = predict_message_mood(message, mock_model)
    mock_model.predict.assert_called_once_with(message)
    assert result == "норм"


def test_predict_message_with_custom_tresholds_med(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.65

    message = "Доля гласных в сообщении"
    result = predict_message_mood(
        message, mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    mock_model.predict.assert_called_once_with(message)
    assert result == "норм"


def test_predict_message_mood_with_custom_tresholds_good(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.71

    msg = "Доля гласных в сообщении"
    result = predict_message_mood(
        msg, mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    mock_model.predict.assert_called_once_with(msg)
    assert result == "отл"


def test_predict_message_mood_with_custom_tresholds_bad(mocker):
    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.01

    msg = "Доля гласных в сообщении"
    result = predict_message_mood(
        msg, mock_model, bad_thresholds=0.6, good_thresholds=0.7
    )
    mock_model.predict.assert_called_once_with(msg)
    assert result == "неуд"


def test_predict_message_mood_with_bad_threshold_greater_good(mocker):
    from predict_message import InvalidThresholdsError

    mock_model = mocker.Mock(spec=SomeModel)
    mock_model.predict.return_value = 0.01

    msg = "Доля гласных в сообщении"
    with pytest.raises(InvalidThresholdsError):
        predict_message_mood(
            msg,
            mock_model,
            bad_thresholds=0.8,
            good_thresholds=0.2,
        )
