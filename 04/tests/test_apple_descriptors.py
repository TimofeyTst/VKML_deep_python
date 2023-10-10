from apple_descriptors import iPhoneDescriptor, MacBookDescriptor, ICloudEmailDescriptor
import pytest


class AppleEcoSystem:
    iphone = iPhoneDescriptor()
    mac = MacBookDescriptor()
    email = ICloudEmailDescriptor()

    def __init__(self, iphone, mac, email):
        self.iphone = iphone
        self.mac = mac
        self.email = email


def test_descriptors_get_values():
    acc1 = AppleEcoSystem("iPhone 14", "MacBook Pro", "example@icloud.com")

    assert acc1.iphone == "iPhone 14"
    assert acc1.mac == "MacBook Pro"
    assert acc1.email == "exa*****@icloud.com"


def test_descriptors_change_values():
    acc1 = AppleEcoSystem("iPhone 14", "MacBook Pro", "example@icloud.com")

    acc1.iphone = "iPhone 15 Pro"
    acc1.mac = "MacBook Air"
    acc1.email = "new_email@icloud.com"

    assert acc1.iphone == "iPhone 15 Pro"
    assert acc1.mac == "MacBook Air"
    assert acc1.email == "new*****@icloud.com"


def test_many_descriptors_values():
    acc1 = AppleEcoSystem("iPhone 13", "MacBook Pro", "tstu@icloud.com")
    acc2 = AppleEcoSystem("iPhone 12 Pro", "MacBook Air", "elau@icloud.com")
    acc3 = AppleEcoSystem("iPhone 13 Pro", "MacBook Pro", "ilau@icloud.com")

    assert acc1.iphone == "iPhone 13"
    assert acc2.iphone == "iPhone 12 Pro"
    assert acc3.iphone == "iPhone 13 Pro"

    assert acc1.mac == "MacBook Pro"
    assert acc2.mac == "MacBook Air"
    assert acc3.mac == "MacBook Pro"

    assert acc1.email == "tst*****@icloud.com"
    assert acc2.email == "ela*****@icloud.com"
    assert acc3.email == "ila*****@icloud.com"


def test_icloud_email_decsriptor_set():
    class AppleClass:
        email = ICloudEmailDescriptor()

        def __init__(self, email):
            self.email = email

    with pytest.raises(ValueError, match="apple_email должен быть строкой"):
        AppleClass(123)

    with pytest.raises(ValueError, match="apple_email должен быть строкой"):
        AppleClass({"example@icloud.com"})

    with pytest.raises(ValueError, match="apple_email должен принадлежать @icloud.com"):
        AppleClass("some empty class")


def test_icloud_email_decsriptor_get():
    class AppleClass:
        email = ICloudEmailDescriptor()

        def __init__(self, email):
            self.email = email

    apple = AppleClass("gls777@icloud.com")
    assert apple.email == "gls*****@icloud.com"

    apple.email = "g1@icloud.com"
    assert apple.email == "g1*****@icloud.com"

    apple.email = "g123456789g123456789@icloud.com"
    assert apple.email == "g12*****@icloud.com"

    with pytest.raises(ValueError, match="apple_email должен принадлежать @icloud.com"):
        apple.email = "gls777000@icloud.ceo"
    assert apple.email == "g12*****@icloud.com"


def test_mac_book_decsriptor_set():
    class AppleClass:
        mac = MacBookDescriptor()

        def __init__(self, mac):
            self.mac = mac

    with pytest.raises(ValueError, match="apple_mac должен быть строкой"):
        AppleClass(123)

    with pytest.raises(ValueError, match="apple_mac должен быть строкой"):
        AppleClass({"MacBook Air"})

    with pytest.raises(
        ValueError, match="Недопустимая модель apple_mac: MacBook Not Air"
    ):
        AppleClass("MacBook Not Air")


def test_mac_book_decsriptor_get():
    class AppleClass:
        mac = MacBookDescriptor()

        def __init__(self, mac):
            self.mac = mac

    apple = AppleClass("MacBook Air")
    assert apple.mac == "MacBook Air"

    apple.mac = "MacBook Pro"
    assert apple.mac == "MacBook Pro"

    with pytest.raises(ValueError, match="Недопустимая модель apple_mac: Macbooking"):
        apple.mac = "Macbooking"
    assert apple.mac == "MacBook Pro"


def test_iphone_decsriptor_set():
    class AppleClass:
        iphone = iPhoneDescriptor()

        def __init__(self, iphone):
            self.iphone = iphone

    with pytest.raises(ValueError, match="apple_iphone должен быть строкой"):
        AppleClass(123)

    with pytest.raises(ValueError, match="apple_iphone должен быть строкой"):
        AppleClass({"iPhone 15"})

    with pytest.raises(
        ValueError, match="Недопустимая модель apple_iphone: iPhone 15 Product"
    ):
        AppleClass("iPhone 15 Product")


def test_iphone_decsriptor_get():
    class AppleClass:
        iphone = iPhoneDescriptor()

        def __init__(self, iphone):
            self.iphone = iphone

    apple = AppleClass("iPhone 15 Pro")
    assert apple.iphone == "iPhone 15 Pro"

    apple.iphone = "iPhone 13 Pro"
    assert apple.iphone == "iPhone 13 Pro"

    with pytest.raises(
        ValueError, match="Недопустимая модель apple_iphone: iPhone 23 AI"
    ):
        apple.iphone = "iPhone 23 AI"
    assert apple.iphone == "iPhone 13 Pro"
