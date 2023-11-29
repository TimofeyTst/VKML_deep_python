from setuptools import setup, Extension


def main():
    module = Extension("cjson", sources=["cjson.c"])

    setup(name="cjson", version="1.0.1", author="TimofeyTst", ext_modules=[module])


if __name__ == "__main__":
    main()
