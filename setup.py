from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='py_text_in_order',
    version='0.0.1',
    description='Tools for processing and ordering OCR text in line.',
    author='PortADa team',
    author_email='agustin.nieto77@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/portada-git/py_text_in_order',  
    packages=['py_text_in_order'],
    py_modules=['text_in_order'],
    install_requires=[
        'json',
        'os',
    ],
    python_requires='>=3.8',
    zip_safe=False
)
