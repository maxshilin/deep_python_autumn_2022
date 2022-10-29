from setuptools import setup, Extension

setup(
    name="multiply",
    version="1.0",
    description="Matrix multiplication of two 2D python lists",
    author="Maxim Shilin",
    ext_modules=[Extension("multiply", ["multiply.c"])],
)
