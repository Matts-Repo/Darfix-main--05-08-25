"""
Setup configuration for Darfix with Orange widget support.
"""

from setuptools import setup, find_packages

setup(
    name="darfix",
    packages=find_packages(),
    namespace_packages=["orangecontrib"],
    entry_points={
        'orange.widgets': [
            'Darfix = orangecontrib.darfix.widgets',
        ],
        'orange.addons': [
            'darfix = orangecontrib.darfix',
        ],
    },
    keywords=[
        'orange3 add-on',
        'orange3-darfix',
        'x-ray diffraction',
        'data analysis',
    ],
)