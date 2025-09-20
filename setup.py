from setuptools import setup, find_packages
from pkg.__version__ import __version__

setup(
    name="netweaver",
    version=__version__,
    packages=find_packages(),
    install_requires=[
        "PyYAML",
    ],
    entry_points={
        "console_scripts": [
            "netweaver=cli.netweaver:main"
        ]
    },
)
