class iPhoneDescriptor:
    VALID_MODELS = [
        "iPhone 15",
        "iPhone 15 Pro",
        "iPhone 14",
        "iPhone 14 Pro",
        "iPhone 13",
        "iPhone 13 Pro",
        "iPhone 12",
        "iPhone 12 Pro",
        "iPhone 11",
        "iPhone 11 Pro",
    ]

    def __set_name__(self, owner, name):
        self.name = f"apple_{name}"

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} должен быть строкой")

        if value not in self.VALID_MODELS:
            raise ValueError(f"Недопустимая модель {self.name}: {value}")
        return setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class MacBookDescriptor:
    VALID_MODELS = ["MacBook Air", "MacBook Pro"]

    def __set_name__(self, owner, name):
        self.name = f"apple_{name}"

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} должен быть строкой")
        if value not in self.VALID_MODELS:
            raise ValueError(f"Недопустимая модель {self.name}: {value}")
        return setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class ICloudEmailDescriptor:
    MAX_EMAIL_LENGTH_PRINT = 3  # Максимальная длина отображаемой почты
    ASTERIKS = "*****"
    DOMAIN = "@icloud.com"

    def __set_name__(self, owner, name):
        self.name = f"apple_{name}"

    def validate_email(self, email):
        if not isinstance(email, str):
            raise ValueError(f"{self.name} должен быть строкой")
        if not email.endswith("@icloud.com"):
            raise ValueError(f"{self.name} должен принадлежать @icloud.com")
        return email

    def __get__(self, instance, owner):
        email = getattr(instance, self.name)
        visible_index = min(email.index("@"), self.MAX_EMAIL_LENGTH_PRINT)
        visible_part = email[:visible_index]
        return f"{visible_part}{self.ASTERIKS}{self.DOMAIN}"

    def __set__(self, instance, value):
        validated_email = self.validate_email(value)
        return setattr(instance, self.name, validated_email)
