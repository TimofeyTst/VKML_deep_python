from model import SomeModel


class InvalidThresholdsError(Exception):
    pass


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    """
    Вычисляет предсказание на основе сообщения.

    Аргументы:
    message (str): Строка, на основе которой предсказываем,
    model (SomeModel): Модель, которая делает предсказание,
    bad_thresholds (float): Порог предсказания, ниже которого считаем его плохим,
    good_thresholds (float): Порог предсказания, выше которого считаем его хорошим.

    Возвращает:
    str: Предсказание "неуд" | "норм" | "отл".

    Примечания:
    - Если `bad_thresholds` больше `good_thresholds` функция выбросит
        исключение InvalidThresholdsError.

    Пример использования:
    >>> model = SomeModel()
    >>> prediction = predict_message_mood("Доля гласных в сообщении", model)
    >>> print(prediction)
    норм
    """
    if bad_thresholds > good_thresholds:
        raise InvalidThresholdsError(
            "bad_thresholds cannot be greater than good_thresholds."
        )

    y_pred = model.predict(message)

    if y_pred < bad_thresholds:
        return "неуд"

    if y_pred > good_thresholds:
        return "отл"

    return "норм"
