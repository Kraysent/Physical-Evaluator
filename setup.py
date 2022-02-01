from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='physical_evaluator',
    version='0.3.14',
    description='Physical evaluator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Kraysent/Physical-Evaluator',
    license='MIT',
    packages=['physical_evaluator'],
    zip_safe=False,
    test_suite='physical_evaluator.tests',
)
