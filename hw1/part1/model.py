class SomeModel:
    def predict(self, message: str) -> float:
        """
        Вычисляет предсказание на основе количества гласных в сообщении.

        Аргументы:
        message (str): Строка, в которой подсчитываем гласные.

        Возвращает:
        float: Предсказание как отношение числа гласных букв к длине сообщения.
               Значение находится в диапазоне от 0.0 до 1.0.

        Примечания:
        - Строка `message` будет приведена к нижнему регистру перед анализом.
        - Если `message` пустая строка, функция вернет 0.0.
        - Гласные буквы определены в строке `vowels`.

        Пример использования:
        >>> model = SomeModel()
        >>> prediction = model.predict("Доля гласных в сообщении")
        >>> print(prediction)
        0.3333333333333333
        """
        message_length = len(message)
        if message_length == 0:
            return 0.0  # Защита от деления на ноль

        message = message.lower()
        vowels = "aeiouаеёиоуиэюя"
        num_vowels = sum(1 for char in message if char in vowels)

        prediction_value = num_vowels / message_length
        return prediction_value
