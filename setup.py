from setuptools import setup
setup(
    name="pyonic_reader",
    version="1.0.0",
    install_requires=[
        "pymupdf"
    ],
    entry_points={
        "console_scripts":[
            "pyoreadr = pyonic_reader:printhelp"
        ]
    }
)