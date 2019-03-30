from setuptools import setup

setup(
    name='fordreader',
    version='1.0.0',
    install_requires=['pyserial'],
    py_modules=['fordreader', 'ELM327']
)
