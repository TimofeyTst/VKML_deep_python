class CustomMeta(type):
    def __new__(mcs, name, bases, classdict):
        custom_dct = mcs.__get_new_dict(classdict)

        def custom_setattr(self, name, value):
            if name.startswith("__") and name.endswith("__"):
                super(self.__class__, self).__setattr__(name, value)
            else:
                super(self.__class__, self).__setattr__("custom_" + name, value)

        custom_dct["__setattr__"] = custom_setattr

        return super().__new__(mcs, name, bases, custom_dct)

    def __setattr__(self, name, value):
        if name.startswith("__") and name.endswith("__"):
            super().__setattr__(name, value)
        else:
            super().__setattr__("custom_" + name, value)

    @staticmethod
    def __get_new_dict(old_dict):
        custom_dct = {}
        for attr_name, attr_value in old_dict.items():
            if attr_name.startswith("__") and attr_name.endswith("__"):
                custom_dct[attr_name] = attr_value
            else:
                custom_dct["custom_" + attr_name] = attr_value

        return custom_dct
