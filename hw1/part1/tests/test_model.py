from model import SomeModel


def test_predict_with_empty_string():
    model = SomeModel()
    prediction = model.predict("")
    assert prediction == 0.0


def test_predict_with_no_vowels():
    model = SomeModel()
    prediction = model.predict("rhythm")
    assert prediction == 0.0


def test_predict_with_vowels():
    model = SomeModel()
    prediction = model.predict("Hello")
    assert prediction == 0.4
